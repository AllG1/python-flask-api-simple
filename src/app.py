"""
Simple python flask api mockup
:build date: 2025-08-14
:author: Jiwon Jeon
"""
import logging.config

from flask import Flask

from config import logging_config, set_default_env, set_settings, get_settings

from db.init_pool import set_db_pool
from views import search_bp, manage_bp

# ============================================================================================
# Init Logging
# ============================================================================================
logging.config.dictConfig(logging_config)

# ============================================================================================
# Set Config
# ============================================================================================
set_default_env()
set_settings()

# ===========================================================================================
# Init Variables
# ============================================================================================
set_db_pool(get_settings())

# ============================================================================================
# Init Flask
# ============================================================================================
app = Flask(__name__)

# ============================================================================================
# Register Routers
# ============================================================================================
app.register_blueprint(search_bp)
app.register_blueprint(manage_bp)

# ============================================================================================
# Basic Routes
# ============================================================================================
@app.route('/')
def hello_world():
    app.logger.info('Hello, World! endpoint was reached')
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
