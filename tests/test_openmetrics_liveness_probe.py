from typing import Callable

import pytest
import requests

from openmetrics_liveness_probe import __version__, liveness_probe, settings


def test_version() -> None:
    assert __version__ == "0.1.6"


def test_start_metrics_server(launch_metrics_server: Callable) -> None:
    response = requests.get(url=f"http://{settings.HOST}:{settings.PORT}")
    response.raise_for_status()
    assert response.status_code == requests.status_codes.codes.ok
    assert "Unixtime последней liveness probe" in response.text


def test_start_multiprocess_mode_metrics_server(
    launch_multiprocess_mode_metrics_server: Callable,
) -> None:
    response = requests.get(url=f"http://{settings.HOST}:{settings.PORT + 1}")
    response.raise_for_status()
    liveness_probe()
    assert response.status_code == requests.status_codes.codes.ok
    assert "Multiprocess metric" in response.text


@pytest.mark.parametrize(
    "url",
    [
        f"http://{settings.HOST}:{settings.PORT}",
        f"http://{settings.HOST}:{settings.PORT + 1}",
    ],
)
def test_liveness_probe(url: str) -> None:
    liveness_probe()
    response = requests.get(url=url)
    response.raise_for_status()
    _probe = response.text.split("\n")[2]
    assert _probe.split(" ")[1] != " "
