""" APIs for Search """

import logging
from flask import Blueprint, jsonify

from db import get_employee


search_bp = Blueprint('search', __name__, url_prefix='/search')
logger = logging.getLogger("app")


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
        return jsonify({"employee_data": employee_data})

    except ValueError as e:
        logger.error(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 400
