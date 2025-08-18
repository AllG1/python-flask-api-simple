""" Load Environment Variables """

import os
import sys
import typing

ENV_TYPE: typing.Any
DOTENV_PATH: typing.Any
ENV_FILES: typing.Any

CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))


def set_default_env():
    # set default global variables
    global ENV_TYPE, DOTENV_PATH, ENV_FILES

    ENV_TYPE = os.getenv("APP_ENV_TYPE", "").upper()  # env mode (ex - dev, test, live)
    DOTENV_PATH = os.path.join(CONFIG_DIR, "data")

    if not ENV_TYPE:
        sys.stderr.write("You must set environment variable 'APP_ENV_TYPE' before running API")
        sys.exit(1)

    # set default environment .env files
    env_files = list()
    if ENV_TYPE == "DEV":
        env_files.append(os.path.join(DOTENV_PATH, 'dev.env'))
        env_files.append(os.path.join(DOTENV_PATH, 'dev.credential.env'))
    elif ENV_TYPE == "TEST":
        env_files.append(os.path.join(DOTENV_PATH, 'test.env'))
        env_files.append(os.path.join(DOTENV_PATH, 'test.credential.env'))
    elif ENV_TYPE == "LIVE":
        env_files.append(os.path.join(DOTENV_PATH, 'live.env'))
        env_files.append(os.path.join(DOTENV_PATH, 'live.credential.env'))

    ENV_FILES = env_files


def get_env_type():
    global ENV_TYPE
    return ENV_TYPE


def get_dotenv_path():
    global DOTENV_PATH
    return DOTENV_PATH


def get_env_files():
    global ENV_FILES
    return ENV_FILES
