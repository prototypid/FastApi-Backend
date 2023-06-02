from pydantic import BaseSettings


class Settings(BaseSettings):
    database_name: str = 'Test'
    database_hostname: str = 'localhost'
    database_username: str
    database_password: int
    database_port: str = 5432
    algorithm: str = 'HS256'
    secret_key: str
    access_token_expire_minutes: int = 30

    class Config:
        env_file = '.env'


settings = Settings()

