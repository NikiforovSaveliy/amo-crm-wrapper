from datetime import datetime
from unittest import TestCase

from amopy.exceptions import DataclassValidationError, DataclassFieldRequiredError
from amopy.objects.values import (
    TextValue,
    BooleanValue,
    DateTimeValue,
    EnumValue,
    LegalEntityValue,
    LinkedEntityValue,
)


class TestTextValue(TestCase):

    def test_valid_data(self):
        instance = TextValue(value="test")
        self.assertEqual(instance.value, "test")

    def test_invalid_value(self):
        with self.assertRaises(DataclassValidationError):
            instance = TextValue(value=123)


class TestBooleanValue(TestCase):
    def test_boolean_value(self):
        instance = BooleanValue(value=True)
        self.assertTrue(instance.value)

    def test_invalid_value(self):
        with self.assertRaises(DataclassValidationError):
            instance = BooleanValue(value=123)


class TestDateTimeValue(TestCase):

    def setUp(self):
        self.test_date = datetime.now()

    def test_date_time_value(self):

        instance = DateTimeValue(value=self.test_date)
        self.assertEqual(instance.value, self.test_date)

    def test_timestamp_value(self):
        instance = DateTimeValue(value=self.test_date.timestamp())
        self.assertEqual(instance.value, self.test_date)

    def test_iso_format_value(self):
        instance = DateTimeValue(value=self.test_date.isoformat())
        self.assertEqual(instance.value, self.test_date)

    def test_invalid_value(self):
        with self.assertRaises(DataclassValidationError):
            instance = DateTimeValue(value="Just random strig to ")


class TestEnumValue(TestCase):
    def test_value(self):

        instance = EnumValue(value="Test")
        self.assertEqual(instance.value, "Test")

    def test_enum_id_value(self):
        instance = EnumValue(enum_id=123)
        self.assertEqual(instance.enum_id, 123)

    def test_enum_code_value(self):

        instance = EnumValue(enum_code="Test")
        self.assertEqual(instance.enum_code, "Test")

    def test_invalid_value(self):

        with self.assertRaises(DataclassValidationError):
            instance = EnumValue(value=123)

        with self.assertRaises(DataclassValidationError):
            instance = EnumValue(enum_id="not integer:) ")

        with self.assertRaises(DataclassValidationError):
            instance = EnumValue(enum_code=123)

    def test_required_values(self):
        with self.assertRaises(DataclassFieldRequiredError):
            instance = EnumValue()


class TestLegalEntityValue(TestCase):

    def test_valid_data(self):
        entity = LegalEntityValue(
            name="Test Entity",
            entity_type=123,
            vat_id="123456789",
            tax_registration_reason_code=12,
            address="123 Main St",
            kpp="987654",
            external_uid="abc-123",
        )
        self.assertEqual(entity.name, "Test Entity")

    def test_invalid_name_type(self):
        with self.assertRaises(DataclassValidationError):
            LegalEntityValue(name=123)

    def test_invalid_entity_type(self):
        with self.assertRaises(DataclassValidationError):
            LegalEntityValue(name="Valid Name", entity_type="Not an int")

    def test_invalid_vat_id_type(self):
        with self.assertRaises(DataclassValidationError):
            LegalEntityValue(name="Valid Name", vat_id=12345)

    def test_invalid_tax_registration_reason_code_type(self):
        with self.assertRaises(DataclassValidationError):
            LegalEntityValue(
                name="Valid Name", tax_registration_reason_code="Not an int"
            )  # Ожидается int

    def test_invalid_address_type(self):
        with self.assertRaises(DataclassValidationError):
            LegalEntityValue(name="Valid Name", address=12345)

    def test_invalid_kpp_type(self):
        with self.assertRaises(DataclassValidationError):
            LegalEntityValue(name="Valid Name", kpp=12345)

    def test_invalid_external_uid_type(self):
        with self.assertRaises(DataclassValidationError):
            LegalEntityValue(name="Valid Name", external_uid=12345)


class TestLinkedEntityValue(TestCase):

    def test_valid_data(self):
        entity = LinkedEntityValue(
            name="Test Entity", entity_id=1, entity_type="contacts", catalog_id=123
        )
        self.assertEqual(entity.name, "Test Entity")
        self.assertEqual(entity.entity_id, 1)
        self.assertEqual(entity.entity_type, "contacts")
        self.assertEqual(entity.catalog_id, 123)

    def test_invalid_name_type(self):
        with self.assertRaises(DataclassValidationError):
            LinkedEntityValue(name=123, entity_id=1, entity_type="contacts")

    def test_invalid_entity_id_type(self):
        with self.assertRaises(DataclassValidationError):
            LinkedEntityValue(
                name="Valid Name", entity_id="Not an int", entity_type="contacts"
            )

    def test_invalid_entity_type_value(self):
        with self.assertRaises(DataclassValidationError):
            LinkedEntityValue(
                name="Valid Name", entity_id=1, entity_type="invalid_type"
            )

    def test_invalid_catalog_id_type(self):
        with self.assertRaises(DataclassValidationError):
            LinkedEntityValue(
                name="Valid Name",
                entity_id=1,
                entity_type="contacts",
                catalog_id="Not an int",
            )
