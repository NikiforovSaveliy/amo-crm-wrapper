from dataclasses import dataclass


@dataclass
class TextValue:
    value: str

    def get_value(self):
        return self.value
