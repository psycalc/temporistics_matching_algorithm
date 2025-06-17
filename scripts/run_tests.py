# Helper script to run the test suite

#!/usr/bin/env python3
import os
import subprocess
import sys


def main():
    exit_first = os.getenv("EXIT_FIRST", "false").lower() == "true"
    all_tests = os.getenv("ALL_TESTS", "false").lower() == "true"

    os.environ["PYTHONPATH"] = os.environ.get("PYTHONPATH", "") + ":" + os.getcwd()
    os.environ.setdefault("USE_TEST_DB_URL", "sqlite:///test.db")
    os.environ["FLASK_CONFIG"] = "testing"
    os.environ["BABEL_DEFAULT_LOCALE"] = "en"
    os.environ["BABEL_DEFAULT_TIMEZONE"] = "Europe/Kiev"
    os.environ["LANGUAGES"] = "en,fr,es,uk"
    os.environ["BABEL_TRANSLATION_DIRECTORIES"] = "translations;locales"

    pytest_args = ["-v", "-s"]
    if exit_first:
        pytest_args.append("-x")

    if all_tests:
        cmd = ["python", "-m", "pytest"] + pytest_args + ["tests/"]
    else:
        cmd = ["python", "-m", "pytest"] + pytest_args + ["-k", "not selenium"]

    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
