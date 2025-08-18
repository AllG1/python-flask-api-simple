""" Main configuration loading for loading dotenv settings by environment setting """

from pydantic_settings import BaseSettings, SettingsConfigDict

from config.env import get_env_files
from config.rdb import RDBSettings


# ============================================================================================
# Configuration Class
# ============================================================================================

class Settings(BaseSettings):
    model_config = SettingsConfigDict(  # dummy setting for init
        env_file="config/data/test.env",
        env_file_encoding="utf-8", 
        extra="ignore",
        env_nested_delimiter="__",
        env_prefix="APP__"
    )
    
    rdb: RDBSettings = RDBSettings()


# ============================================================================================
# Global Variables
# ============================================================================================


settings: Settings


# ============================================================================================
# Set Settings
# ============================================================================================


def set_settings() -> Settings:
    global settings

    settings = Settings(_env_file=get_env_files(), _env_file_encoding="utf-8",
                        extra="ignore", env_nested_delimiter="__", env_prefix="APP__")

    return settings


def get_settings() -> Settings:
    global settings
    return settings
