import requests

from decouple import config


SHOPIFY_STORE_DOMAIN = config("SHOPIFY_STORE_DOMAIN")

SHOPIFY_ADMIN_ACCESS_TOKEN = config("SHOPIFY_ADMIN_ACCESS_TOKEN")

SHOPIFY_API_VERSION = config("SHOPIFY_API_VERSION", default="2026-01")


def main():
    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{SHOPIFY_API_VERSION}/shop.json"
    headers = {

    "X-Shopify-Access-Token": SHOPIFY_ADMIN_ACCESS_TOKEN,

    "Content-Type": "application/json",

    }


    response = requests.get(url, headers=headers, timeout=30)


    print("HTTP status:", response.status_code)


    if response.status_code != 200:
        print("Something went wrong.")
        print(response.text)
        return

    data = response.json()

    print("Shop name:", data["shop"]["name"])

    print("Shop email:", data["shop"]["email"])

if __name__ == "__main__":
    main()