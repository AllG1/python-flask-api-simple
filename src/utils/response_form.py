""" 
Functions for making API response.
We use this functions for keeping form of API response consistent.
Status codes are depends on https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status
Thanks for https://pypi.org/project/http-response-codes/.
"""
from response_codes import HTTP_200_OK, HTTP_SUCCESS
from typing import Tuple


def make_response_form(data=None, http_status = HTTP_200_OK, description: str = '') -> Tuple[dict, int]:
    """
    Make general API response form.
    :param data: return data from API process
    :param http_status: (response_codes) HTTP status code
    :return: (response_dict, http_status_code)
    """

    if http_status.status_code in HTTP_SUCCESS:
        return {"status": http_status.status_code, "response": data}, http_status.status_code
    else:  # not 200 code
        error_response = {
            "error": {
                "code": http_status.status_code,
                "message": http_status.message,
                "description": description or http_status.description
            }
        }
        return {"status": http_status.status_code, "response": error_response}, http_status.status_code

