""" RDB Settings """

from pydantic import Field, BaseModel, field_validator


# =========================================================================================
# RDB Server Setting
# =========================================================================================

class RDBSettings(BaseModel):
    host: str = Field(default="localhost", description="RDB Host")
    port: int = Field(default=3306, description="RDB Port")
    user: str = Field(default="root", description="RDB User")
    password: str = Field(default="", description="RDB Password")
    database: str = Field(default="test", description="RDB Database")

    @field_validator("host", "user", "password", "database")
    def not_empty(cls, v):
        if not v:
            raise ValueError("This field cannot be empty.")
        return v

    @field_validator("port")
    def valid_port(cls, v):
        if not (0 < v < 65536):
            raise ValueError("Port must be between 1 and 65535.")
        return v
