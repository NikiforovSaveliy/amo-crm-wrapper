import datetime
import unittest

from amopy.exceptions import DataclassValidationError
from amopy.objects.custom_fields import (
    TextCustomFieldObject,
    NumericCustomFieldObject,
    CheckboxCustomFieldObject,
    SelectCustomFieldObject,
    DateTimeCustomFieldObject,
)
from amopy.objects.entities import LeadObject, EmbeddedObject, ContactObject
from amopy.objects.factories import (
    init_custom_field_object,
    init_lead_object,
    init_contact_object,
)
from tests.mocks import contact_mock


class TestInitCustomFieldObject(unittest.TestCase):

    def test_text_custom_field(self):
        data = {
            "field_name": "Test Field",
            "field_type": "text",
            "field_id": 1,
            "values": [{"value": "test text"}],
        }
        result = init_custom_field_object(data)
        self.assertIsInstance(result, TextCustomFieldObject)
        self.assertEqual(result.field_name, "Test Field")
        self.assertEqual(result.field_id, 1)
        self.assertEqual(result.values[0].value, "test text")

    def test_numeric_custom_field(self):
        data = {
            "field_name": "Numeric Field",
            "field_type": "numeric",
            "field_id": 2,
            "values": [{"value": "123"}],
        }
        result = init_custom_field_object(data)
        self.assertIsInstance(result, NumericCustomFieldObject)
        self.assertEqual(result.field_name, "Numeric Field")
        self.assertEqual(result.field_id, 2)
        self.assertEqual(result.values[0].value, "123")

    def test_checkbox_custom_field(self):
        data = {
            "field_name": "Checkbox Field",
            "field_type": "checkbox",
            "field_id": 3,
            "values": [{"value": True}],
        }
        result = init_custom_field_object(data)
        self.assertIsInstance(result, CheckboxCustomFieldObject)
        self.assertEqual(result.field_name, "Checkbox Field")
        self.assertEqual(result.field_id, 3)
        self.assertEqual(result.values[0].value, True)

    def test_select_custom_field(self):
        data = {
            "field_name": "Select Field",
            "field_type": "select",
            "field_id": 4,
            "values": [{"value": "option1"}],
        }
        result = init_custom_field_object(data)
        self.assertIsInstance(result, SelectCustomFieldObject)
        self.assertEqual(result.field_name, "Select Field")
        self.assertEqual(result.field_id, 4)
        self.assertEqual(result.values[0].value, "option1")

    def test_multiselect_custom_field(self):
        data = {
            "field_name": "MultiSelect Field",
            "field_type": "multiselect",
            "field_id": 5,
            "values": [{"value": "option1"}, {"value": "option2"}],
        }
        result = init_custom_field_object(data)
        self.assertIsInstance(result, SelectCustomFieldObject)
        self.assertEqual(result.field_name, "MultiSelect Field")
        self.assertEqual(result.field_id, 5)
        self.assertEqual(result.values[0].value, "option1")
        self.assertEqual(result.values[1].value, "option2")

    def test_date_custom_field(self):
        date = datetime.datetime.now()
        data = {
            "field_name": "Date Field",
            "field_type": "data",
            "field_id": 6,
            "values": [{"value": date.isoformat()}],
        }
        result = init_custom_field_object(data)
        self.assertIsInstance(result, DateTimeCustomFieldObject)
        self.assertEqual(result.field_name, "Date Field")
        self.assertEqual(result.field_id, 6)
        self.assertEqual(result.values[0].value, date)

    def test_missing_field_type(self):
        data = {
            "field_name": "Missing Field Type",
            "field_id": 7,
            "values": [{"value": "test"}],
        }
        with self.assertRaises(DataclassValidationError):
            init_custom_field_object(data)

    def test_invalid_field_type(self):
        data = {
            "field_name": "Invalid Field Type",
            "field_type": "invalid_type",
            "field_id": 8,
            "values": [{"value": "test"}],
        }
        with self.assertRaises(DataclassValidationError):
            init_custom_field_object(data)

    def test_invalid_field_data(self):
        data = {
            "field_name": "Invalid Field Data",
            "field_type": "select",
            "field_id": 8,
            "values": [{}],
        }
        with self.assertRaises(DataclassValidationError):
            init_custom_field_object(data)


