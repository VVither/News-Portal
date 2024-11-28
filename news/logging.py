import logging
import logging.config
import os
from django.conf import settings
from django.core.mail import send_mail
from django.utils.log import RequireDebugFalse, RequireDebugTrue


def configure_logging():
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'console': {
                'format': '%(asctime)s - %(levelname)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'verbose': {
                'format': '%(asctime)s - %(pathname)s - %(levelname)s - %(module)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'general': {
                'format': '%(asctime)s - %(levelname)s - %(module)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'errors': {
                'format': '%(asctime)s - %(levelname)s - %(message)s - %(pathname)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'security': {
                'format': '%(asctime)s - %(levelname)s - %(module)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'mail': {
                'format': '%(asctime)s - %(levelname)s - %(message)s - %(pathname)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'console',
                'filters': ['require_debug_true'],
            },
            'general': {
                'class': 'logging.FileHandler',
                'filename': os.path.join(settings.BASE_DIR, 'logs', 'general.log'),
                'level': 'INFO',
                'formatter': 'general',
                'filters': ['require_debug_false'],
            },
            'errors': {
                'class': 'logging.FileHandler',
                'filename': os.path.join(settings.BASE_DIR, 'logs', 'errors.log'),
                'level': 'ERROR',
                'formatter': 'errors',
                'filters': ['require_debug_false'],
            },
            'security': {
                'class': 'logging.FileHandler',
                'filename': os.path.join(settings.BASE_DIR, 'logs', 'security.log'),
                'level': 'INFO',
                'formatter': 'security',
                'filters': ['require_debug_false'],
            },
            'mail_handler': {
                'class': 'logging.handlers.SMTPHandler',
                'mailhost': settings.EMAIL_HOST,
                'fromaddr': settings.EMAIL_HOST_USER,
                'toaddrs': settings.ADMINS,
                'subject': 'Django Application Error',
                'level': 'ERROR',
                'formatter': 'mail',
                'filters': ['require_debug_false', 'request_or_server_errors'],
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'general', 'errors'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['errors', 'mail_handler'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django.server': {
                'handlers': ['errors', 'mail_handler'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django.template': {
                'handlers': ['errors'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django.db.backends': {
                'handlers': ['errors'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django.security': {
                'handlers': ['security'],
                'level': 'INFO',
                'propagate': False,
            },
             'allauth': { # Добавлено для allauth
                'handlers': ['general', 'errors'],
                'level': 'INFO',
                'propagate': False,
            },
        },
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },
            'request_or_server_errors': {
                '()': 'News_Portal.utils.RequestOrServerErrorFilter',
            },
        }
    }

    logging.config.dictConfig(LOGGING)