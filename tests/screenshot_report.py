import logging
import os
import shutil
import subprocess
import threading
import time
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from tests.browser_utils import find_browser

logger = logging.getLogger(__name__)


def generate_report():
    java_home = os.path.expanduser("~/scoop/apps/openjdk/current")
    if not (Path(java_home) / "bin" / "java.exe").exists():
        logger.warning("Java not found, skipping allure report")
        return False

    env = {**os.environ, "JAVA_HOME": java_home}
    try:
        allure_bin = shutil.which("allure.cmd") or shutil.which("allure") or "allure"
        subprocess.run(
            [allure_bin, "generate", "allure-results", "-o", "allure-report", "--clean"],
            env=env, capture_output=True, text=True, timeout=30, check=True,
        )
        logger.info("Allure report generated")
        return True
    except Exception as e:
        logger.warning("Allure generation failed: %s", e)
        return False


def capture_report_screenshot(report_dir="allure-report", output_dir="screenshots", timeout=15):
    report_path = Path(report_dir).resolve()
    if not (report_path / "index.html").exists():
        logger.warning("Report index.html not found at %s", report_path)
        return

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(report_path), **kwargs)

    server = HTTPServer(("127.0.0.1", 0), Handler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    port = server.server_address[1]
    logger.info("Report HTTP server on http://127.0.0.1:%s", port)

    binary = find_browser()
    if not binary:
        logger.warning("No browser binary found, skipping report screenshot")
        server.shutdown()
        return

    options = Options()
    options.binary_location = binary
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    try:
        d = webdriver.Chrome(options=options)
        d.set_window_size(1440, 900)
        d.get(f"http://127.0.0.1:{port}/index.html")
        WebDriverWait(d, timeout).until(
            lambda drv: drv.execute_script("return document.readyState") == "complete"
        )
        time.sleep(3)
        total_height = d.execute_script("return document.body.scrollHeight")
        d.set_window_size(1440, max(900, total_height))
        time.sleep(2)

        Path(output_dir).mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = Path(output_dir) / f"allure_report_{ts}.png"
        saved = d.save_screenshot(str(screenshot_path))
        logger.info("Report screenshot saved to %s (success=%s)", screenshot_path, saved)
        d.quit()
    except Exception as e:
        logger.exception("Failed to capture report screenshot: %s", e)
    finally:
        server.shutdown()
