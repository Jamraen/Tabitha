import json

with open("T:/Tcode/sample_listing.json", "r", encoding="utf-8") as myfile:
    listing = json.load(myfile)
category = ["category"]
print(category)
print("Loaded!")