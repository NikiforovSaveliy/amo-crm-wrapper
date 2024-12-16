from dataclasses import dataclass
from amopy.enities import base


@dataclass
class Lead(base.BaseEntity):

    @property
    def type(self):
        return "leads"