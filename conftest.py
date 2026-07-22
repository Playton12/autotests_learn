import logging
import shutil
import time
from pathlib import Path

import pytest
import requests

from petstore.mock_server import MockPetstoreServer

logger = logging.getLogger(__name__)

_PETSTORE_CONNECT_TIMEOUT = 15
_PETSTORE_POLL_INTERVAL = 2
_PETSTORE_REQUEST_TIMEOUT = 3

_collected_api = False
_collected_ui = False


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
def pytest_collection_modifyitems(items):
    global _collected_api, _collected_ui
    for item in items:
        node = item.nodeid
        if "petstore/tests/" in node:
            _collected_api = True
        elif "saucedemo/tests/" in node:
            _collected_ui = True


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    try:
        from utils.screenshot_report import (
            generate_report,
            capture_report_screenshot,
            filter_allure_results,
        )

        has_api = _collected_api
        has_ui = _collected_ui
        has_both = has_api and has_ui

        results_dir = "allure-results"

        if has_both:
            report_dir = "allure-report"
            if generate_report(results_dir, report_dir):
                capture_report_screenshot(report_dir, output_name="all")
            _generate_filtered_screenshot(
                results_dir, filter_allure_results, generate_report,
                capture_report_screenshot, "petstore/tests", "api", "allure-report-api",
            )
            _generate_filtered_screenshot(
                results_dir, filter_allure_results, generate_report,
                capture_report_screenshot, "saucedemo/tests", "ui", "allure-report-ui",
            )
        elif has_api:
            if generate_report(results_dir, "allure-report"):
                capture_report_screenshot("allure-report", output_name="api")
        elif has_ui:
            if generate_report(results_dir, "allure-report"):
                capture_report_screenshot("allure-report", output_name="ui")
        else:
            if generate_report(results_dir, "allure-report"):
                capture_report_screenshot("allure-report", output_name="report")

    except Exception as e:
        logger.warning("Post-run report/screenshot failed: %s", e)


def _generate_filtered_screenshot(
    results_dir, filter_fn, generate_fn, screenshot_fn,
    test_dir_prefix, output_name, report_dir,
):
    tmp_results = f"allure-results-{output_name}"
    try:
        if filter_fn(results_dir, tmp_results, test_dir_prefix):
            if generate_fn(tmp_results, report_dir):
                screenshot_fn(report_dir, output_name=output_name)
    finally:
        p = Path(tmp_results)
        if p.exists():
            shutil.rmtree(p)
        r = Path(report_dir)
        if r.exists():
            shutil.rmtree(r)


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
