from typing import ClassVar
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API
    PORT : int = 8000
    DEV : bool = True

    #logs
    LOG_DIR: str = "logs"
    DEBUG: bool = False

    #Database
    PATH_DATA: ClassVar[str] = "database\\fakedb.json"
    DB_CONN: str


    #config inner class
    class Config():
        env_file = ".env"