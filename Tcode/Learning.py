import json #Adds the Json library


garment_info = { #Structure name

"type": "top", #information

"primary_colour": "black", #information

"warnings": ["Label not readable", "Lighting too dark", "Dress too ugly"], #information/list or array

"season": "winter", #information
}


with open("T:/Tcode/example_listing.json", "w", encoding="utf-8") as f:#    
    json.dump(garment_info, f, indent=2) #Dumps garment info to a different file


print("Saved example_listing.json") #Prints the things quotation.