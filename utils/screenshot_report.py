import glob
import json
import logging
import shutil
import subprocess
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from utils.browser_utils import find_browser

logger = logging.getLogger(__name__)


def generate_report(results_dir="allure-results", report_dir="allure-report") -> bool:
    allure_bin = shutil.which("allure.cmd") or shutil.which("allure")
    if not allure_bin:
        logger.warning("Allure CLI not found, skipping report generation")
        return False

    try:
        subprocess.run(
            [allure_bin, "generate", results_dir, "-o", report_dir, "--clean"],
            capture_output=True, text=True, timeout=30, check=True,
        )
        logger.info("Allure report generated to %s", report_dir)
        return True
    except Exception as e:
        logger.warning("Allure generation failed: %s", e)
        return False


def filter_allure_results(src_dir: str, dest_dir: str, test_dir_prefix: str) -> bool:
    src = Path(src_dir)
    if not src.exists():
        return False

    result_files = glob.glob(str(src / "*-result.json"))
    matching_uuids = set()

    for rf in result_files:
        try:
            with open(rf) as f:
                data = json.load(f)
            full_name = data.get("fullName", "") or data.get("name", "")
            if test_dir_prefix in full_name:
                uuid = Path(rf).stem.replace("-result", "")
                matching_uuids.add(uuid)
        except (json.JSONDecodeError, OSError):
            continue

    if not matching_uuids:
        return False

    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)

    for f in src.iterdir():
        if f.name.startswith(tuple(matching_uuids)):
            shutil.copy2(f, dest / f.name)

    logger.info("Filtered %d test results to %s", len(matching_uuids), dest_dir)
    return True


def capture_report_screenshot(report_dir="allure-report", output_name="report", output_dir="screenshots", timeout=15):
    report_path = Path(report_dir).resolve()
    if not (report_path / "index.html").exists():
        logger.warning("Report index.html not found at %s", report_path)
        return None

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(report_path), **kwargs)

    server = HTTPServer(("127.0.0.1", 0), Handler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    port = server.server_address[1]

    binary = find_browser()
    if not binary:
        logger.warning("No browser binary found, skipping report screenshot")
        server.shutdown()
        return None

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

        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        screenshot_path = out / f"{output_name}.png"
        d.save_screenshot(str(screenshot_path))
        logger.info("Report screenshot saved to %s", screenshot_path)
        d.quit()
        return str(screenshot_path)
    except Exception as e:
        logger.error("Failed to capture report screenshot: %s", e)
        return None
    finally:
        server.shutdown()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    if generate_report():
        path = capture_report_screenshot()
        if path:
            print(f"Screenshot: {path}")
        else:
            print("Screenshot not captured")
    else:
        print("Report not generated")
