from pydantic import BaseSettings


class Settings(BaseSettings):
    host: 'localhost'

    class Config:
        case_sensitive = True