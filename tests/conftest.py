import os

import pytest
from prometheus_client import (
    GC_COLLECTOR,
    PLATFORM_COLLECTOR,
    PROCESS_COLLECTOR,
    REGISTRY,
    CollectorRegistry,
    start_http_server,
)
from prometheus_client.multiprocess import MultiProcessCollector

from openmetrics_liveness_probe import settings


@pytest.fixture
def launch_metrics_server() -> None:
    REGISTRY.unregister(PROCESS_COLLECTOR)
    REGISTRY.unregister(PLATFORM_COLLECTOR)
    REGISTRY.unregister(GC_COLLECTOR)
    return start_http_server(addr=settings.HOST, port=settings.PORT, registry=REGISTRY)


@pytest.fixture
def launch_multiprocess_mode_metrics_server(port: int = settings.PORT + 1) -> None:
    os.environ.setdefault("PROMETHEUS_MULTIPROC_DIR", "/tmp")
    registry = CollectorRegistry()
    MultiProcessCollector(registry=registry)
    return start_http_server(addr=settings.HOST, port=port, registry=registry)
