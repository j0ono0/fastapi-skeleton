from pydantic import BaseSettings
 


class Settings(BaseSettings):
    production_env: bool 
    database_url: str
    allowed_hosts: list

    class Config:
        env_file = 'settings.env'
        env_file_encoding = 'utf-8'