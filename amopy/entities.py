from abc import abstractmethod
from typing import TypeVar, Annotated

from amopy.fields import BodyField
from amopy.objects.custom_fields import BaseCustomFieldObject


class BaseEntity:

    @property
    @abstractmethod
    def entity_type(self):
        pass


EntityType = TypeVar("EntityType", bound=BaseEntity)


class LeadEntity(BaseCustomFieldObject):

    id: Annotated[int, BodyField(alias="id")]
    created_by: Annotated[int, BodyField(alias="created_by")]
    updated_by: Annotated[int, BodyField(alias="updated_by")]
    account_id: Annotated[int, BodyField(alias="account_id")]
    name: Annotated[str, BodyField(alias="name", changeable=True)]
    price: Annotated[int, BodyField(alias="price", changeable=True)]
    responsible_user_id: Annotated[
        int, BodyField(alias="responsible_user_id", changeable=True)
    ]
    loss_reason_id: Annotated[int, BodyField(alias="loss_reason_id", changeable=True)]
    closed_at: Annotated[int, BodyField(alias="closed_at", changeable=True)]

    entity_type = "leads"
