from typing import Optional

from pydantic import __version__ as __pydantic_version__

if __pydantic_version__[0] == "2":
    from pydantic.v1 import BaseSettings
else:
    from pydantic import BaseSettings  # type: ignore


class Settings(BaseSettings):
    ENABLED: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    SERVICE_NAME: str = "example"
    METRIC_NAME: str = "liveness_probe_unixtime"
    ENABLE_DEFAULT_PROMETHEUS_METRICS: bool = False
    PROMETHEUS_MULTIPROC_DIR: Optional[str] = None

    class Config:
        env_prefix = "OPENMETRICS_LIVENESS_PROBE_"
        case_sensitive = True
        fields = {
            "PROMETHEUS_MULTIPROC_DIR": {
                "env": "PROMETHEUS_MULTIPROC_DIR",
            },
        }


settings = Settings()
