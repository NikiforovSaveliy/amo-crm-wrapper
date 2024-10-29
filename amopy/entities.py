from abc import abstractmethod
from typing import Annotated

from amopy.fields import BodyField


class BaseEntity:

    @property
    @abstractmethod
    def entity_type(self):
        pass

    def __init__(self, **attrs):
        for attr, value in attrs.items():
            setattr(self, attr, value)


class LeadEntity(BaseEntity):

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
