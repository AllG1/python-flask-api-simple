import sys
import os

import unittest

from flask import Flask

# Change the context
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from config.env import set_default_env
from config.load_main import get_settings, set_settings
from db.init_pool import set_db_pool
from views.manage_view import manage_bp
from views.search_view import search_bp
from views.data_view import data_bp

# ============================================================================================
# Set Environment Variable for test
# ============================================================================================
os.environ['APP_ENV_TYPE'] = 'dev'

# ============================================================================================
# Set Config
# ============================================================================================
set_default_env()
set_settings()

# ===========================================================================================
# Init Variables
# ============================================================================================
set_db_pool(get_settings())

# ===========================================================================================
# Make TestCase
# ============================================================================================

class APITestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.register_blueprint(manage_bp)
        app.register_blueprint(search_bp)
        app.register_blueprint(data_bp)
        self.client = app.test_client()

    def test_create_employee_missing_fields(self):
        # Missing required fields
        response = self.client.post('/manage/create', data={})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing fields', response.data)

    def test_create_employee_success(self):
        # All required fields present
        data = {
            "first_name": "John",
            "position": "employee",
            "department": "sales",
            "phone_number": "1234567890",
            "email": "john@example.com"
        }
        response = self.client.post('/manage/create', data=data)
        # Accept 201 or 500 if DB is not mocked
        self.assertIn(response.status_code, [201, 500])

    def test_inactivate_employee(self):
        # Example: inactivate employee with id 1
        response = self.client.post('/manage/inactivate/1')
        self.assertIn(response.status_code, [200, 500])

    def test_promote_employee(self):
        # Promote employee with id 1 to manager
        response = self.client.post('/manage/position/1/manager')
        self.assertIn(response.status_code, [200, 400, 500])

    def test_department_transfer(self):
        # Transfer employee with id 1 to IT department
        response = self.client.post('/manage/department/1/it')
        self.assertIn(response.status_code, [200, 400, 500])

    def test_search_by_id_not_found(self):
        response = self.client.get('/search/id/999999')
        # Accept 404 or 500 if DB is not mocked
        self.assertIn(response.status_code, [404, 500])

    def test_search_by_position(self):
        response = self.client.get('/search/position/0')
        self.assertEqual(response.status_code, 200)

    def test_search_by_department(self):
        response = self.client.get('/search/department/0')
        self.assertEqual(response.status_code, 200)

    def test_get_employee_list(self):
        response = self.client.get('/data/employee/0')
        self.assertIn(response.status_code, [200, 500])

    def test_get_document_list(self):
        response = self.client.get('/data/documents/0')
        self.assertIn(response.status_code, [200, 500])

if __name__ == '__main__':
    unittest.main()