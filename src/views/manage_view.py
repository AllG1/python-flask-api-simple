""" APIs for manage employee """

from datetime import datetime, timezone
import logging
import re
from typing import Tuple

from flask import Blueprint, jsonify, request
from pydantic import BaseModel, field_validator
from response_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_204_NO_CONTENT

from db import create_employee, inactivate_employee, promote_employee, transfer_employee
from utils.response_form import make_response_form


manage_bp = Blueprint('manage', __name__, url_prefix='/manage')
logger = logging.getLogger("app")



# ============================================================================================
# Pydantic classes & methods for query validation
# ============================================================================================


class CreateEmployeeRequest(BaseModel):
    first_name: str
    surname: str = ""
    position: int
    department: int
    phone_number: str
    email: str
    birth_date: Optional[str] = None

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
            return None
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
            raise ValueError("Invalid birth date format. Expected YYYY-MM-DD.")
        elif not datetime.strptime(value, "%Y-%m-%d"):
            raise ValueError("Invalid birth date. Date does not exist.")
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


def is_valid_position(position: str) -> Tuple[bool, int]:
    """ 
    Check the position valid
    :param position: position name
    :return: Tuple[bool, int] - (is_valid, position_id)
    """
    valid_positions = {"employee": 0, "manager": 1, "admin": 2}
    return position.lower() in valid_positions.keys(), valid_positions.get(position.lower(), -1)


def is_valid_department(department: str) -> Tuple[bool, int]:
    """
    Check the department valid
    :param department: department name
    :return: Tuple[bool, int] - (is_valid, department_id)
    """
    valid_departments = {"hr": 0, "it": 1, "sales": 2}
    return department.lower() in valid_departments.keys(), valid_departments.get(department.lower(), -1)

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
        logger.info(f"Validation error occurred: {e}")

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
        employee_id = create_employee(employee_data)
        if employee_id:
            logger.info(f"Employee created successfully: (employee id: {employee_id}) {employee_data}")
            resp, http_code = make_response_form(http_status=HTTP_201_CREATED)
        else:
            logger.info(f"Failed to create employee: {employee_data}")
            resp, http_code = make_response_form(http_status=HTTP_500_INTERNAL_SERVER_ERROR)
        return jsonify(resp), http_code

    except Exception as e:
        logger.exception(f"Error occurred: {e}")
        resp, http_code = make_response_form(http_status=HTTP_500_INTERNAL_SERVER_ERROR)
        return jsonify(resp), http_code


@manage_bp.route("/inactivate/<int:employee_id>", methods=["POST"])
def inactivate_employee_route(employee_id: int):
    """
    Route to inactivate an employee.
    Use this function if the employee cannot work anymore (e.g. fired, resigned)
    :param employee_id: The ID of the employee to inactivate
    """
    logger.info(f"Inactivate employee request received for ID: {employee_id}")

    try:
        # Call the inactivate_employee function from the db module
        inactivate_employee(employee_id)
        logger.info(f"Employee inactivated successfully: {employee_id}")
        resp, http_code = make_response_form(http_status=HTTP_200_OK)
        return jsonify(resp), http_code

    except Exception as e:
        logger.exception(f"Error occurred: {e}")
        resp, http_code = make_response_form(http_status=HTTP_500_INTERNAL_SERVER_ERROR)
        return jsonify(resp), http_code


@manage_bp.route("/position/<int:employee_id>/<string:new_position>", methods=["POST"])
def promote_employee_route(employee_id: int, new_position: str):
    """
    Route to promote an employee to a new position.
    :param employee_id: The ID of the employee who will change position
    :param new_position: The new position to assign to the employee
    """
    logger.info(f"Promote employee request received for ID: {employee_id} to position: {new_position}")

    # check valid position
    valid_position, position_id = is_valid_position(new_position)
    if not valid_position:
        resp, http_code = make_response_form(http_status=HTTP_400_BAD_REQUEST, description="Invalid position")
        return jsonify(resp), http_code

    # update employee position
    try:
        # Call the promote_employee function from the db module
        promote_employee(employee_id, position_id)
        logger.info(f"Employee promoted successfully: {employee_id} to position: {new_position}(id: {position_id})")
        resp, http_code = make_response_form(http_status=HTTP_200_OK)
        return jsonify(resp), http_code

    except Exception as e:
        logger.exception(f"Error occurred: {e}")
        resp, http_code = make_response_form(http_status=HTTP_500_INTERNAL_SERVER_ERROR)
        return jsonify(resp), http_code


@manage_bp.route("/department/<int:employee_id>/<string:new_department>", methods=["POST"])
def department_transfer_route(employee_id: int, new_department: str):
    """
    Route to transfer an employee to a new department.
    :param employee_id: The ID of the employee who will transfer the department
    :param new_department: The Name of the new department
    """
    logger.info(f"Transfer employee request received for employee ID: {employee_id} to department ID: {department_id}")

    # check valid department
    valid_department, department_id = is_valid_department(new_department)
    if not valid_department:
        resp, http_code = make_response_form(http_status=HTTP_400_BAD_REQUEST, description="Invalid department")
        return jsonify(resp), http_code
    
    # update employee department
    try:
        # Call the transfer_employee function from the db module
        transfer_employee(employee_id, department_id)
        logger.info(f"Employee transferred successfully: {employee_id} to department: {new_department}(id: {department_id})")
        resp, http_code = make_response_form(http_status=HTTP_200_OK)
        return jsonify(resp), http_code

    except Exception as e:
        logger.exception(f"Error occurred: {e}")
        resp, http_code = make_response_form(http_status=HTTP_500_INTERNAL_SERVER_ERROR)
        return jsonify(resp), http_code
