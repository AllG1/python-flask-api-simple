""" APIs which shows employee data """

import logging

from flask import Blueprint, jsonify
from response_codes import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from db import get_employees, get_documents
from utils import make_response_form, EmployeeSearchResponse, DocumentSearchResponse


data_bp = Blueprint('data', __name__, url_prefix='/data')
logger = logging.getLogger("app")


# ==============================================================================================
# APIs
# ==============================================================================================


@data_bp.route("/employee/<int:offset>", methods=["GET"])
def get_employee_list(offset: int):
    """
    Get a list of employees with pagination.
    :param offset: offset of the page
    """
    limit = 10

    try:
        # get employee list
        employees = get_employees(offset, limit)

        # make data return format
        v_employees = list(map(lambda x: EmployeeSearchResponse(**x).model_dump(), employees))

        # return validated data
        return make_response_form(data=v_employees, http_status=HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching employee list: {e}")
        return make_response_form(http_status=HTTP_500_INTERNAL_SERVER_ERROR)


@data_bp.route("/documents/<int:offset>", methods=["GET"])
def get_document_list(offset: int):
    """
    Get a list of documents with pagination.
    :param offset: offset of the page
    """
    limit = 10

    try:
        # get document list
        documents = get_documents(offset, limit)

        # make data return format
        v_documents = list(map(lambda x: DocumentSearchResponse(**x).model_dump(), documents))
        ret_dict = {"documents": v_documents, "offset": offset, "show_next_button": len(v_documents) == limit}

        # return validated data
        return make_response_form(data=ret_dict, http_status=HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching document list: {e}")
        return make_response_form(http_status=HTTP_500_INTERNAL_SERVER_ERROR)
