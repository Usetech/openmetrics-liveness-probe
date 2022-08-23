from typing import Any, Callable

import requests
from requests.status_codes import codes

from openmetrics_liveness_probe import __version__


def test_version() -> None:
    assert __version__ == "0.1.6"


def test_start_metrics_server(
    mock_metrics_server: Callable, get_attrs_for_mock_metrics_server: Any
) -> None:
    url, text = get_attrs_for_mock_metrics_server
    response = requests.get(url=url)
    response.raise_for_status()
    assert response.text == text
    assert response.status_code == codes.ok


def test_liveness_probe(
    get_liveness_probe_metric: Any, get_liveness_probe_metric_value: Any
) -> None:
    assert (
        get_liveness_probe_metric[0].samples[0].value == get_liveness_probe_metric_value
    )
