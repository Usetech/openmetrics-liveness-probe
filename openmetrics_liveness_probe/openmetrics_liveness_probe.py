from time import time

import prometheus_client

from .conf import settings


CONSUMER_LIVENESS_PROBE_UNIXTIME = prometheus_client.Gauge(
    settings.METRIC_NAME, "Unixtime последней liveness probe", ["service"]
)


def start_metrics_server(host=settings.HOST, port=settings.PORT):
    prometheus_client.start_http_server(addr=host, port=port)


def liveness_probe():
    CONSUMER_LIVENESS_PROBE_UNIXTIME.labels(service=settings.SERVICE_NAME).set(time())
