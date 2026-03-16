import requests
from typing import List
from models.product import ProductCreate, ProductUpdate, ProductResponse

BASE_URL = "http://127.0.0.1:8000/api/products/"


class ProductAPIClient:

    def list_products(self) -> List[ProductResponse]:
        response = requests.get(BASE_URL)
        response.raise_for_status()

        products = response.json()
        return [ProductResponse(**p) for p in products]


    def get_product(self, product_id: int) -> ProductResponse:
        response = requests.get(f"{BASE_URL}{product_id}/")
        response.raise_for_status()

        return ProductResponse(**response.json())


    def create_product(self, product: ProductCreate) -> ProductResponse:
        response = requests.post(BASE_URL, json=product.model_dump())
        response.raise_for_status()

        return ProductResponse(**response.json())


    def update_product(self, product_id: int, product: ProductUpdate) -> ProductResponse:
        response = requests.put(
            f"{BASE_URL}{product_id}/",
            json=product.model_dump()
        )
        response.raise_for_status()

        return ProductResponse(**response.json())


    def partial_update_product(self, product_id: int, product: ProductUpdate) -> ProductResponse:
        response = requests.patch(
            f"{BASE_URL}{product_id}/",
            json=product.model_dump(exclude_none=True)
        )
        response.raise_for_status()

        return ProductResponse(**response.json())


    def delete_product(self, product_id: int) -> None:
        response = requests.delete(f"{BASE_URL}{product_id}/")
        response.raise_for_status()
