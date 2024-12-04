import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    email: str
    password: str
    destination: str

    class Config:
        env_file = ".env"


# Check if env file is there
if not os.path.exists(".env"):
    raise FileNotFoundError("Environment file is missing.")

settings = Settings()