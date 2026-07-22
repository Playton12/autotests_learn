import logging
import os
from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

BASE_URL = os.getenv("BASE_URL", "http://localhost:8080/v2")
API_KEY = os.getenv("API_KEY", "")
UI_BASE_URL = os.getenv("UI_BASE_URL", "https://www.saucedemo.com")
UI_USERNAME = os.getenv("UI_USERNAME", "standard_user")
UI_PASSWORD = os.getenv("UI_PASSWORD", "secret_sauce")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
BROWSER = os.getenv("BROWSER", "chrome")
try:
    WAIT_TIMEOUT = int(os.getenv("WAIT_TIMEOUT", "10"))
except ValueError:
    WAIT_TIMEOUT = 10
