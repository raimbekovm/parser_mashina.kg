# Mashina.kg Car Data Parser

### Overview
This repository contains a Python-based web scraping and data processing toolkit that builds a clean, structured dataset of automobiles from `mashina.kg`. It extracts brands, models, and model generations and stores them as easy-to-use JSON files for analysis, ML feature engineering, or integration into other systems.

### Why it matters
- **Real-world scraping**: Handles dynamic site structure with robust parsing, delays, and retries.
- **Data engineering mindset**: Clear pipeline, intermediate artifacts, and JSON schemas for reproducibility.
- **Pragmatic reliability**: Retries for missing data, polite scraping practices, and modular scripts.

---

### Highlights
- **Brand parsing** from saved HTML into canonical IDs and slugs
- **Name reconciliation** between slugs and human-readable brand names
- **Generation collection** per model with HTTP headers, timeouts, and polite delays
- **Retry mechanism** to backfill missing generations
- **Clean JSON outputs** suitable for downstream tasks

---

### Tech Stack
- Python 3.9+
- requests, beautifulsoup4

Install dependencies:
```bash
pip install -U requests beautifulsoup4
```

---

### Repository Structure
- `brand_name.py` — Parse brand slugs and IDs from a saved HTML file
- `replace_name.py` — Map human-readable brand names to IDs using a models HTML dump
- `generations.py` — Fetch generations for each brand/model (from live website)
- `retry.py` — Retry fetching generations for models that are missing data
- `uniting.py` — Merge brand slug/ID/name into a single, sorted structure
- `models_with_generations_sample.json` — Example of the final structured output

Note: Some scripts expect input files you generate in prior steps (see “Pipeline & Usage”).

---

### Data Pipeline & Usage
Below is a minimal end-to-end flow. Paths and filenames mirror the current scripts.

1) Extract brand slugs → IDs from saved HTML
- Input: `all.html` (a previously saved HTML page that contains the brand `<option>` elements)
- The script expects it at `.venv/all.html` by default. Adjust the path in `brand_name.py` if needed.
- Output: `.venv/brands.json`
```bash
python brand_name.py
# If needed, copy output to project root for later steps
cp .venv/brands.json brands.json
```

2) Reconcile brand names → IDs using a models HTML dump
- Inputs: `brands.json` (from step 1), `models.html` (saved HTML with model metadata)
- Output: `brands_updated.json` (name → id)
```bash
python replace_name.py
```

3) Merge brand slug, id, and human-readable name
- Inputs: `brands.json`, `brands_updated.json`
- Output: `brands_merged.json`
```bash
python uniting.py
```

4) Collect generations for each model (live requests)
- Input: `models_by_brand.json` with structure:
```json
{
  "toyota": [ { "name": "Camry", "slug": "camry" }, "..." ],
  "bmw":    [ { "name": "3 Series", "slug": "3-series" }, "..." ]
}
```
- Output: `models_with_generations.json`
```bash
python generations.py
```

5) Retry backfilling missing generations
- Input/Output: `models_with_generations.json` (updated in place)
```bash
python retry.py
```

If you do not yet have `models_by_brand.json`, you can create it using your preferred approach (e.g., additional scraping of per-brand model lists) following the example schema above.

---

### Sample Output
A slice from `models_with_generations_sample.json`:
```json
{
  "ac": {
    "cobra": {
      "model_name": "Cobra",
      "generations": [
        { "generation_value": "238", "generation_title": "AC Cobra Mk VI (2013-2015)" },
        { "generation_value": "239", "generation_title": "AC Cobra Mk V (1999-2007)" }
      ]
    }
  }
}
```

---

### Practical Notes
- The scraper sets realistic headers and timeouts and uses small randomized delays between requests.
- Keep saved HTML snapshots (`all.html`, `models.html`) under version control only if they are small and non-sensitive; otherwise document how to reproduce them.
- Always respect `mashina.kg`’s Terms of Service and robots rules. Use responsibly.

---

### Roadmap / Possible Extensions
- Add a dedicated script to build `models_by_brand.json` end-to-end
- CLI interface with subcommands and argument parsing
- Caching and incremental updates
- Dockerfile and `requirements.txt` for one-command setup
- Unit tests with VCR-like HTTP cassettes

---

### Author & Contact
If you’d like a walkthrough of the pipeline or want to discuss scraping/data engineering roles, feel free to reach out. I’m happy to demo the tooling and talk through design trade-offs.
- Name: Murat Raimbekov
- LinkedIn: [linkedin.com/in/murat-raimbekov](https://www.linkedin.com/in/murat-raimbekov)