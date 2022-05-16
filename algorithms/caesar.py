from cryptark import Cryptark

class Caesar(Cryptark):

    def encode(self, message: str, encode_args: list[str]) -> str:
        message = ''.join(filter(str.isalnum, message)).upper()
        alphabet, cipher = self._main_logic('encode', encode_args)
        return ''.join([cipher[alphabet.index(l)] for l in message])

    def decode(self, message: str, decode_args: list[str]) -> str:
        message = ''.join(filter(str.isalnum, message)).upper()
        alphabet, cipher = self._main_logic('encode', decode_args)
        return ''.join([alphabet[cipher.index(l)] for l in message])

    def _shift(self, seq, n):
        n = n % len(seq)
        return seq[n:] + seq[:n]

    def _main_logic(self, args):
        key = int(args[0])
        alphabet = [chr(i + 65) for i in range(0,26)]
        cipher = self._shift(alphabet, key)
        print('plain: ', alphabet)
        print('cipher:',cipher) 
        return alphabet, cipher
