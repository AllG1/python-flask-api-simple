""" APIs for manage employee """

from datetime import datetime, timezone
import logging
import re

from flask import Blueprint, jsonify, request
from pydantic import BaseModel, field_validator, ValidationError
from response_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from db import create_employee
from utils.response_form import make_response_form


manage_bp = Blueprint('manage', __name__, url_prefix='/manage')
logger = logging.getLogger("app")



# ============================================================================================
# Pydantic classes for query validation
# ============================================================================================


class CreateEmployeeRequest(BaseModel):
    first_name: str
    surname: str = ""
    position: int
    department: int
    phone_number: str
    email: str
    birth_date: str = "0000-00-00"

    @field_validator("email")
    def validate_email(cls, value):
        if "@" not in value:
            raise ValueError("Invalid email address")
        return value
    
    @field_validator("birth_date")
    def validate_birth_date(cls, value):
        # check birth_date is in YYYY-MM-DD format
        # If there's no birthday information of employee, then insert 0000-00-00
        if not value:
            return "0000-00-00"
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
            raise ValueError("Invalid birth date format. Expected YYYY-MM-DD.")
        return value
    
    @field_validator("position", mode="before")
    def validate_position(cls, value):
        if isinstance(value, str):
            if value.lower() == "employee":
                return 0
            elif value.lower() == "manager":
                return 1
            elif value.lower() == "admin":
                return 2
            else:
                raise ValueError("Invalid position. Expected one of: employee, manager, admin.")
        elif isinstance(value, int):
            if value not in [0, 1, 2]:
                raise ValueError("Invalid position. Expected one of: 0 (employee), 1 (manager), 2 (admin).")
        return value

    @field_validator("department", mode="before")
    def validate_department(cls, value):
        if isinstance(value, str):
            if value.lower() == "hr":
                return 0
            elif value.lower() == "it":
                return 1
            elif value.lower() == "sales":
                return 2
            else:
                raise ValueError("Invalid department. Expected one of: hr, IT, sales.")
        elif isinstance(value, int):
            if value not in [0, 1, 2]:
                raise ValueError("Invalid department. Expected one of: 0 (hr), 1 (IT), 2 (sales).")
        return value


# ============================================================================================
# APIs
# ============================================================================================


@manage_bp.route("/create", methods=["POST"])
def create_employee_route():
    """
    Route to create a new employee
    """
    logger.info("Create employee request received")

    # check parameter
    try:
        request_data = CreateEmployeeRequest(**request.form.to_dict())
    except Exception as e:
        logger.error(f"Validation error occurred: {e}")

        # check some field are missing
        missing_fields = list()
        try:
            required_fields = list(
                map(
                    lambda item: item[0],
                    filter(lambda item: item[1].is_required(), CreateEmployeeRequest.model_fields.items())
                )
            )
            missing_fields = list(filter(lambda x: x not in request.form, required_fields))
        except:
            pass
        description = f"Missing fields: {','.join(missing_fields)}" if missing_fields else "Validation error occurred"

        resp, http_code = make_response_form(http_status=HTTP_400_BAD_REQUEST, description=description)
        return jsonify(resp), http_code

    try:
        # Here you would typically get the employee data from the request
        # For demonstration, we will just use a mock employee data
        employee_data = {
            "first_name": request_data.first_name,
            "surname": request_data.surname,
            "position": request_data.position,
            "department": request_data.department,
            "phone_number": request_data.phone_number,
            "email": request_data.email,
            "birth_date": request_data.birth_date,
            "status": 1,  # Assuming status is always active for new employees
            "description": request.form.get("description", ""),
            "register_time": datetime.now(timezone.utc).isoformat()  # Current time in ISO format
        }

        # Call the create_employee function from the db module
        create_employee(employee_data)
        logger.info(f"Employee created successfully: {employee_data}")
        resp, http_code = make_response_form(http_status=HTTP_201_CREATED)
        return jsonify(resp), http_code

    except Exception as e:
        logger.exception(f"Error occurred: {e}")
        resp, http_code = make_response_form(http_status=HTTP_500_INTERNAL_SERVER_ERROR)
        return jsonify(resp), http_code
