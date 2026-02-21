import requests
from decouple import config

SHOPIFY_STORE_DOMAIN = config("SHOPIFY_STORE_DOMAIN")
SHOPIFY_ADMIN_ACCESS_TOKEN = config("SHOPIFY_ADMIN_ACCESS_TOKEN")
SHOPIFY_API_VERSION = config("SHOPIFY_API_VERSION", default="2024-10")


def main():
    product_id = 14788384063856  # <-- real product ID

    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{SHOPIFY_API_VERSION}/products/{product_id}.json"

    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ADMIN_ACCESS_TOKEN,
        "Content-Type": "application/json",
    }

    description_html = """
    <p><strong>Beautiful pre-loved item</strong> in great condition.</p>
    <p>Measurements (flat lay): waist 36cm, length 84cm.</p>
    """

    payload = {
        "product": {
            "id": product_id,
            "body_html": description_html.strip(),
        }
    }

    response = requests.put(url, headers=headers, json=payload, timeout=30)

    print("HTTP status:", response.status_code)

    if response.status_code not in (200, 201):
        print("Failed.")
        print(response.text)
        return

    print("Updated description for product:", product_id)


if __name__ == "__main__":
    main()
