import json

# original mapping: slug -> id
with open("brands.json", "r", encoding="utf-8") as f:
    brands = json.load(f)

# updated mapping: name -> id
with open("brands_updated.json", "r", encoding="utf-8") as f:
    brands_updated = json.load(f)

# Reverse updated mapping to: id -> name
id_to_name = {mark_id: name for name, mark_id in brands_updated.items()}

# Merge slug, id, and name into a single list
merged_list = [
    {
        "id": mark_id,
        "slug": slug,
        "name": id_to_name.get(mark_id, slug)  # fallback to slug if name missing
    }
    for slug, mark_id in brands.items()
]

# sort alphabetically
merged_list.sort(key=lambda x: x["name"].lower())

# save merged data
with open("brands_merged.json", "w", encoding="utf-8") as f:
    json.dump(merged_list, f, ensure_ascii=False, indent=2)

print("Merged data saved to brands_merged.json")
