from django.db import models
from vendor.models import Vendor
from product.models import Product


class VendorProductMapping(models.Model):
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name="vendor_products"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_vendors"
    )

    is_primary = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "vendor_product_mapping"
        unique_together = ("vendor", "product")

    def __str__(self):
        return f"{self.vendor.name} -> {self.product.name}"
