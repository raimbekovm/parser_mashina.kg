import json
import time
import random
import requests
from bs4 import BeautifulSoup

def extract_generations(brand_slug, model_slug):
    """
    Fetch and parse generation data for a given brand and model slug.
    Returns a list of generations with their value and title.
    """
    url = f"https://m.mashina.kg/search/{brand_slug}/{model_slug}/?currency=2&sort_by=upped_at%20desc"
    print(f"Fetching generations from: {url}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    optgroups = soup.find_all("optgroup", class_="only-group")

    generations = []
    for optgroup in optgroups:
        for option in optgroup.find_all("option"):
            generations.append({
                "generation_value": option.get("value"),
                "generation_title": option.get("title", "")
            })
    return generations

def main():
    # load models organized by brand slug
    with open("models_by_brand.json", "r", encoding="utf-8") as f:
        models_by_brand = json.load(f)

    all_data = {}

    for brand_slug, models in models_by_brand.items():
        print(f"Parsing brand: {brand_slug} with {len(models)} models")
        all_data[brand_slug] = {}
        for model in models:
            model_slug = model.get("slug")
            if not model_slug:
                continue

            generations = extract_generations(brand_slug, model_slug)
            all_data[brand_slug][model_slug] = {
                "model_name": model.get("name"),
                "generations": generations
            }

            time.sleep(random.uniform(1, 3))  # delay between requests

    # save all parsed data to JSON
    with open("models_with_generations.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print("Saved models with generations to models_with_generations.json")

if __name__ == "__main__":
    main()