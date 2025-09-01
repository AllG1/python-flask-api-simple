""" Global variables for RDB connection """

from functools import wraps
import logging
import os
import time
import pymysql
from dbutils.pooled_db import PooledDB

from config import Settings


logger = logging.getLogger("app")


# ============================================================================================
# Global variables for RDB connection
# ============================================================================================


DB_POOL: PooledDB = None


# ============================================================================================
# util functions
# ============================================================================================
def make_db_pool(settings: Settings) -> PooledDB:
    """ Make database connection pool """
    connection_set = False
    for i in range(5):
        try:
            # connect database
            logger.info(f"[PID:{os.getpid()}] Creating database connection pool ({settings.rdb.host}:{settings.rdb.port}|{settings.rdb.database})")
            DB_POOL = PooledDB(
                creator=pymysql,
                maxconnections=5,
                mincached=2,
                maxcached=5,
                blocking=True,
                maxusage=None,
                setsession=[],
                host=settings.rdb.host,
                port=settings.rdb.port,
                user=settings.rdb.user,
                password=settings.rdb.password,
                database=settings.rdb.database,
                charset='utf8mb4',
                autocommit=True
            )
            logger.info(f"[PID:{os.getpid()}] Database connection pool created successfully ({settings.rdb.host}:{settings.rdb.port}|{settings.rdb.database})")
            connection_set = True
            break
        except Exception as e:
            logger.critical(f"[PID:{os.getpid()}] Failed to create database connection pool: {e}")

            # wait for loading of mysql container
            logger.info(f"[PID:{os.getpid()}] Retrying to connect to the database in 10 seconds...")
            time.sleep(10)
        
    if not connection_set:
        logger.critical(f"[PID:{os.getpid()}] Exiting due to database connection failure.")
        exit(1)

    return DB_POOL


# ============================================================================================
# Setting functions
# ============================================================================================

def set_db_pool(settings: Settings) -> PooledDB:
    """ Set database connection pool """
    global DB_POOL

    DB_POOL = make_db_pool(settings)

    return DB_POOL


# ============================================================================================
# Getter functions
# ============================================================================================

def get_db_pool() -> PooledDB:
    """ Get database connection pool """
    return DB_POOL


# ==============================================================================================
# Decorator for DB management
# ==============================================================================================


def db_session_auto_close(func):
    """
    Decorator to manage database sessions for a function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        db_pool = get_db_pool()  # load pre-defined database connection pool
        db_conn = db_pool.connection()  # get a connection from the pool
        query_result = None

        try:
            with db_conn.cursor(pymysql.cursors.DictCursor) as cursor:
                query_result = func(*args, **kwargs, cursor=cursor)  # execute the function with the cursor
        except Exception as e:
            logging.exception(f"Error in database operation: {e}")
        finally:
            cursor.close()
            db_conn.close()  # ensure the connection is closed
        
        return query_result

    return wrapper
