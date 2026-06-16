import requests

from decouple import config

from datetime import datetime


SHOPIFY_STORE_DOMAIN = config("SHOPIFY_STORE_DOMAIN")

SHOPIFY_ADMIN_ACCESS_TOKEN = config("SHOPIFY_ADMIN_ACCESS_TOKEN")

SHOPIFY_API_VERSION = config("SHOPIFY_API_VERSION", default="2026-01")


def main():
    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{SHOPIFY_API_VERSION}/products.json"

    headers = {

    "X-Shopify-Access-Token": SHOPIFY_ADMIN_ACCESS_TOKEN,

    "Content-Type": "application/json",

    }


    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    payload = {

    "product": {

    "title": f"Pre-loved garment test ({timestamp})",

    "status": "draft"

    }

    }


    response = requests.post(url, headers=headers, json=payload, timeout=30)


    print("HTTP status:", response.status_code)


    if response.status_code not in (200, 201):
        print("Failed to create product.")

        print(response.text)

        return


        data = response.json()

        product_id = data["product"]["id"]

        print("Created product ID:", product_id)


        # helpful: show where it is in admin (students can paste this into browser)

        print("Admin URL:")

        print(f"https://admin.shopify.com/store/{SHOPIFY_STORE_DOMAIN.split('.')[0]}/products/{product_id}")


if __name__ == "__main__":
    main()