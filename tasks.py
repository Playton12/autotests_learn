"""Project task runner. Usage: python tasks.py <command>"""
import glob
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PYTHON = sys.executable


def run(cmd: list[str], **kwargs) -> int:
    print(f"\n> {' '.join(cmd)}\n")
    return subprocess.run(cmd, cwd=ROOT, **kwargs).returncode


def cmd_install():
    """Install dependencies"""
    return run([PYTHON, "-m", "pip", "install", "-r", "requirements.txt"])


def cmd_test():
    """Run all tests"""
    return run([PYTHON, "-m", "pytest", "-v"])


def cmd_test_api():
    """Run API tests only"""
    return run([PYTHON, "-m", "pytest", "-m", "api", "-v"])


def cmd_test_ui():
    """Run UI tests only"""
    return run([PYTHON, "-m", "pytest", "-m", "ui", "-v"])


def cmd_test_parallel():
    """Run all tests in parallel"""
    return run([PYTHON, "-m", "pytest", "-n", "auto", "-v"])


def cmd_report():
    """Generate and open Allure report"""
    rc = run(["allure", "generate", "allure-results", "-o", "allure-report", "--clean"])
    if rc == 0:
        run(["allure", "open", "allure-report"])
    return rc


def cmd_screenshot():
    """Take screenshot of Allure report"""
    return run([PYTHON, "screenshot_report.py"])


def cmd_clean():
    """Remove generated files"""
    for d in ["allure-results", "allure-report", "reports", "screenshots", ".pytest_cache"]:
        path = os.path.join(ROOT, d)
        if os.path.isdir(path):
            shutil.rmtree(path)
            print(f"  removed {d}/")
    for pycache in glob.glob(os.path.join(ROOT, "**", "__pycache__"), recursive=True):
        if ".venv" not in pycache:
            shutil.rmtree(pycache)
            print(f"  removed {pycache.replace(ROOT + os.sep, '')}")
    return 0


COMMANDS = {
    "install":       cmd_install,
    "test":          cmd_test,
    "test_api":      cmd_test_api,
    "test_ui":       cmd_test_ui,
    "test_parallel": cmd_test_parallel,
    "report":        cmd_report,
    "screenshot":    cmd_screenshot,
    "clean":         cmd_clean,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(f"\nUsage: python tasks.py <command>\n")
        for name in COMMANDS:
            print(f"  {name.replace('_', '-'):<16} {COMMANDS[name].__doc__}")
        print()
        return 0

    name = sys.argv[1].replace("-", "_")
    fn = COMMANDS.get(name)
    if not fn:
        print(f"Unknown command: {sys.argv[1]}")
        print(f"Run 'python tasks.py --help' for available commands.")
        return 1
    return fn()


if __name__ == "__main__":
    sys.exit(main())
