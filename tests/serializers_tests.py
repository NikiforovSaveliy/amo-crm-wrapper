from typing import Annotated
from unittest import TestCase

from amopy.body_fields import BodyField
from amopy.custom_fields import TextField
from amopy.enities import Lead
from amopy.serializers import EntitySerializer


class TestEntityClass(Lead):
    body_field: Annotated[int, BodyField("body_field")]
    text_field: TextField(123)


class TestSerializers(TestCase):

    def setUp(self):
        self.mock_data = {
            "body_field": 123,
            "custom_fields_values": [
                {
                    "field_id": 123,
                    "field_code": "Just boring text field",
                    "values": [{"value": "Test"}],
                }
            ],
        }

    def test_serialize(self):
        serializer = EntitySerializer(TestEntityClass)
        entity_instance = TestEntityClass(body_field=123, text_field="123")
        serialized = serializer.to_response(entity_instance)
        self.assertEqual(serialized["body_field"], 123)
        self.assertEqual(serialized["custom_fields_values"][0]["field_id"], 123)
        self.assertEqual(
            serialized["custom_fields_values"][0]["values"][0]["value"], "123"
        )

    def test_deserialize(self):
        serializer = EntitySerializer(TestEntityClass)
        entity_instance = serializer.from_response(self.mock_data)
        self.assertEqual(entity_instance.body_field, 123)
        self.assertEqual(entity_instance.text_field, "Test")
