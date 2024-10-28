from typing import Dict

from amopy.entities import EntityType


class BaseMapper:

    def __init__(self, entity: EntityType):
        self._entity = entity

    def map(self, data: Dict):
        pass
