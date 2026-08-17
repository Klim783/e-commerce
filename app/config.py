from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	database_url : str = 'postgresql+psycopg2://shop_user:shop_pass@localhost:5499/shop'

	jwt_secret:str
	jwt_algorithm:str = 'HS256'
	jwt_expire_minutes:int = 60


	model_config = SettingsConfigDict(env_file = '.env', extra ='ignore')

settings = Settings()