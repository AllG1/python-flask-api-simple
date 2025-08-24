""" Logging Configuration """
# https://docs.python.org/3/library/logging.config.html

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d][%(funcName)s] %(message)s'
        },
        'verbose': {
            'format': '[%(asctime)s][%(name)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'DEBUG'
        },
        'logfile': {
            'class': 'logging.FileHandler',
            'filename': './logs/app.log',
            'formatter': 'verbose',
            'level': 'INFO'
        }
    },
    'loggers': {
        'app': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}