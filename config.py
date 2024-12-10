from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    DB_HOST : str 
    DB_PORT : str 
    DB_USER : str 
    DB_PASS : str  
    DB_NAME : str 

    @property
    def db_url(self):
        #DSN
        #postgresql+asyncpg://user:password@localhost:5342/dbname
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    model_config = SettingsConfigDict(env_file=".env")


setting = Setting()


# from dotenv import dotenv_values

# config = dotenv_values(".env")

# DB_HOST=config.get("DB_HOST")
# DB_PORT=config.get("DB_PORT")
# DB_USER=config.get("DB_USER")
# DB_PASS=config.get("DB_PASS")
# DB_NAME=config.get("DB_NAME")
# DB_URL=f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# class settings:
#     DB_HOST=DB_HOST
#     DB_PORT=DB_PORT
#     DB_USER=DB_USER
#     DB_PASS=DB_PASS
#     DB_NAME=DB_NAME
#     DB_URL=DB_URL