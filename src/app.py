"""
Simple python flask api mockup
:build date: 2025-08-14
:author: Jiwon Jeon
"""
import logging.config

from flask import Flask

from config import logging_config

# ============================================================================================
# Init Logging
# ============================================================================================
logging.config.dictConfig(logging_config)

# ============================================================================================
# Init Flask
# ============================================================================================
app = Flask(__name__)

# ============================================================================================
# Routes
# ============================================================================================
@app.route('/')
def hello_world():
    app.logger.info('Hello, World! endpoint was reached')
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
