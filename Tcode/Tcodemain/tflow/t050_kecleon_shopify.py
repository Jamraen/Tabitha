import requests
from decouple import config
from datetime import datetime
import t00_guzzlord_storage
import base64

SHOPIFY_STORE_DOMAIN = config("SHOPIFY_STORE_DOMAIN")

SHOPIFY_ADMIN_ACCESS_TOKEN = config("SHOPIFY_ADMIN_ACCESS_TOKEN")

SHOPIFY_API_VERSION = config("SHOPIFY_API_VERSION", default="2026-01")

file_path = "C:\\Users\\Wylph\\Downloads\\Tabitha-main\\Tcode\\Tcodemain\\tflow\\photo_output_folder\\testphoto.jpg"

headers = {

    "X-Shopify-Access-Token": SHOPIFY_ADMIN_ACCESS_TOKEN,

    "Content-Type": "application/json",

    }

def to_shopify_bool(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    return "true" if str(value).strip().lower() in ("y", "yes", "true") else "false"

def make_garment_template():
    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{SHOPIFY_API_VERSION}/products.json"


    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print (t00_guzzlord_storage.TITLE)

    payload = {

    "product": {

    "title": str(t00_guzzlord_storage.TITLE) + " " + timestamp,

    "product_type": t00_guzzlord_storage.GARMENT_TYPE,
    "vendor": "Reluv",
    "body_html": t00_guzzlord_storage.DESCRIPTION,
    "variants": [{"price": t00_guzzlord_storage.GARMENT_PRICE,
                 "barcode": t00_guzzlord_storage.BARCODE,
                 }],
    "tags": t00_guzzlord_storage.TAGS,
    "status": "draft",
    "metafields": [
        {
            "namespace": "custom",
            "key": "waist",
            "value": t00_guzzlord_storage.WAIST,
            "type": "number_decimal"
        },
        {
            "namespace": "custom",
            "key": "inseam",
            "value": t00_guzzlord_storage.INSEAM,
            "type": "number_decimal"
        },
        {
            "namespace": "custom",
            "key": "rise",
            "value": t00_guzzlord_storage.RISE,
            "type": "number_decimal"
        },
        {
            "namespace": "custom",
            "key": "hip_cm",
            "value": t00_guzzlord_storage.HIP_CM,
            "type": "number_decimal"
        },
        {
            "namespace": "custom",
            "key": "bust_cm",
            "value": t00_guzzlord_storage.BUST_CM,
            "type": "number_decimal"
        },
        {
            "namespace": "custom",
            "key": "thigh_diameter",
            "value": t00_guzzlord_storage.THIGH_DIAMETER,
            "type": "number_decimal"
        },
        {
            "namespace": "custom",
            "key": "length_cm",
            "value": t00_guzzlord_storage.LENGTH_CM,
            "type": "number_decimal"
        },
        {
            "namespace": "custom",
            "key": "sleeve_length",
            "value": t00_guzzlord_storage.SLEEVE_LENGTH,
            "type": "number_decimal"
        },
        {
            "namespace": "custom",
            "key": "style",
            "value": t00_guzzlord_storage.STYLE,
            "type": "single_line_text_field"
        },
        {
            "namespace": "custom",
            "key": "size",
            "value": t00_guzzlord_storage.SIZE,
            "type": "number_decimal"
        },
        {
            "namespace": "custom",
            "key": "length",
            "value": t00_guzzlord_storage.LENGTH,
            "type": "number_decimal"
        },
        {
            "namespace": "custom",
            "key": "colour",
            "value": t00_guzzlord_storage.COLOUR,
            "type": "single_line_text_field"
        },
        {
            "namespace": "custom",
            "key": "active_wear",
            "value": to_shopify_bool(t00_guzzlord_storage.ACTIVE_WEAR),
            "type": "boolean"
        },
        {
            "namespace": "custom",
            "key": "condition",
            "value": t00_guzzlord_storage.CONDITION,
            "type": "single_line_text_field"
        },
        {
            "namespace": "custom",
            "key": "occasion",
            "value": t00_guzzlord_storage.OCCASION,
            "type": "single_line_text_field"
        },
        {
            "namespace": "custom",
            "key": "season",
            "value": t00_guzzlord_storage.SEASON,
            "type": "single_line_text_field"
        },
        {
            "namespace": "custom",
            "key": "material",
            "value": t00_guzzlord_storage.MATERIAL,
            "type": "single_line_text_field"
        },
        {
            "namespace": "custom",
            "key": "storage",
            "value": t00_guzzlord_storage.STORAGE_LOCATION,
            "type": "single_line_text_field"
        }
    ],
    }
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Could not reach Shopify: {e}. Please check that the WIFI is working."}


    print("HTTP status:", response.status_code)


    if response.status_code not in (200, 201):
        print("Failed to create product.")
        print(response.text)
        return {"success": False, "error": f"Shopify returned {response.status_code}: {response.text}"}


    data = response.json()

    product_id = data["product"]["id"]

    print("Created product ID:", product_id)


    # helpful: show where it is in admin (students can paste this into browser)

    print("Admin URL:")

    admin_url = (f"https://admin.shopify.com/store/{SHOPIFY_STORE_DOMAIN.split('.')[0]}/products/{product_id}")
    # add_image_from_file(product_id, file_path)
    image_ok = add_image_from_file(product_id, t00_guzzlord_storage.PHOTOFILEPATH)
    return {"success": True, "product_id": product_id, "admin_url": admin_url, "image_ok": image_ok}

#--------------------------------------------

def add_image_from_file(product_id, file_path):
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    
    url = (
        f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/"
        f"{SHOPIFY_API_VERSION}/products/{product_id}/images.json"
    )
    print(url, "Jee")
    filename = file_path.split("\\")[-1]
    print(filename, "Hi")
    payload = {
        "image": {
            "attachment": encoded,
            "filename": filename,
            # "filename": file_path.split("\\")[-1],
            "alt": "Product image",
        }
    }
    try: 
        response = requests.post(url, headers=headers, json=payload, timeout=30)
    except requests.exceptions.RequestException as e:
        print("Failed to upload image:", e)
        return False
    
    if response.status_code not in (200, 201):
        print("Failed:", response.text)
        return False
    print("Image added." +str(file_path))

# if __name__ == "__main__":
#     make_garment_template()