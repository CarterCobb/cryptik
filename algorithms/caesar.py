from cryptark import Cryptark

class Caesar(Cryptark):

    def encode(self, message: str, encode_args: list[str]) -> str:
        message = ''.join(filter(str.isalnum, message)).upper()
        key = int(encode_args[0])
        alphabet = [chr(i + 65) for i in range(0,26)]
        cipher = self._shift(alphabet, key)
        print(alphabet)
        print(cipher)
        return ''.join([cipher[alphabet.index(l)] for l in message])

    def decode(self, message: str, decode_args: list[str]) -> str:
        message = ''.join(filter(str.isalnum, message)).upper()
        key = int(decode_args[0])
        alphabet = [chr(i + 65) for i in range(0,26)]
        cipher = self._shift(alphabet, key)
        print(alphabet)
        print(cipher)
        return ''.join([alphabet[cipher.index(l)] for l in message])

    def _shift(self, seq, n):
        n = n % len(seq)
        return seq[n:] + seq[:n]
