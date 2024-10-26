from unittest import TestCase

from amopy.exceptions import DataclassValidationError
from amopy.objects.linking import LinkingItemMetadata, LinkingItem


class TestLinkingItemMetadata(TestCase):

    def test_valid_linking_item_metadata(self):
        data = LinkingItemMetadata(quantity=10, catalog_id=123)
        self.assertEqual(data.quantity, 10)
        self.assertEqual(data.catalog_id, 123)

    def test_invalid_quantity_type(self):
        with self.assertRaises(DataclassValidationError):
            LinkingItemMetadata(quantity="ten", catalog_id=123)

    def test_invalid_catalog_id_type(self):
        with self.assertRaises(DataclassValidationError):
            LinkingItemMetadata(quantity=10, catalog_id="catalog_123")


class TestLinkingItem(TestCase):

    def test_valid_linking_item(self):
        metadata = LinkingItemMetadata(quantity=5, catalog_id=321)
        item = LinkingItem(to_entity_id=1, to_entity_type="leads", metadata=metadata)
        self.assertEqual(item.to_entity_id, 1)
        self.assertEqual(item.to_entity_type, "leads")
        self.assertEqual(item.metadata.quantity, 5)
        self.assertEqual(item.metadata.catalog_id, 321)

    def test_valid_linking_item_without_metadata(self):
        item = LinkingItem(to_entity_id=2, to_entity_type="contacts", metadata=None)
        self.assertEqual(item.to_entity_id, 2)
        self.assertEqual(item.to_entity_type, "contacts")
        self.assertIsNone(item.metadata)

    def test_invalid_entity_type(self):
        with self.assertRaises(DataclassValidationError):
            LinkingItem(to_entity_id=3, to_entity_type="invalid_type", metadata=None)

    def test_invalid_to_entity_id_type(self):
        with self.assertRaises(DataclassValidationError):
            LinkingItem(to_entity_id="three", to_entity_type="leads", metadata=None)
