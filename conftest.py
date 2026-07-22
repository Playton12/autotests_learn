import logging
import time

import pytest
import requests

from utils.mock_server import MockPetstoreServer

logger = logging.getLogger(__name__)

_PETSTORE_CONNECT_TIMEOUT = 15
_PETSTORE_POLL_INTERVAL = 2
_PETSTORE_REQUEST_TIMEOUT = 3


def _is_remote_url(url: str) -> bool:
    return "localhost" not in url and "127.0.0.1" not in url


def _is_petstore_reachable(base_url: str) -> bool:
    deadline = time.time() + _PETSTORE_CONNECT_TIMEOUT
    while time.time() < deadline:
        try:
            resp = requests.get(
                f"{base_url}/pet/findByStatus",
                params={"status": "available"},
                timeout=_PETSTORE_REQUEST_TIMEOUT,
            )
            if resp.status_code < 500:
                return True
        except requests.ConnectionError:
            pass
        time.sleep(_PETSTORE_POLL_INTERVAL)
    return False


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    try:
        from screenshot_report import generate_report, capture_report_screenshot
        if generate_report():
            capture_report_screenshot()
    except Exception as e:
        logger.warning("Post-run report/screenshot failed: %s", e)


@pytest.fixture(scope="session")
def mock_petstore():
    from config.settings import BASE_URL

    if _is_remote_url(BASE_URL) and _is_petstore_reachable(BASE_URL):
        logger.info("Real Petstore is reachable at %s", BASE_URL)
        return

    logger.info("Starting mock Petstore server ...")
    server = MockPetstoreServer()
    time.sleep(0.5)
    logger.info("Mock Petstore running at %s", server.url)
    yield server
    server.stop()


@pytest.fixture(scope="session")
def base_url(mock_petstore):
    if mock_petstore:
        return mock_petstore.url
    from config.settings import BASE_URL
    return BASE_URL
