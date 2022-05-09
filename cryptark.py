from abc import ABC, abstractmethod
from log import log

class Cryptark(ABC):

    @abstractmethod
    def encode(self, message: str, encode_args: list[str]) -> str:
        log.error('Not implemented :/')
        pass

    @abstractmethod
    def decode(self, message: str, decode_args: list[str]) -> str:
        log.error('Not implemented :/')
        pass