class DataclassValidationError(Exception):
    """
    Ошибка валидаций перед проверкой
    """

    def __init__(self, msg):
        super().__init__(msg)


class ValueObjectValidationError(Exception):
    pass


class CustomFieldObjectValidationError(Exception):
    pass


class DataclassFieldRequiredError(DataclassValidationError):
    pass
