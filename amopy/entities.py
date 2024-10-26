from abc import abstractmethod

from amopy.objects.custom_fields import BaseCustomFieldObject


class BaseEntity:

    @property
    @abstractmethod
    def entity_type(self):
        pass


class LeadEntity(BaseCustomFieldObject):
    entity_type = "leads"
