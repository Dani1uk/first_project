from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    DB_HOST : str 
    DB_PORT : str 
    DB_USER : str 
    DB_PASS : str  
    DB_NAME : str 

    @property
    def Data_base_url_acyncpg(self):
        #postgresql+asyncpg: //user: password@localhost/dbname
        return f"postgresql+asyncpg: //{self.DB_USER}: {self.DB_PASS}@{self.DB_HOST}/{self.DB_NAME}"
    
    model_config = SettingsConfigDict(env_file=".env")


setting = Setting()