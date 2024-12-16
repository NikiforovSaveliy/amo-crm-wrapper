from typing import Union


class ImproperlyConfiguredField(Exception):

    def __init__(self, klass, reason: str):
        super().__init__(f"{klass.__class__.__name__} improperly configured: {reason}")


class CustomField:
    __slots__ = ("field_id", "field_code", "value_object", "many")

    def __init__(
        self,
        *,
        field_id: Union[int, None] = None,
        field_code: Union[str, None] = None,
        value_object=None,
        many: bool,
    ):

        if not (field_id or field_code):
            raise ImproperlyConfiguredField(
                self, "field_id or field_code should be set"
            )

        self.field_id = field_id
        self.field_code = field_code
        self.many = many
        self.value_object = value_object
