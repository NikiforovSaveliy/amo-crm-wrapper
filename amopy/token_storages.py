from abc import ABC, abstractmethod
from typing import Dict


class AbstractTokenStorage(ABC):

    @abstractmethod
    def get_access_token(self) -> str:
        pass

    @abstractmethod
    def get_auth_header(self) -> Dict[str, str]:
        pass


class LongTermTokenStorage(AbstractTokenStorage):

    def __init__(self, long_term_token: str):
        self.long_term_token = long_term_token

    def get_access_token(self):
        return self.long_term_token

    def get_auth_header(self) -> Dict[str, str]:
        return {"Authentication": "Bearer " + self.long_term_token}
