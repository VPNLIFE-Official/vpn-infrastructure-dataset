#!/usr/bin/env python3
"""Download the published dataset files into data/.

The files are served from https://vpn-life.com/data/ under CC BY 4.0.
This script only fetches; it does not transform anything.
"""
import pathlib
import urllib.request

BASE = "https://vpn-life.com/data/"
OUT = pathlib.Path(__file__).resolve().parents[1] / "data"
UA = "vpn-life-dataset-mirror/1.0 (+https://vpn-life.com/data/)"

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


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        req = urllib.request.Request(BASE + name, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=120) as r:
            body = r.read()
        (OUT / name).write_bytes(body)
        print(f"{name}  {len(body):,} bytes")


if __name__ == "__main__":
    main()