class TestInitLeadObject(unittest.TestCase):

    def setUp(self):
        self.valid_data = {
            "id": 3912171,
            "name": "Example",
            "price": 12,
            "responsible_user_id": 504141,
            "group_id": 0,
            "status_id": 143,
            "pipeline_id": 3104455,
            "loss_reason_id": 4203748,
            "source_id": None,
            "created_by": 504141,
            "updated_by": 504141,
            "created_at": 1585299171,
            "updated_at": 1590683337,
            "closed_at": 1590683337,
            "closest_task_at": None,
            "is_deleted": False,
            "custom_fields_values": None,
            "score": None,
            "account_id": 28805383,
            "is_price_modified_by_robot": False,
            "_embedded": {
                "tags": [
                    {
                        "id": 100667,
                        "name": "тест",
                        "color": None,
                    }
                ],
                "catalog_elements": [
                    {"id": 525439, "metadata": {"quantity": 1, "catalog_id": 4521}}
                ],
                "loss_reason": [
                    {
                        "id": 4203748,
                        "name": "Пропала потребность",
                        "sort": 100000,
                        "created_at": 1582117280,
                        "updated_at": 1582117280,
                    }
                ],
                "companies": [{"id": 10971463}],
                "contacts": [{"id": 10971465, "is_main": True}],
            },
        }

    def test_valid_lead_object(self):
        lead = init_lead_object(self.valid_data)
        self.assertIsInstance(lead, LeadObject)
        self.assertEqual(lead.id, 3912171)
        self.assertEqual(lead.name, "Example")
        self.assertEqual(lead.price, 12)
        self.assertEqual(lead.responsible_user_id, 504141)
        self.assertEqual(lead.pipeline_id, 3104455)
        self.assertEqual(lead.loss_reason_id, 4203748)
        self.assertEqual(lead.is_deleted, False)
        self.assertEqual(lead.custom_fields_values, [])

        self.assertEqual(len(lead.embedded.tags), 1)
        self.assertEqual(lead.embedded.tags[0].id, 100667)
        self.assertEqual(lead.embedded.tags[0].name, "тест")

        self.assertEqual(len(lead.embedded.companies), 1)
        self.assertEqual(lead.embedded.companies[0].id, 10971463)

        self.assertEqual(len(lead.embedded.contacts), 1)
        self.assertEqual(lead.embedded.contacts[0].id, 10971465)
        self.assertTrue(lead.embedded.contacts[0].is_main)

    def test_missing_embedded_data(self):
        data = self.valid_data.copy()
        data.pop("_embedded")
        lead = init_lead_object(data)
        self.assertIsInstance(lead.embedded, EmbeddedObject)
        self.assertEqual(len(lead.embedded.contacts), 0)
        self.assertEqual(len(lead.embedded.companies), 0)
        self.assertEqual(len(lead.embedded.tags), 0)

    def test_invalid_custom_fields(self):
        data = self.valid_data.copy()
        data["custom_fields_values"] = "invalid"
        with self.assertRaises(DataclassValidationError):
            init_lead_object(data)


class TestInitContactObject(unittest.TestCase):

    def setUp(self):
        self.valid_data = contact_mock

    def test_valid_contact_object(self):
        contact = init_contact_object(self.valid_data)
        self.assertIsInstance(contact, ContactObject)
        self.assertEqual(contact.id, 3)
        self.assertEqual(contact.name, "Иван Иванов")
        self.assertEqual(contact.first_name, "Иван")
        self.assertEqual(contact.last_name, "Иванов")
        self.assertEqual(contact.responsible_user_id, 504141)
        self.assertEqual(contact.created_by, 504141)
        self.assertEqual(contact.account_id, 28805383)

        self.assertEqual(len(contact.custom_fields_values), 1)
        self.assertEqual(contact.custom_fields_values[0].field_name, "Телефон")
        self.assertEqual(contact.custom_fields_values[0].values[0].value, "+79123")
        self.assertEqual(contact.custom_fields_values[0].values[0].enum_code, "WORK")

        self.assertEqual(len(contact.embedded.leads), 2)
        self.assertEqual(contact.embedded.leads[0].id, 1)
        self.assertEqual(contact.embedded.leads[1].id, 3916883)

        self.assertEqual(len(contact.embedded.companies), 1)
        self.assertEqual(contact.embedded.companies[0].id, 1)

        self.assertEqual(len(contact.embedded.tags), 0)

    def test_missing_embedded_data(self):
        data = self.valid_data.copy()
        data.pop("_embedded")
        contact = init_contact_object(data)
        self.assertIsInstance(contact.embedded, EmbeddedObject)
        self.assertEqual(len(contact.embedded.leads), 0)
        self.assertEqual(len(contact.embedded.companies), 0)
        self.assertEqual(len(contact.embedded.tags), 0)

    def test_invalid_custom_fields(self):
        data = self.valid_data.copy()
        data["custom_fields_values"] = "invalid"
        with self.assertRaises(DataclassValidationError):
            init_contact_object(data)

    def test_no_custom_fields(self):
        data = self.valid_data.copy()
        data["custom_fields_values"] = []
        contact = init_contact_object(data)
        self.assertIsInstance(contact, ContactObject)
        self.assertEqual(len(contact.custom_fields_values), 0)


if __name__ == "__main__":
    unittest.main()
