from rest_framework import serializers
from .models import VendorProductMapping


class VendorProductMappingSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorProductMapping
        fields = "__all__"

    def validate(self, data):

        vendor = data.get("vendor")
        product = data.get("product")
        is_primary = data.get("is_primary")

        # prevent duplicate mapping
        if VendorProductMapping.objects.filter(
            vendor=vendor, product=product
        ).exists():
            raise serializers.ValidationError(
                "This vendor-product mapping already exists."
            )

        # only one primary product per vendor
        if is_primary:
            if VendorProductMapping.objects.filter(
                vendor=vendor,
                is_primary=True
            ).exists():
                raise serializers.ValidationError(
                    "This vendor already has a primary product."
                )

        return data
