import requests
from decouple import config


SHOPIFY_STORE_DOMAIN = config("SHOPIFY_STORE_DOMAIN")
SHOPIFY_ADMIN_ACCESS_TOKEN = config("SHOPIFY_ADMIN_ACCESS_TOKEN")
SHOPIFY_API_VERSION = config("SHOPIFY_API_VERSION", default="2026-01")


def send_graphql(query_text: str, variables: dict) -> dict:
    url = (
        f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/"
        f"{SHOPIFY_API_VERSION}/graphql.json"
    )

    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ADMIN_ACCESS_TOKEN,
        "Content-Type": "application/json",
    }

    response = requests.post(
        url,
        headers=headers,
        json={
            "query": query_text,
            "variables": variables,
        },
        timeout=60,
    )

    response.raise_for_status()

    payload = response.json()

    if "errors" in payload:
        raise RuntimeError(payload["errors"])

    return payload["data"]


def main():
    product_id_number = 14788384063856
    product_gid = f"gid://shopify/Product/{product_id_number}"

    mutation = """
    mutation SetMetafields($metafields: [MetafieldsSetInput!]!) {
        metafieldsSet(metafields: $metafields) {
            metafields {
                id
                namespace
                key
                value
                type
            }
            userErrors {
                field
                message
            }
        }
    }
    """

    metafields_to_set = [
        {
            "ownerId": product_gid,
            "namespace": "consignment",
            "key": "seller_number",
            "type": "single_line_text_field",
            "value": "SELLER-042",
        },
        {
            "ownerId": product_gid,
            "namespace": "storage",
            "key": "location",
            "type": "single_line_text_field",
            "value": "R2-B7-BIN12",
        },
        {
            "ownerId": product_gid,
            "namespace": "measurements",
            "key": "length_cm",
            "type": "number_decimal",
            "value": "84.2",
        },
    ]

    data = send_graphql(mutation, {"metafields": metafields_to_set})
    result = data["metafieldsSet"]

    if result["userErrors"]:
        print("User errors:")
        for err in result["userErrors"]:
            print(err)
        return

    print("Metafields written:")
    for mf in result["metafields"]:
        print(mf["namespace"], mf["key"], "=", mf["value"])


if __name__ == "__main__":
    main()
