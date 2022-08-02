from time import time

import prometheus_client

from .conf import settings

METRIC_NAME = f"{settings.SERVICE_NAME}_{settings.NAME_POSTFIX}"

CONSUMER_LIVENESS_PROBE_UNIXTIME = prometheus_client.Gauge(
    METRIC_NAME, "Unixtime последней liveness probe"
)


def start_metrics_server(host=settings.HOST, port=settings.PORT):
    prometheus_client.start_http_server(addr=host, port=port)


def liveness_probe():
    CONSUMER_LIVENESS_PROBE_UNIXTIME.set(time())
