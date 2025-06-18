from fastapi import status

from .base_HTTP_exception import BaseHTTPExceptions

class NotFound(BaseHTTPExceptions):
    decription = "Not Found"
    status_code = status.HTTP_404_NOT_FOUND
    exception_code = "API_RESOURCE_NOT_FOUND"

class UnprocessableContent(BaseHTTPExceptions):
    decription = "Error To Call The Request"
    status_code = status.HTTP_402_PAYMENT_REQUIRED
    exception_code = "API_SERVER_PAYMENT_REQUIRED"