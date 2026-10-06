"""Capture the README screenshots from a locally running copy of the app.

Starts the app on a spare port with a throwaway case directory, opens one demonstration case
through the public API, and asks a Chromium-based browser in headless mode to save each page
as a PNG under docs/screenshots/. Nothing here is used by the app or the tests.

    uv run python scripts/capture_screenshots.py [--browser PATH]
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "docs" / "screenshots"
PORT = 8765
BASE = f"http://127.0.0.1:{PORT}"
BROWSERS = (
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/usr/bin/chromium",
    "/usr/bin/google-chrome",
)
MIGRATION = "rbi.nbfc-it-framework.2017__rbi.nbfc-cyber.2026"
TABLETOP = (
    "/tabletop?classes=nbfc.middle_layer&scenario=ransomware-with-personal-data"
    "&start=2026-10-01T09:00"
)


def _post(path: str, payload: dict) -> dict:
    request = urllib.request.Request(
        BASE + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={"content-type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def _wait_until_up() -> None:
    for _ in range(100):
        try:
            with urllib.request.urlopen(BASE + "/obligations", timeout=2):
                return
        except OSError:
            time.sleep(0.3)
    raise RuntimeError("the app did not start")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", default=next((b for b in BROWSERS if Path(b).exists()), None))
    args = parser.parse_args()
    if not args.browser:
        print("No Chromium-based browser found; pass --browser PATH", file=sys.stderr)
        return 2
    OUT.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="sentinelbrief-shots-"))
    env = {**os.environ, "SENTINELBRIEF_CASES_DIR": str(work / "cases")}
    server = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "sentinelbrief.api.app:app", "--port", str(PORT)],
        cwd=REPO,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_until_up()
        case_id = _post(
            "/api/cases",
            {
                "opened_by": "Asha Rao",
                "entity_classes": ["nbfc.middle_layer"],
                "incident_types": ["Malicious code attacks such as Ransomware"],
                "when_detected": "2026-10-01T09:00:00+05:30",
                "when_noticed": "2026-10-01T09:25:00+05:30",
                "is_cyber_incident": True,
            },
        )["case_id"]
        pages = {
            "01-feed.png": ("/", 1500),
            "02-incident-case.png": (f"/cases/{case_id}", 2600),
            "03-obligation-with-citation.png": (
                "/obligations/rbi.nbfc-cyber.2026.ch5-incident-reporting-6h",
                1500,
            ),
            "04-migrator-changed-clauses.png": (f"/migrations/{MIGRATION}?status=changed", 2200),
            "05-tabletop.png": (TABLETOP, 1900),
        }
        for name, (path, height) in pages.items():
            target = OUT / name
            subprocess.run(
                [
                    args.browser,
                    "--headless=new",
                    "--disable-gpu",
                    "--hide-scrollbars",
                    f"--user-data-dir={work / 'profile'}",
                    f"--window-size=1280,{height}",
                    f"--screenshot={target}",
                    BASE + path,
                ],
                check=True,
                timeout=120,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if not target.is_file():
                raise RuntimeError(f"{args.browser} wrote no screenshot for {path}")
            print(f"{name}: {target.stat().st_size} bytes")
    finally:
        server.terminate()
        server.wait(timeout=20)
        shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
