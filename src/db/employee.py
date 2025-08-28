""" Some execution context for employee database operations """

import logging
from typing import List

import pymysql

from db import db_session_auto_close


logger = logging.getLogger("app")


# ============================================================================================
# Employee Database Operations
# ============================================================================================


@db_session_auto_close
def create_employee(employee_data: dict, cursor: pymysql.cursors.DictCursor=None) -> int:
    """ 
    Create a new employee record
    :param employee_data: A dictionary containing employee information
    :param cursor: The database cursor
    :return: The ID of the newly created employee record
    """
    query = "INSERT INTO employee_list " \
    "(first_name, surname, position, department, phone_number, email, birth_date, status, description, register_time) " \
    "VALUES (%(first_name)s, %(surname)s, %(position)s, %(department)s, %(phone_number)s, %(email)s, %(birth_date)s, %(status)s, %(description)s, %(register_time)s)"
    cursor.execute(query, employee_data)
    return cursor.lastrowid


@db_session_auto_close
def get_employee(employee_id: int, cursor: pymysql.cursors.DictCursor=None) -> dict:
    """
    Get an employee record by ID
    :param employee_id: The ID of the employee
    :param cursor: The database cursor
    :return: A dictionary containing employee information
    """
    query = "SELECT * FROM employee_list WHERE id = %(employee_id)s"
    cursor.execute(query, {"employee_id": employee_id})
    return cursor.fetchone()


@db_session_auto_close
def get_employees_by_position(position_id: int, cursor: pymysql.cursors.DictCursor=None) -> List[dict]:
    """
    Get a list of employees by position ID
    :param position_id: The ID of the position
    :param cursor: The database cursor
    :return: A list of dictionaries containing employee information
    """
    query = "SELECT * FROM employee_list WHERE position = %(position)s"
    cursor.execute(query, {"position": position_id})
    return cursor.fetchall()


@db_session_auto_close
def get_employees_by_department(department_id: int, cursor: pymysql.cursors.DictCursor=None) -> List[dict]:
    """
    Get a list of employees by department ID
    :param department_id: The ID of the department
    :param cursor: The database cursor
    :return: A list of dictionaries containing employee information
    """
    query = "SELECT * FROM employee_list WHERE department = %(department)s"
    cursor.execute(query, {"department": department_id})
    return cursor.fetchall()


@db_session_auto_close
def inactivate_employee(employee_id: int, cursor: pymysql.cursors.DictCursor=None) -> None:
    """
    Inactivate an employee record by ID
    :param employee_id: The ID of the employee
    :param cursor: The database cursor
    """
    query = "UPDATE employee_list SET status = 0 WHERE id = %(employee_id)s"
    cursor.execute(query, {"employee_id": employee_id})


@db_session_auto_close
def promote_employee(employee_id: int, new_position: int, cursor: pymysql.cursors.DictCursor=None) -> None:
    """
    Promote an employee to a new position
    :param employee_id: The ID of the employee
    :param new_position: The new position ID
    :param cursor: The database cursor
    """
    query = "UPDATE employee_list SET position = %(new_position)s WHERE id = %(employee_id)s"
    cursor.execute(query, {"employee_id": employee_id, "new_position": new_position})


@db_session_auto_close
def transfer_employee(employee_id: int, new_department: int, cursor: pymysql.cursors.DictCursor=None) -> None:
    """
    Transfer an employee to a new department
    :param employee_id: The ID of the employee
    :param new_department: The new department ID
    :param cursor: The database cursor
    """
    query = "UPDATE employee_list SET department = %(new_department)s WHERE id = %(employee_id)s"
    cursor.execute(query, {"employee_id": employee_id, "new_department": new_department})


@db_session_auto_close
def get_employees(offset: int, limit: int, cursor: pymysql.cursors.DictCursor=None) -> List[dict]:
    """
    Get Employee's data by pagenation.
    :param offset: The offset of the page
    :param limit: The number of records to return
    """
    query = "SELECT * FROM employee_list LIMIT %(offset)s, %(limit)s"
    cursor.execute(query, {"offset": offset, "limit": limit})
    return cursor.fetchall()


@db_session_auto_close
def get_documents(offset: int, limit: int, cursor: pymysql.cursors.DictCursor=None) -> List[dict]:
    """
    Get Document's data by pagenation.
    :param offset: The offset of the page
    :param limit: The number of records to return
    """
    query = "SELECT * FROM document_approval LIMIT %(offset)s, %(limit)s"
    cursor.execute(query, {"offset": offset, "limit": limit})
    return cursor.fetchall()