from cryptark import Cryptark
from log import log

"""
Key pairs:
{1,1}
{5,21}
{7,15}
{9,3}
{11,19}
{17,23}
{25,25}
"""

class Multiplicative(Cryptark):

    def encode(self, message: str, encode_args: list[str]) -> str:
        message = ''.join(filter(str.isalnum, message)).upper()
        alphabet, cipher = self._main_logic(encode_args)
        return ''.join([cipher[alphabet.index(l)] for l in message])

    def decode(self, message: str, decode_args: list[str]) -> str:
        message = ''.join(filter(str.isalnum, message)).upper()
        alphabet, cipher = self._main_logic(decode_args)
        return ''.join([alphabet[cipher.index(l)] for l in message])
    
    def _main_logic(self, args):
        key = int(args[0])
        if key % 2 == 0 or key == 13:
            log.error('Not relatively prime to the mod (26) or key is 13; cannot be a common factor')
            return [chr(i + 65) for i in range(0,26)], [chr(i + 65) for i in range(0,26)]
        alphabet = [chr(i + 65) for i in range(0,26)]
        cipher = [chr(((i * key) % 26) + 65) for i in range(0, 26)]
        print('plain: ', alphabet)
        print('cipher:',cipher) 
        return alphabet, cipher


class Affine(Cryptark):

    def encode(self, message: str, encode_args: list[str]) -> str:
        message = ''.join(filter(str.isalnum, message)).upper()
        alphabet, cipher = self._main_logic(encode_args)
        return ''.join([cipher[alphabet.index(l)] for l in message])

    def decode(self, message: str, decode_args: list[str]) -> str:
        message = ''.join(filter(str.isalnum, message)).upper()
        alphabet, cipher = self._main_logic(decode_args)
        return ''.join([alphabet[cipher.index(l)] for l in message])
    
    def _main_logic(self, args):
        main_key = int(args[0])
        multi = int(main_key / 26)
        shift = main_key % 26
        print(multi, shift)
        if multi % 2 == 0 or multi == 13:
            log.error('Not relatively prime to the mod (26) or key is 13; cannot be a common factor')
            return [chr(i + 65) for i in range(0,26)], [chr(i + 65) for i in range(0,26)]
        alphabet = [chr(i + 65) for i in range(0,26)]
        print('plain: ', alphabet)
        cipher = [chr(((i * multi) % 26) + 65) for i in range(0, 26)]
        print(f'mulit{multi}:', cipher)
        cipher = [alphabet[((i * multi) + shift) % 26] for i in range(0, 26)]
        print('cipher:',cipher) 
        return alphabet, cipher

