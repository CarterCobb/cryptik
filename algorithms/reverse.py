from base64 import decode
from cryptark import Cryptark

class Reverse(Cryptark):

    def encode(self, message: str, _) -> str:
        return self.decode(message)

    def decode(self, message: str) -> str:
        message = ''.join(filter(str.isalnum, message)).upper()
        return ''.join([f' {message[i]}' if i % 5 == 0 else message[i] for i in range(len(message))][::-1])