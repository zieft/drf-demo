"""
Test custom Django management commands.
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django. test import SimpleTestCase

@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True  # when .check methods is called, return True, nothing else
        
        call_command('wait_for_db')  # defined in /management/commands/wait_for_commands.py
        
        patched_check.assert_called_once_with(databases=['default'])  
        # check if "check" has been called exact once & with parameter database=['default'],
        # if not called or called more than once, an Error will be raised.
        
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        
        # setup the Mocking
        # 当这个方法被调用时，将依次返回 Psycopg2Error 错误两次，返回 OperationalError 错误三次，然后返回 True
        patched_check.side_effect = [Psycopg2OpError] * 2 + [OperationalError] * 3 + [True]
        
        call_command('wait_for_db')
        
        # 检查 patched_check 方法是否被调用了六次。如果不是，这个断言（assertion）将会失败，测试也会失败。
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
        