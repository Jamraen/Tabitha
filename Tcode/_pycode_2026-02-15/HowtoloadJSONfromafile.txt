import json #imports json library.


with open("T:/Tcode/example_listing.json", "r", encoding="utf-8") as myfile: #opens a file called example_listing and prepares to pull from it.
    garment_info = json.load(myfile) #pulls garment info from above stated file.

colour = garment_info["primary_colour"] #pulls the colour from garment info and turns it into a colour variable
brand = garment_info.get("brand_visible", None) #check for brand, if not visible return None
warnings = garment_info.get("warnings", None) # check for warnings, if none visible return None

print(colour) #prints colour variable
print(garment_info) #prints garment info
print(brand) #prints brand
print(warnings) #prints warnings