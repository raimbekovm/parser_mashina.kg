from bs4 import BeautifulSoup
import json

HTML_FILE_PATH = ".venv/all.html"  # Local HTML file to parse

with open(HTML_FILE_PATH, "r", encoding="utf-8") as file:
    lines = file.readlines()

# Extract the part of HTML containing brand <option> tags
brand_html = "".join(lines[2483:2694])

soup = BeautifulSoup(brand_html, "html.parser")
brands = {}

for option in soup.find_all("option"):
    slug = option.get("data-slug")
    mark_id = option.get("data-mark-id")
    if slug and mark_id:
        brands[slug] = mark_id

# Output to console
for slug, mark_id in brands.items():
    print(f"{mark_id}: {slug}")

# Save to JSON
with open(".venv/brands.json", "w", encoding="utf-8") as output_file:
    json.dump(brands, output_file, ensure_ascii=False, indent=2)
