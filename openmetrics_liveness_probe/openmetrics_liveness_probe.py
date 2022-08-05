from time import time

import prometheus_client
from prometheus_client.multiprocess import MultiProcessCollector

from .conf import settings

CONSUMER_LIVENESS_PROBE_UNIXTIME = prometheus_client.Gauge(
    settings.METRIC_NAME, "Unixtime последней liveness probe", ["service"]
)


def start_metrics_server(host=settings.HOST, port=settings.PORT):
    if not settings.ENABLED:
        return


    if not settings.ENABLE_DEFAULT_PROMETHEUS_METRICS:
        prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)
        prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
        prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
        
    if settings.PROMETHEUS_MULTIPROC_DIR:
        registry = prometheus_client.CollectorRegistry()
        MultiProcessCollector(registry=registry)

    registry = registry if settings.PROMETHEUS_MULTIPROC_DIR else prometheus_client.REGISTRY
    
    prometheus_client.start_http_server(addr=host, port=port, registry=registry)


def liveness_probe():
    if not settings.ENABLED:
        return

    CONSUMER_LIVENESS_PROBE_UNIXTIME.labels(service=settings.SERVICE_NAME).set(time())
