from time import time

import prometheus_client
from prometheus_client.multiprocess import MultiProcessCollector

from .conf import settings

CONSUMER_LIVENESS_PROBE_UNIXTIME = prometheus_client.Gauge(
    settings.METRIC_NAME, "Unixtime последней liveness probe", ["service", "version"]
)


def start_metrics_server(host: str = settings.HOST, port: int = settings.PORT) -> None:
    """Starts the metrics server from prometheus_client at http://{{host}}:{{port}}.
       The server starts multiprocess mode, if value of environment variable
       PROMETHEUS_MULTIPROC_DIR is not None.

    Args:
        host (str, optional): IP address. Defaults to settings.HOST.
        port (int, optional): Port number. Defaults to settings.PORT.
    """
    if not settings.ENABLED:
        return

    registry = prometheus_client.REGISTRY

    if not settings.ENABLE_DEFAULT_PROMETHEUS_METRICS:
        prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)
        prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
        prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)

    if settings.PROMETHEUS_MULTIPROC_DIR:
        registry = prometheus_client.CollectorRegistry()
        MultiProcessCollector(registry=registry)

    prometheus_client.start_http_server(addr=host, port=port, registry=registry)


def liveness_probe(version="undefined") -> None:
    """Sets the liveness probe metric to the metrics server."""
    if not settings.ENABLED:
        return

    CONSUMER_LIVENESS_PROBE_UNIXTIME.labels(
        service=settings.SERVICE_NAME, version=version
    ).set(time())
