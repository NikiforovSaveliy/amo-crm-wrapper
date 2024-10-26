from datetime import datetime
from unittest import TestCase

from amopy.exceptions import DataclassValidationError
from amopy.objects.custom_fields import TextCustomFieldObject
from amopy.objects.embedded import EmbeddedLead, EmbeddedContact, EmbeddedCompany
from amopy.objects.entities import (
    TagObject,
    EmbeddedObject,
    LeadObject,
    ContactObject,
    CatalogItem,
)


class TestTagObject(TestCase):

    def test_valid_tag_object(self):
        tag = TagObject(id=1, name="Important", color="red", request_id="req_123")
        self.assertEqual(tag.id, 1)
        self.assertEqual(tag.name, "Important")
        self.assertEqual(tag.color, "red")
        self.assertEqual(tag.request_id, "req_123")

    def test_invalid_tag_id(self):
        with self.assertRaises(DataclassValidationError):
            TagObject(id="one", name="Important", color="red")


class TestEmbeddedObject(TestCase):

    def test_valid_embedded_object(self):
        leads = [EmbeddedLead(id=1)]
        contacts = [EmbeddedContact(id=2, is_main=True)]
        tags = [TagObject(id=1, name="Tag1", color="blue")]
        companies = [EmbeddedCompany(id=3)]
        embedded = EmbeddedObject(
            leads=leads, contacts=contacts, tags=tags, companies=companies
        )

        self.assertEqual(embedded.leads[0].id, 1)
        self.assertEqual(embedded.contacts[0].id, 2)
        self.assertTrue(embedded.contacts[0].is_main)
        self.assertEqual(embedded.tags[0].name, "Tag1")
        self.assertEqual(embedded.companies[0].id, 3)

    def test_default_values_embedded_object(self):
        embedded = EmbeddedObject()
        self.assertEqual(embedded.leads, [])
        self.assertEqual(embedded.contacts, [])
        self.assertEqual(embedded.tags, [])
        self.assertEqual(embedded.companies, [])


class TestLeadObject(TestCase):

    def setUp(self):
        self.embedded = EmbeddedObject(
            leads=[EmbeddedLead(id=1)],
            contacts=[EmbeddedContact(id=2, is_main=True)],
            tags=[TagObject(id=1, name="Tag1", color="blue")],
            companies=[EmbeddedCompany(id=3)],
        )
        self.valid_data = {
            "id": 1,
            "name": "Test Lead",
            "price": 1000,
            "responsible_user_id": 10,
            "group_id": 1,
            "status_id": 2,
            "pipeline_id": 3,
            "loss_reason_id": 4,
            "source_id": 5,
            "created_by": 6,
            "updated_by": 7,
            "closed_at": 8,
            "created_at": 100,
            "updated_at": 100,
            "closest_task_at": 100,
            "is_deleted": False,
            "custom_fields_values": [
                TextCustomFieldObject(
                    field_code="TextField",
                    field_name="Test-Name",
                    field_type="text",
                    values=[],
                )
            ],
            "score": None,
            "account_id": 123,
            "labor_cost": 500,
            "is_price_modified_by_robot": False,
            "embedded": self.embedded,
        }

    def test_valid_lead_object(self):
        lead = LeadObject(**self.valid_data)
        self.assertEqual(lead.id, 1)
        self.assertEqual(lead.name, "Test Lead")
        self.assertEqual(lead.price, 1000)
        self.assertEqual(lead.embedded.leads[0].id, 1)

    def test_invalid_custom_field(self):
        invalid_data = self.valid_data.copy()
        invalid_data["custom_fields_values"] = "InvalidType"
        with self.assertRaises(DataclassValidationError):
            LeadObject(**invalid_data)

    def test_invalid_id_type(self):
        invalid_data = self.valid_data.copy()
        invalid_data["id"] = "invalid_id"
        with self.assertRaises(DataclassValidationError):
            LeadObject(**invalid_data)

    def test_invalid_price_type(self):
        invalid_data = self.valid_data.copy()
        invalid_data["price"] = "one thousand"
        with self.assertRaises(DataclassValidationError):
            LeadObject(**invalid_data)

    def test_invalid_dates(self):
        invalid_data = self.valid_data.copy()
        invalid_data["created_at"] = "not a datetime"
        with self.assertRaises(DataclassValidationError):
            LeadObject(**invalid_data)

    def test_optional_score(self):
        valid_data = self.valid_data.copy()
        valid_data["score"] = 100
        lead = LeadObject(**valid_data)
        self.assertEqual(lead.score, 100)


