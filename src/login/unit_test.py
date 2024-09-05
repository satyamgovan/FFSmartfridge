import unittest
from unittest.mock import patch
from src.login.login import LoginSystem


class TestLoginSystem(unittest.TestCase):

    def setUp(self):
        self.db_path = '../../database/database.db'
        self.login_system = LoginSystem(self.db_path)

    @patch('src.login.login.DatabaseManager')
    def test_validate_login_success(self, mock_db_manager):
        mock_db_manager.return_value.conditional_select.return_value = [
            (1, 'tester', 'tester', 'Delivery Driver')
        ]

        username = 'tester'
        password = 'tester'
        user_id, user_role = self.login_system.validate_login(username, password)

        self.assertIsNotNone(user_id)
        self.assertEqual(user_role, 'Delivery Driver')

    @patch('src.login.login.DatabaseManager')
    def test_validate_login_failure(self, mock_db_manager):
        mock_db_manager.return_value.conditional_select.return_value = []

        username = 'wronguser'
        password = 'wrongpass'
        user_id, user_role = self.login_system.validate_login(username, password)

        self.assertIsNone(user_id)
        self.assertIsNone(user_role)


if __name__ == '__main__':
    unittest.main()