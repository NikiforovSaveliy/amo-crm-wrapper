from unittest import TestCase

from amopy.entities import LeadEntity
from amopy.mapper import BaseMapper
from tests.mocks import lead_mock


class TestBaseMapper(TestCase):

    def setUp(self):
        self.mock_data = lead_mock
        self.mapper = BaseMapper(LeadEntity)

    def test_from_dict(self):
        mapped_entity: LeadEntity = self.mapper.from_dict(self.mock_data)
        self.assertEqual(mapped_entity.id, self.mock_data["id"])
        self.assertEqual(mapped_entity.created_by, self.mock_data["created_by"])
        self.assertEqual(mapped_entity.updated_by, self.mock_data["updated_by"])
        self.assertEqual(mapped_entity.name, self.mock_data["name"])
        self.assertEqual(mapped_entity.price, self.mock_data["price"])

    def test_to_dict(self):
        mapped_entity = LeadEntity(
            id=self.mock_data["id"],
            created_by=self.mock_data["created_by"],
            name=self.mock_data["name"],
        )

        converted_entity = self.mapper.to_dict(mapped_entity)

        self.assertEqual(converted_entity["id"], self.mock_data["id"])
        self.assertEqual(converted_entity["created_by"], self.mock_data["created_by"])
        self.assertEqual(converted_entity["name"], self.mock_data["name"])
