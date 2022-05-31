from cryptark import Cryptark


class RSA(Cryptark):

    def encode(self, message: str, encode_args: list[str]) -> str:
        return super().encode(message, encode_args)

    def decode(self, message: str, decode_args: list[str]) -> str:
        return super().decode(message, decode_args)
