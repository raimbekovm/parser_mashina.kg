import json
import time
import random
import requests
from bs4 import BeautifulSoup

def extract_generations(brand_slug, model_slug):
    """
    Fetch generation data for a specific brand and model from the website.
    Returns a list of generations with their value and title.
    """
    url = f"https://m.mashina.kg/search/{brand_slug}/{model_slug}/?currency=2&sort_by=upped_at%20desc"
    print(f"Fetching generations from: {url}")

    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/115.0.0.0 Safari/537.36"),
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
    # load existing data that may have incomplete generation info
    with open("models_with_generations.json", "r", encoding="utf-8") as f:
        all_data = json.load(f)

    # retry fetching generations for models missing them
    for brand_slug, models in all_data.items():
        print(f"Checking brand: {brand_slug}")
        for model_slug, model_data in models.items():
            if not model_data.get("generations"):
                print(f"Retrying generations for model: {model_slug} ({model_data.get('model_name')})")
                new_generations = extract_generations(brand_slug, model_slug)
                if new_generations:
                    print(f"Found {len(new_generations)} generations for {model_slug}")
                    model_data["generations"] = new_generations
                else:
                    print(f"No generations found for {model_slug} on retry")
                time.sleep(random.uniform(1, 3))  # polite delay between requests

    # save the updated data
    with open("models_with_generations.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print("Retry parsing complete and data updated.")

if __name__ == "__main__":
    main()
