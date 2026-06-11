import json


listing = {

"type": "dress",

"primary_colour": "blue",

"season": "summer",

"warnings": ["Size tag not readable", "Product may contain radioactive isotopes"],

"pricing": {

"currency": "NZD",

"recommended_resale_price": 35.0, 

"confidence": 0.7

}

}


print("Type:", listing["type"])

print("Price:", listing["pricing"]["recommended_resale_price"])


listing["warnings"].append("Lighting uneven")

listing["pricing"]["recommended_resale_price"] = 29.0

print("Price:", listing["pricing"]["recommended_resale_price"])

with open("T:/Tcode/practice.json", "w", encoding="utf-8") as myfile:
    json.dump(listing, myfile, indent=2)


print("Saved practice.json")