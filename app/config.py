from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    database_hostname:str
    database_username:str
    database_name:str
    database_password:str
    database_port:str
    secret_key: str 
    algorithm :str
    access_token_expire_minutes:int

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.database_username}:{self.database_password}@{self.database_hostname}:{self.database_port}/{self.database_name}"

    # class Config:
    #     env_file=".env"
settings=Settings()     