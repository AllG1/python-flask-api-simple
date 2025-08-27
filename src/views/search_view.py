""" APIs for Search """

import logging

from flask import Blueprint, jsonify
from response_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from db import get_employee, get_employees_by_position, get_employees_by_department
from utils import make_response_form, EmployeeSearchResponse


search_bp = Blueprint('search', __name__, url_prefix='/search')
logger = logging.getLogger("app")


# ==============================================================================================
# APIs
# ==============================================================================================


@search_bp.route("/id/<int:employee_id>")
def search_by_id(employee_id: int):
    """
    Search API for a specific employee ID

    :param employee_id: The ID of the employee to search for
    :return: A JSON response with the search result
    """
    logger.info(f"Search by ID received: {employee_id}")

    try:
        # Here you would typically query your database or data source
        # For demonstration, we will just return a mock response
        if employee_id < 0:
            raise ValueError("Employee ID must be a positive integer or 0")

        # get employee data from database or data source
        employee_data = get_employee(employee_id)
        logger.info(f"Employee data retrieved: {employee_data}")

        # make response form
        if employee_data:
            employee_response = EmployeeSearchResponse(**employee_data)
        else:
            employee_response = None

        if employee_data:
            resp, http_code = make_response_form(data=employee_response.model_dump())
        else:  # no data found
            resp, http_code = make_response_form(http_status=HTTP_404_NOT_FOUND)
        return jsonify(resp), http_code

    except ValueError as e:
        logger.error(f"Error occurred: {e}")
        resp, http_code = make_response_form(http_status=HTTP_500_INTERNAL_SERVER_ERROR)
        return jsonify(resp), http_code


@search_bp.route("/position/<int:position_id>")
def search_by_position(position_id: int):
    """
    Search API for a specific position ID

    :param position_id: The ID of the position to search for
         - 0: Employee
         - 1: Manager
         - 2: Director
    :return: A JSON response with the search result
    """
    logger.info(f"Search by position received: {position_id}")

    try:
        if position_id < 0:
            raise ValueError("Position ID must be a positive integer or 0")

        # get employee data from database or data source
        employee_data = get_employees_by_position(position_id)
        logger.info(f"Employee data retrieved: {employee_data}")
        if employee_data:
            resp, http_code = make_response_form(data={"employees": employee_data})
        else:  # no data found
            resp, http_code = make_response_form(data={"employees": list()})
        return jsonify(resp), http_code

    except ValueError as e:
        logger.error(f"Error occurred: {e}")
        resp, http_code = make_response_form(http_status=HTTP_500_INTERNAL_SERVER_ERROR)
        return jsonify(resp), http_code
    

@search_bp.route("/department/<int:department_id>")
def search_by_department(department_id: int):
    """
    Search API for a specific department ID

    :param department_id: The ID of the department to search for
         - 0: Sales
         - 1: IT
         - 2: HR
    :return: A JSON response with the search result
    """
    logger.info(f"Search by department received: {department_id}")

    try:
        if department_id < 0:
            raise ValueError("Department ID must be a positive integer or 0")

        # get employee data from database or data source
        employee_data = get_employees_by_department(department_id)
        logger.info(f"Employee data retrieved: {employee_data}")
        if employee_data:
            resp, http_code = make_response_form(data={"employees": employee_data})
        else:  # no data found
            resp, http_code = make_response_form(data={"employees": list()})
        return jsonify(resp), http_code

    except ValueError as e:
        logger.error(f"Error occurred: {e}")
        resp, http_code = make_response_form(http_status=HTTP_500_INTERNAL_SERVER_ERROR)
        return jsonify(resp), http_code
