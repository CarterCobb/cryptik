from cryptark import Cryptark
import re
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letter_to_i = dict(zip(alphabet, range(len(alphabet))))
i_to_letter = dict(zip(range(len(alphabet)), alphabet))

class Vigenere(Cryptark):

    def encode(self, message: str, encode_args: list[str]) -> str:
        space_indecies = self._find_spaces(message)
        key, message = self._clean_text(encode_args[0]), self._clean_text(message)
        encripted = ''
        for s in self._split(message, key):
            i = 0
            for l in s:
                number = (letter_to_i[l] + letter_to_i[key[i]]) % len(alphabet)
                encripted += i_to_letter[number]
                i += 1
                if i in space_indecies: encripted += ' '
        return encripted

    def decode(self, message: str, decode_args: list[str]) -> str:
        space_indecies = self._find_spaces(message)
        key, message = self._clean_text(decode_args[0]), self._clean_text(message)
        decripted = ''
        for s in self._split(message, key):
            i = 0
            for l in s:
                number = (letter_to_i[l] - letter_to_i[key[i]]) % len(alphabet)
                decripted += i_to_letter[number]
                i += 1
                if i in space_indecies: decripted += ' '
        return decripted

    def _find_spaces(self, message) -> list[int]:
        return [i.start() for i in re.finditer(' ', message)]

    def _clean_text(self, text) -> str:
        return ''.join(filter(str.isalnum, text)).upper()
    
    def _split(self, message, key) -> list[str]:
        return [message[i:i + len(key)] for i in range(0, len(message), len(key))]