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
    search_word = "skirt"  # try: dress, pants, t-shirt

    taxonomy_query = """
    query TaxonomySearch($search: String!) {
        taxonomy {
            categories(first: 10, search: $search) {
                nodes {
                    id
                    name
                }
            }
        }
    }
    """

    data = send_graphql(taxonomy_query, {"search": search_word})
    nodes = data["taxonomy"]["categories"]["nodes"]

    print("Search results:")
    for i, node in enumerate(nodes, start=1):
        print(i, node["name"], node["id"])

    print("\nPick one of the IDs above and paste it into chosen_category_id.\n")

    chosen_category_id = None  # e.g. "gid://shopify/TaxonomyCategory/..."

    if not chosen_category_id:
        print("No category chosen yet. Stop here after copying one.")
        return

    product_id_number = 14788384063856
    product_gid = f"gid://shopify/Product/{product_id_number}"

    update_mutation = """
    mutation SetCategory($input: ProductInput!) {
        productUpdate(input: $input) {
            product {
                id
            }
            userErrors {
                field
                message
            }
        }
    }
    """

    variables = {
        "input": {
            "id": product_gid,
            "productCategory": {
                "productTaxonomyNodeId": chosen_category_id
            },
        }
    }

    data2 = send_graphql(update_mutation, variables)
    result2 = data2["productUpdate"]

    if result2["userErrors"]:
        print("User errors:")
        for err in result2["userErrors"]:
            print(err)
        return

    print("Category set successfully!")


if __name__ == "__main__":
    main()
