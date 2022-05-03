from abc import ABC, abstractmethod
from typing import List
from log import log

class Cryptark(ABC):

    @abstractmethod
    def encode(self, message: str, encode_args: List[str]) -> str:
        log.error('Not implemented :/')
        pass

    @abstractmethod
    def decode(self, message: str) -> str:
        log.error('Not implemented :/')
        pass