from cryptark import Cryptark
from log import log

class Reverse(Cryptark):

    def encode(self, message: str, _) -> str:
        return self.decode(message)

    def decode(self, message: str) -> str:
        log.info(f'IN: {message}')
        message = ''.join(filter(str.isalnum, message)).upper()
        return ''.join([f' {message[i]}' if i % 5 == 0 else message[i] for i in range(len(message))][::-1])