from client.vendor import VendorAPIClient
from models.vendor import VendorCreate, VendorUpdate


def run_vendor_tests():
    print("\nRunning Vendor API tests")

    client = VendorAPIClient()

    # CREATE
    vendor = client.create_vendor(
        VendorCreate(
            name="Microsoft",
            code="MSFT001",
            description="Cloud provider"
        )
    )
    print("Created:", vendor)

    # LIST
    vendors = client.list_vendors()
    print("All Vendors:", vendors)

    # GET
    vendor = client.get_vendor(vendor.id)
    print("Retrieved:", vendor)

    # UPDATE (PUT)
    updated = client.update_vendor(
        vendor.id,
        VendorUpdate(
            name="Microsoft Corp",
            code="MSFT001",
            description="Updated description"
        )
    )
    print("Updated:", updated)

    # PATCH
    patched = client.partial_update_vendor(
        vendor.id,
        VendorUpdate(description="Patched description")
    )
    print("Patched:", patched)

    # DELETE
    client.delete_vendor(vendor.id)
    print("Deleted vendor")
