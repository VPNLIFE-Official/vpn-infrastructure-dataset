#!/usr/bin/env python3
"""Download the published dataset files into data/.

The files are served from https://vpn-life.com/data/ under CC BY 4.0.
This script only fetches; it does not transform anything.

2026-09-23: the origin returns Cloudflare 52x errors intermittently.
A single 525 on one file used to fail the whole scheduled run
(2026-09-21T21:40Z: `HTTP Error 525`, job failed in 18 seconds).
The origin was healthy again seconds later, so we retry with a backoff
instead of failing the run. We also refuse to overwrite a good file with
a short or empty body.
"""
import pathlib
import sys
import time
import urllib.error
import urllib.request

BASE = "https://vpn-life.com/data/"
OUT = pathlib.Path(__file__).resolve().parents[1] / "data"
UA = "vpn-life-dataset-mirror/1.0 (+https://vpn-life.com/data/)"

TRIES = 5
BACKOFF = 15          # seconds; multiplied by the attempt number
MIN_BYTES = 64        # anything shorter than this is not a dataset file

FILES = [
    "vpn-life-country-servers.csv",
    "vpn-life-country-load.csv",
    "vpn-life-country-coverage.csv",
    "vpn-life-provider-daily.csv",
    "vpn-life-provider-current.csv",
    "vpn-life-fx-daily.csv",
    "vpn-life-speed-city.csv",
    "vpn-life-speed-measurements.csv",
    "vpn-life-dataset.json",
]


def fetch(name):
    """Fetch one file, retrying transient origin errors."""
    last = None
    for attempt in range(1, TRIES + 1):
        try:
            req = urllib.request.Request(BASE + name, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                body = r.read()
            if len(body) < MIN_BYTES:
                raise ValueError(f"body too short ({len(body)} bytes)")
            return body
        except urllib.error.HTTPError as ex:
            last = ex
            # 5xx and 429 are worth retrying; 404 means the file moved.
            if ex.code < 500 and ex.code != 429:
                raise
        except Exception as ex:                                  # noqa: BLE001
            last = ex
        if attempt < TRIES:
            wait = BACKOFF * attempt
            print(f"  {name}: {last} — retrying in {wait}s "
                  f"({attempt}/{TRIES})", flush=True)
            time.sleep(wait)
    raise SystemExit(f"{name}: giving up after {TRIES} attempts — {last}")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        body = fetch(name)
        (OUT / name).write_bytes(body)
        print(f"{name}  {len(body):,} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
