import logging
import time

import pytest
import requests

from tests.mock_server import MockPetstoreServer

logger = logging.getLogger(__name__)


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    try:
        from tests.screenshot_report import generate_report, capture_report_screenshot
        if generate_report():
            capture_report_screenshot(timeout=15)
    except Exception as e:
        logger.warning("Post-run report/screenshot failed: %s", e)


@pytest.fixture(scope="session")
def mock_petstore():
    from config.settings import BASE_URL

    if "localhost" not in BASE_URL and "127.0.0.1" not in BASE_URL:
        deadline = time.time() + 15
        while time.time() < deadline:
            try:
                resp = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": "available"}, timeout=3)
                if resp.status_code < 500:
                    logger.info("Real Petstore is reachable at %s", BASE_URL)
                    return
            except requests.ConnectionError:
                pass
            time.sleep(2)

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
