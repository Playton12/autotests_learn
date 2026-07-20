import os
import shutil
from pathlib import Path


def find_browser() -> str | None:
    for name in ("chrome", "chromium", "firefox"):
        found = shutil.which(name)
        if found:
            return found

    for candidate in (
        "C:/Program Files/Google/Chrome/Application/chrome.exe",
        "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
        os.path.expanduser("~/AppData/Local/Google/Chrome/Application/chrome.exe"),
        os.path.expanduser("~/scoop/apps/googlechrome/current/chrome.exe"),
    ):
        if Path(candidate).exists():
            return candidate

    return None