class TestContactObject(TestCase):

    def setUp(self):
        self.embedded = EmbeddedObject(
            leads=[EmbeddedLead(id=1)],
            contacts=[EmbeddedContact(id=2, is_main=True)],
            tags=[TagObject(id=1, name="Tag1", color="blue")],
            companies=[EmbeddedCompany(id=3)],
        )
        self.valid_data = {
            "id": 1,
            "name": "John Doe",
            "first_name": "John",
            "last_name": "Doe",
            "responsible_user_id": 10,
            "group_id": 1,
            "created_by": 6,
            "updated_by": 7,
            "created_at": datetime(2024, 10, 20, 12, 0, 0),
            "updated_at": datetime(2024, 10, 21, 12, 0, 0),
            "closest_task_at": datetime(2024, 10, 22, 12, 0, 0),
            "custom_fields_values": [],
            "account_id": 123,
            "embedded": self.embedded,
        }

    def test_valid_contact_object(self):
        contact = ContactObject(**self.valid_data)
        self.assertEqual(contact.name, "John Doe")
        self.assertEqual(contact.first_name, "John")
        self.assertEqual(contact.last_name, "Doe")
        self.assertEqual(contact.embedded.leads[0].id, 1)

    def test_optional_first_name_last_name(self):
        data = self.valid_data.copy()
        data["first_name"] = None
        data["last_name"] = None
        contact = ContactObject(**data)
        self.assertIsNone(contact.first_name)
        self.assertIsNone(contact.last_name)

    def test_invalid_id_type(self):
        data = self.valid_data.copy()
        data["id"] = "invalid_id"
        with self.assertRaises(DataclassValidationError):
            ContactObject(**data)

    def test_invalid_closest_task_at(self):
        data = self.valid_data.copy()
        data["closest_task_at"] = "invalid_date"
        with self.assertRaises(DataclassValidationError):
            ContactObject(**data)


class TestCatalogItem(TestCase):

    def setUp(self):
        self.embedded = EmbeddedObject()
        self.valid_data = {
            "id": 1,
            "catalog_id": 101,
            "name": "Test Item",
            "created_by": 6,
            "updated_by": 7,
            "created_at": datetime(2024, 10, 20, 12, 0, 0),
            "updated_at": datetime(2024, 10, 21, 12, 0, 0),
            "custom_fields_values": [],
            "account_id": 123,
            "embedded": self.embedded,
        }

    def test_valid_catalog_item(self):
        catalog_item = CatalogItem(**self.valid_data)
        self.assertEqual(catalog_item.id, 1)
        self.assertEqual(catalog_item.catalog_id, 101)
        self.assertEqual(catalog_item.name, "Test Item")

    def test_invalid_catalog_item_id(self):
        data = self.valid_data.copy()
        data["id"] = "invalid_id"
        with self.assertRaises(DataclassValidationError):
            CatalogItem(**data)

    def test_invalid_created_at(self):
        data = self.valid_data.copy()
        data["created_at"] = "invalid_date"
        with self.assertRaises(DataclassValidationError):
            CatalogItem(**data)

    def test_optional_custom_fields_values(self):
        data = self.valid_data.copy()
        data["custom_fields_values"] = []
        catalog_item = CatalogItem(**data)
        self.assertEqual(catalog_item.custom_fields_values, [])
