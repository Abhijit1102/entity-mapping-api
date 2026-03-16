from client.certification import CertificationAPIClient
from models.certification import CertificationCreate, CertificationUpdate


def run_certification_tests():

    print("\nRunning Certification API tests")

    client = CertificationAPIClient()

    # CREATE
    certification = client.create_certification(
        CertificationCreate(
            name="AWS Certified Developer",
            code="AWSDEV001",
            description="AWS developer certification"
        )
    )
    print("Created:", certification)

    # LIST
    certifications = client.list_certifications()
    print("All Certifications:", certifications)

    # GET
    certification = client.get_certification(certification.id)
    print("Retrieved:", certification)

    # UPDATE
    updated = client.update_certification(
        certification.id,
        CertificationUpdate(
            name="AWS Certified Developer Associate",
            code="AWSDEV001",
            description="Updated certification"
        )
    )
    print("Updated:", updated)

    # PATCH
    patched = client.partial_update_certification(
        certification.id,
        CertificationUpdate(description="Patched description")
    )
    print("Patched:", patched)

    # DELETE
    client.delete_certification(certification.id)
    print("Deleted certification")
