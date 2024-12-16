from abc import abstractmethod
from typing import Literal


class BaseEntity:

    # TODO: Добавить после остальные типы
    @property
    @abstractmethod
    def type(self) -> Literal["leads", "contacts"]:
        pass

    def __init__(self, **initial_state):
        for key, value in initial_state.items():
            setattr(self, key, value)
