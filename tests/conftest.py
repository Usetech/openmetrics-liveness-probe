import os
from typing import Any, Iterable, Tuple

import pytest
from prometheus_client import (
    GC_COLLECTOR,
    PLATFORM_COLLECTOR,
    PROCESS_COLLECTOR,
    REGISTRY,
    CollectorRegistry,
    Metric,
)
from prometheus_client.exposition import generate_latest
from prometheus_client.multiprocess import MultiProcessCollector
from prometheus_client.openmetrics import parser
from requests.status_codes import codes

from openmetrics_liveness_probe import liveness_probe, settings
from openmetrics_liveness_probe.openmetrics_liveness_probe import (
    CONSUMER_LIVENESS_PROBE_UNIXTIME,
)


@pytest.fixture(params=["single", "multiprocess"])
def get_attrs_for_mock_metrics_server(request) -> Tuple[str, str]:
    if request.param == "single":
        try:
            REGISTRY.unregister(PROCESS_COLLECTOR)
            REGISTRY.unregister(PLATFORM_COLLECTOR)
            REGISTRY.unregister(GC_COLLECTOR)
        except KeyError:
            pass
        url = f"http://{settings.HOST}:{settings.PORT}"

    if request.param == "multiprocess":
        os.environ.setdefault("PROMETHEUS_MULTIPROC_DIR", "/tmp")
        registry = CollectorRegistry()
        MultiProcessCollector(registry=registry)
        url = f"http://{settings.HOST}:{settings.PORT + 1}"

    return url, generate_latest().decode("utf-8")


@pytest.fixture(params=["single", "multiprocess"])
def mock_metrics_server(
    requests_mock: Any, get_attrs_for_mock_metrics_server: Any
) -> Any:
    url, text = get_attrs_for_mock_metrics_server
    return requests_mock.get(
        url=url,
        text=text,
        status_code=codes.ok,
    )


@pytest.fixture
def get_liveness_probe_metric_enabled() -> Iterable[Metric]:
    liveness_probe()
    return CONSUMER_LIVENESS_PROBE_UNIXTIME.collect()


@pytest.fixture
def get_liveness_probe_metric_disabled() -> Iterable[Metric]:
    settings.ENABLED = False
    liveness_probe()
    return CONSUMER_LIVENESS_PROBE_UNIXTIME.collect()


@pytest.fixture
def get_liveness_probe_metric_from_prometheus_client() -> Iterable[Metric]:
    text = f"{generate_latest().decode('utf-8')}# EOF"
    return list(parser.text_string_to_metric_families(text))
