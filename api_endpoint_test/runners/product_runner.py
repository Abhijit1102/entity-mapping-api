from client.product import ProductAPIClient
from models.product import ProductCreate, ProductUpdate


def run_product_tests():

    print("\nRunning Product API tests")

    client = ProductAPIClient()

    # CREATE
    product = client.create_product(
        ProductCreate(
            name="Azure Cloud",
            code="AZR001",
            description="Microsoft cloud product"
        )
    )
    print("Created:", product)

    # LIST
    products = client.list_products()
    print("All Products:", products)

    # GET
    product = client.get_product(product.id)
    print("Retrieved:", product)

    # UPDATE
    updated = client.update_product(
        product.id,
        ProductUpdate(
            name="Azure Cloud Service",
            code="AZR001",
            description="Updated cloud service"
        )
    )
    print("Updated:", updated)

    # PATCH
    patched = client.partial_update_product(
        product.id,
        ProductUpdate(description="Patched description")
    )
    print("Patched:", patched)

    # DELETE
    client.delete_product(product.id)
    print("Deleted product")
