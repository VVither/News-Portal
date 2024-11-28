import logging

class RequestOrServerErrorFilter(logging.Filter):
    def filter(self, record):
        return record.name == 'django.request' or record.name == 'django.server'