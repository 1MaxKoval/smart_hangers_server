from rest_framework.exceptions import APIException
from rest_framework import status


class BaseHangerException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = {'error': 'Server Error'}


class HangerAppException(BaseHangerException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = {'error': 'Error occurred while contacting the Hanger API'}
