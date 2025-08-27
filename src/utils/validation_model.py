# ==============================================================================================
# Response Models
# ==============================================================================================

import datetime
import logging

from pydantic import BaseModel, field_validator


logger = logging.getLogger("app")


class EmployeeSearchResponse(BaseModel):
    id: int
    first_name: str
    surname: str = ""
    position: str
    department: str
    phone_number: str
    email: str
    birth_date: str = "0000-00-00"
    status: str
    description: str = ""
    register_time: str = "0000-00-00 00:00:00"

    @field_validator("position", mode="before")
    def set_position(cls, v) -> str:
        positions = {0: "Employee", 1: "Manager", 2: "Director"}
        try:
            if isinstance(v, int):
                return positions[v]
            elif isinstance(v, str) and v in positions.values():
                return v
        except Exception as e:
            logger.exception("Not valid position")
        raise ValueError("Invalid position")

    @field_validator("department", mode="before")
    def set_department(cls, v) -> str:
        departments = {0: "hr", 1: "it", 2: "sales"}
        try:
            if isinstance(v, int):
                return departments[v]
            elif isinstance(v, str) and v.lower() in departments.values():
                return v
        except Exception as e:
            logger.exception("Not valid department")
        raise ValueError("Invalid department")

    @field_validator("status", mode="before")
    def set_status(cls, v) -> str:
        statuses = {0: "inactive", 1: "active"}
        try:
            if isinstance(v, int):
                return statuses[v]
            elif isinstance(v, str) and v.lower() in statuses.values():
                return v
        except Exception as e:
            logger.exception("Not valid status")
        raise ValueError("Invalid status")

    @field_validator("birth_date", mode="before")
    def set_birth_date(cls, v) -> str:
        try:
            # 1) make datetime to string
            if isinstance(v, datetime.datetime) or isinstance(v, datetime.date):
                return v.strftime("%Y-%m-%d")
            # 2) check string is valid format (Y-m-d)
            if isinstance(v, str):
                try:
                    datetime.datetime.strptime(v, "%Y-%m-%d")
                    return v
                except ValueError:
                    pass
        except Exception as e:
            logger.exception("Not valid birth date")
        raise ValueError("Invalid birth date")

    @field_validator("register_time", mode="before")
    def set_register_time(cls, v) -> str:
        try:
            if isinstance(v, datetime.datetime) or isinstance(v, datetime.date):
                return v.strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(v, str):
                try:
                    datetime.datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
                    return v
                except ValueError:
                    pass
        except Exception as e:
            logger.exception("Not valid register time")
        raise ValueError("Invalid register time")
    

class DocumentApprovalResponse(BaseModel):
    id: int
    issuer: int
    assignee: int
    status: str
    dayoff_start_date: str
    dayoff_end_date: str
    reason: str = ""
    created_at: str = "0000-00-00"
    updated_at: str = "0000-00-00"

    @field_validator("status", mode="before")
    def set_status(cls, v) -> str:
        statuses = {0: "Pending", 1: "Approved", 2: "Rejected"}
        try:
            if isinstance(v, int):
                return statuses[v]
            elif isinstance(v, str) and v.capitalize() in statuses.values():
                return v.capitalize()
        except Exception as e:
            logger.exception("Not valid status")
        raise ValueError("Invalid status")

    @field_validator("dayoff_start_date", mode="before")
    def set_start_date(cls, v) -> str:
        try:
            if isinstance(v, datetime.datetime) or isinstance(v, datetime.date):
                return v.strftime("%Y-%m-%d")
            if isinstance(v, str):
                try:
                    datetime.datetime.strptime(v, "%Y-%m-%d")
                    return v
                except ValueError:
                    pass
        except Exception as e:
            logger.exception("Not valid dayoff_start_date")
        raise ValueError("Invalid dayoff_start_date")

    @field_validator("dayoff_end_date", mode="before")
    def set_end_date(cls, v) -> str:
        try:
            if isinstance(v, datetime.datetime) or isinstance(v, datetime.date):
                return v.strftime("%Y-%m-%d")
            if isinstance(v, str):
                try:
                    datetime.datetime.strptime(v, "%Y-%m-%d")
                    return v
                except ValueError:
                    pass
        except Exception as e:
            logger.exception("Not valid dayoff_end_date")
        raise ValueError("Invalid dayoff_end_date")

    @field_validator("created_at", "updated_at", mode="before")
    def set_datetime(cls, v) -> str:
        try:
            if isinstance(v, datetime.datetime) or isinstance(v, datetime.date):
                return v.strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(v, str):
                try:
                    datetime.datetime.strptime(v, "%Y-%m-%d")
                    return v
                except ValueError:
                    pass
        except Exception as e:
            logger.exception("Not valid datetime")
        raise ValueError("Invalid datetime")
