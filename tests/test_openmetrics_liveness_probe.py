from typing import Any, Callable

import requests
from prometheus_client import Gauge
from requests.status_codes import codes

from openmetrics_liveness_probe import __version__
from openmetrics_liveness_probe.openmetrics_liveness_probe import (
    CONSUMER_LIVENESS_PROBE_UNIXTIME,
)


def test_version() -> None:
    assert __version__ == "0.2.0"


def test_type_of_consumer_liveness_probe_unixtime() -> None:
    assert isinstance(CONSUMER_LIVENESS_PROBE_UNIXTIME, Gauge) is True


def test_start_metrics_server(
    mock_metrics_server: Callable, get_attrs_for_mock_metrics_server: Any
) -> None:
    url, text = get_attrs_for_mock_metrics_server
    response = requests.get(url=url)
    response.raise_for_status()
    assert response.text == text
    assert response.status_code == codes.ok


def test_liveness_probe_enabled(
    get_liveness_probe_metric_enabled: Any,
    get_liveness_probe_metric_from_prometheus_client: Any,
) -> None:
    assert (
        get_liveness_probe_metric_enabled[0].samples[0].value
        == get_liveness_probe_metric_from_prometheus_client[0].samples[0].value
    )
    assert (
        get_liveness_probe_metric_enabled[0].samples[0].labels["service"]
        == get_liveness_probe_metric_from_prometheus_client[0]
        .samples[0]
        .labels["service"]
    )


def test_liveness_probe_disabled(
    get_liveness_probe_metric_disabled: Any,
    get_liveness_probe_metric_from_prometheus_client: Any,
) -> None:
    assert (
        get_liveness_probe_metric_disabled[0].samples
        == get_liveness_probe_metric_from_prometheus_client[0].samples
    )
