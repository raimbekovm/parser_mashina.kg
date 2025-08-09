import json
import re

with open("brands.json", "r", encoding="utf-8") as f:
    brands = json.load(f)  # {slug: mark_id}

with open("models.html", "r", encoding="utf-8") as f:
    models_html = f.read()

# id, name, slug
pattern = re.compile(
    r'"id":\s*(\d+),\s*"name":\s*"([^"]+)",\s*"slug":\s*"([^"]+)"',
    re.DOTALL
)
model_entries = pattern.findall(models_html)

# Reverse: mark_id → slug
mark_id_to_slug = {v: k for k, v in brands.items()}

updated_brands = {}
for mark_id, name, slug in model_entries:
    if mark_id in mark_id_to_slug:
        updated_brands[name] = mark_id

with open("brands_updated.json", "w", encoding="utf-8") as f:
    json.dump(updated_brands, f, ensure_ascii=False, indent=2)

print("Updated brands saved to brands_updated.json")
