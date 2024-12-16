from typing import Union, Annotated

from amopy.values import TextValue


class ImproperlyConfiguredField(Exception):

    def __init__(self, klass, reason: str):
        super().__init__(f"{klass.__class__.__name__} improperly configured: {reason}")


class CustomField:
    __slots__ = ("field_id", "field_code", "value_object", "many")

    def __init__(
        self,
        *,
        field_id: Union[int, None] = None,
        value_object=None,
        many: bool,
    ):
        self.field_id = field_id
        self.many = many
        self.value_object = value_object


def TextField(field_id: int):  # noqa
    return Annotated[
        str, CustomField(field_id=field_id, value_object=TextValue, many=False)
    ]
