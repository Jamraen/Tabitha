import requests
from decouple import config


SHOPIFY_STORE_DOMAIN = config("SHOPIFY_STORE_DOMAIN")
SHOPIFY_ADMIN_ACCESS_TOKEN = config("SHOPIFY_ADMIN_ACCESS_TOKEN")
SHOPIFY_API_VERSION = config("SHOPIFY_API_VERSION", default="2026-01")


def main():
    product_id = 14788384063856

    url = (
        f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/"
        f"{SHOPIFY_API_VERSION}/products/{product_id}/images.json"
    )

    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ADMIN_ACCESS_TOKEN,
        "Content-Type": "application/json",
    }

    image_url = (
        "https://upload.wikimedia.org/wikipedia/commons/3/3f/"
        "Placeholder_view_vector.svg"
    )

    payload = {
        "image": {
            "src": image_url,
            "alt": "Test image from URL",
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=30,
    )

    print("HTTP status:", response.status_code)

    if response.status_code not in (200, 201):
        print(response.text)
        return

    print("Added image to product.")


if __name__ == "__main__":
    main()
