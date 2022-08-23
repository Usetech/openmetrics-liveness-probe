from typing import Any, Iterable, Tuple

import pytest
from prometheus_client import Metric
from prometheus_client.openmetrics import parser
from requests.status_codes import codes

from openmetrics_liveness_probe import liveness_probe, settings
from openmetrics_liveness_probe.openmetrics_liveness_probe import (
    CONSUMER_LIVENESS_PROBE_UNIXTIME,
)


@pytest.fixture(params=["single", "multiprocess"])
def get_attrs_for_mock_metrics_server(request) -> Tuple[str, str]:
    if request.param == "single":
        url = f"http://{settings.HOST}:{settings.PORT}"
        text = """# HELP liveness_probe_unixtime Unixtime последней liveness probe \
            # TYPE liveness_probe_unixtime gauge \n# EOF\n"""
    if request.param == "multiprocess":
        url = f"http://{settings.HOST}:{settings.PORT + 1}"
        text = """# HELP liveness_probe_unixtime Multiprocess metric# TYPE \
            liveness_probe_unixtime gauge \n# EOF\n"""

    return url, f"{list(parser.text_string_to_metric_families(text))[0]}"


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
def get_liveness_probe_metric() -> Iterable[Metric]:
    liveness_probe()
    return CONSUMER_LIVENESS_PROBE_UNIXTIME.collect()


@pytest.fixture
def get_liveness_probe_metric_value(
    get_liveness_probe_metric: Iterable[Metric],
) -> float:
    return get_liveness_probe_metric[0].samples[0].value  # type: ignore
