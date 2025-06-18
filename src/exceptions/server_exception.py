from fastapi import status

from .base_HTTP_exception import BaseHTTPExceptions


class InternalServerError(BaseHTTPExceptions):
    decription = "Unhandled error"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    exception_code = "API_UNHANDLE_ERROR"

class NotImplemented(BaseHTTPExceptions):
    decription = "Servise Is Not Implemented"
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    exception_code = "API_END_POINT_NOT_IMPLEMENTED"

