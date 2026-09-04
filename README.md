# VPN Infrastructure Dataset

An independent, **daily-updated, timestamped** dataset of VPN infrastructure.

Every day we fetch the public server lists that VPN providers themselves expose,
count them per country, and write down the date we saw them. Every row carries
its own observation date.

| | |
|---|---|
| **Providers** | 7 |
| **Countries** | 155 |
| **Rows** | 9,231 |
| **Covered** | 2026-08-26 → 2026-09-03 (9 days) |
| **Updated** | Daily, around 06:00 Japan time |
| **License** | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ja) |

- **Dataset home:** https://vpn-life.com/data/
- **Methodology:** https://vpn-life.com/how-we-test/
- **Machine-readable manifest:** https://vpn-life.com/data/vpn-life-dataset.json

> This table is generated from the dataset itself. It is not written by hand,
> so it cannot drift from what the files actually contain.

---

## Why this exists

VPN providers advertise rounded numbers — "8,000+ servers", "100+ countries" —
and review sites quote those numbers for months without re-checking. We have
seen articles still citing a figure that the provider's own list contradicts on
the same day.

So we do the boring thing: **fetch the list, count it, write down the date.**

We do not estimate. If we have not measured something, the file says so instead
of filling the gap with a plausible number.

---

## Files

| File | Columns | Rows | What it is |
|---|---|---:|---|
| `vpn-life-country-servers.csv` | `date, vpn, country_code, servers` | 2491 | Per-country server counts, one row per provider per country per day. |
| `vpn-life-country-load.csv` | `date, vpn, country_code, load_pct` | 900 | Per-country mean server load, as reported by the provider's own list. |
| `vpn-life-country-coverage.csv` | `date, vpn, country_code, cities, source_type` | 5624 | Whether a provider had a presence in a country that day, and in how many cities. This is the only file that covers **all providers**. |
| `vpn-life-provider-daily.csv` | `date, vpn, metric, value` | 84 | Totals per provider: servers, locations, countries. |
| `vpn-life-provider-current.csv` | `observed_date, vpn, …, source_url` | 7 | The latest values, each with the URL they were read from. |
| `vpn-life-fx-daily.csv` | `date, currency, rate_per_usd` | 96 | Exchange rates, used when converting prices. |
| `vpn-life-speed-city.csv` | `city, vpn, mean_down_mbps, paired_measurements, …, verdict` | 28 | City-level speed, computed as a ratio of means. |
| `vpn-life-speed-measurements.csv` | `city, vpn, measurements, median_down_mbps, …` | 1 | Speed built up one measurement at a time, reported as a median. |
| `vpn-life-dataset.json` | — | — | Everything above plus the metadata, in a single file. |

---

## Caveats — please read before citing

1. **Server counts are what the provider publishes**, not an independent census
   of physical machines.
2. **Load percentages are the mean of the values a provider's own list returns**
   for that country at the moment we fetched it. They are **not** comparable
   across providers unless you assume every provider defines "load" identically.
   We do not assume that.
3. **Speed data is sparse.** It covers **2 providers**, and only a small number
   of cities have enough paired measurements to support a verdict. Rows marked
   `insufficient` should not be used to rank providers.
4. **The series is young.** Check `temporalCoverage` in the JSON before drawing
   trend lines.
5. Missing values are left empty. They are never zero-filled.

---

## Using it

```bash
pip install pandas
python - <<'PY'
import pandas as pd
url = "https://vpn-life.com/data/vpn-life-country-coverage.csv"
df = pd.read_csv(url)
# どの会社が、その日、何カ国に拠点を持っていたか
print(df.groupby(["date", "vpn"])["country_code"].nunique().unstack())
PY
```

---

## How to cite

```
VPN LIFE, “VPN LIFE Dataset (2026-09-03)”, https://vpn-life.com/data/, licensed under CC BY 4.0.
```

BibTeX:

```bibtex
@misc{vpnlife_dataset_20260903,
  title        = {VPN LIFE Dataset: daily VPN infrastructure measurements},
  author       = {{VPN LIFE}},
  year         = {2026},
  howpublished = {\url{https://vpn-life.com/data/}},
  note         = {Version 2026-09-03. Licensed under CC BY 4.0}
}
```

See also `CITATION.cff` in this repository.

---

## Machine-readable descriptors

The schema is published in two standard formats so tools and registries can
read it without a human in the loop. Both are regenerated whenever the data is.

| File | Standard | Read by |
|---|---|---|
| `datapackage.json` | [Frictionless Data](https://specs.frictionlessdata.io/data-package/) | data.world, CKAN, OpenRefine, `frictionless` CLI |
| `croissant.json` | [Croissant 1.0](http://mlcommons.org/croissant/) (ML Commons) | Google Dataset Search, Hugging Face, Kaggle |

```bash
pip install frictionless
frictionless validate datapackage.json
```

---

## Requests

If you are a journalist or researcher and need something these files do not
cover — a longer window, the pre-aggregation records, a specific country or
provider — ask via https://vpn-life.com/about/ . We share raw records.

---

## License

Data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ja). You may use it commercially and modify
it. Please credit **VPN LIFE** and link to https://vpn-life.com/data/ .
