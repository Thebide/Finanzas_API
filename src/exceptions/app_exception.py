from typing import Optional

class BaseAppExceptions(Exception):
    default_message: str = "UNKNOWN ERROR"

    def __init__(self, message: Optional[str]):
        self.message = message or self.default_message
        super().__init__(self.message)

class NotFoundError(BaseAppExceptions):
    default_message = "No se encontro el recurso."