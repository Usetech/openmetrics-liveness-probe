from pydantic import BaseSettings


class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    SERVICE_NAME: str
    NAME_POSTFIX: str = "liveness_probe_unixtime"

    class Config:
        env_prefix = "OPENMETRICS_LIVENESS_PROBE_"
        case_sensitive = True


settings = Settings()
