from pydantic import BaseSettings


class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    SERVICE_NAME: str
    METRIC_NAME: str = "liveness_probe_unixtime"
    ENABLE_DEFAULT_PROMETHEUS_METRICS: bool = False

    class Config:
        env_prefix = "OPENMETRICS_LIVENESS_PROBE_"
        case_sensitive = True


settings = Settings()
