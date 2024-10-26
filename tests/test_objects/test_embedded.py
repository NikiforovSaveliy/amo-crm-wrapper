from unittest import TestCase

from amopy.exceptions import DataclassValidationError
from amopy.objects.embedded import (
    EmbeddedLead,
    EmbeddedContact,
    EmbeddedCompany,
    EmbeddedMetadataCatalogItem,
    EmbeddedCatalogItem,
)


class TestEmbeddedLead(TestCase):

    def test_valid_embedded_lead(self):
        lead = EmbeddedLead(id=1)
        self.assertEqual(lead.id, 1)

    def test_invalid_id_type_embedded_lead(self):
        with self.assertRaises(DataclassValidationError):
            EmbeddedLead(id="one")


class TestEmbeddedContact(TestCase):

    def test_valid_embedded_contact(self):
        contact = EmbeddedContact(id=1, is_main=True)
        self.assertEqual(contact.id, 1)
        self.assertTrue(contact.is_main)

    def test_invalid_id_type_embedded_contact(self):
        with self.assertRaises(DataclassValidationError):
            EmbeddedContact(id="one", is_main=True)

    def test_invalid_is_main_type_embedded_contact(self):
        with self.assertRaises(DataclassValidationError):
            EmbeddedContact(id=1, is_main="yes")


class TestEmbeddedCompany(TestCase):

    def test_valid_embedded_company(self):
        company = EmbeddedCompany(id=1)
        self.assertEqual(company.id, 1)

    def test_invalid_id_type_embedded_company(self):
        with self.assertRaises(DataclassValidationError):
            EmbeddedCompany(id="one")


class TestEmbeddedMetadataCatalogItem(TestCase):

    def test_valid_embedded_metadata_catalog_item(self):
        item = EmbeddedMetadataCatalogItem(
            id=1, catalog_id=2, price_id=100, quantity=50
        )
        self.assertEqual(item.id, 1)
        self.assertEqual(item.catalog_id, 2)
        self.assertEqual(item.price_id, 100)
        self.assertEqual(item.quantity, 50)

    def test_catalog_id_as_string(self):
        item = EmbeddedMetadataCatalogItem(
            id=1, catalog_id="2", price_id=100, quantity=50
        )
        self.assertEqual(item.catalog_id, 2)

    def test_invalid_id_type_embedded_metadata_catalog_item(self):
        with self.assertRaises(DataclassValidationError):
            EmbeddedMetadataCatalogItem(
                id="one", catalog_id=2, price_id=100, quantity=50
            )

    def test_invalid_quantity_type_embedded_metadata_catalog_item(self):
        with self.assertRaises(DataclassValidationError):
            EmbeddedMetadataCatalogItem(
                id=1, catalog_id=2, price_id=100, quantity="fifty"
            )


class TestEmbeddedCatalogItem(TestCase):

    def test_valid_embedded_catalog_item(self):
        metadata = EmbeddedMetadataCatalogItem(
            id=1, catalog_id=2, price_id=100, quantity=50
        )
        item = EmbeddedCatalogItem(id=1, metadata=metadata)
        self.assertEqual(item.id, 1)
        self.assertEqual(item.metadata.id, 1)
        self.assertEqual(item.metadata.catalog_id, 2)

    def test_invalid_id_type_embedded_catalog_item(self):
        metadata = EmbeddedMetadataCatalogItem(
            id=1, catalog_id=2, price_id=100, quantity=50
        )
        with self.assertRaises(DataclassValidationError):
            EmbeddedCatalogItem(id="one", metadata=metadata)

    def test_invalid_metadata_type(self):
        with self.assertRaises(DataclassValidationError):
            EmbeddedCatalogItem(id=1, metadata="invalid_metadata")
