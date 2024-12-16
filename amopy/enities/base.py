from abc import abstractmethod
from dataclasses import dataclass
from typing import Literal


@dataclass
class BaseEntity:

    # TODO: Добавить после остальные типы
    @abstractmethod
    @property
    def type(self) -> Literal["leads", "contacts"]:
        pass
