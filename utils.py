from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    database_config: SecretStr
    port_redis: SecretStr
    host_redis: SecretStr
    psw_redis: SecretStr

    class Config:
        env_file = '.env'

        env_file_encoding = 'utf-8'


config = Settings()

port_redis = config.port_redis.get_secret_value()
host_redis = config.host_redis.get_secret_value()
psw_redis = config.psw_redis.get_secret_value()

