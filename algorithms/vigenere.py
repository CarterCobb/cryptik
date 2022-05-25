from cryptark import Cryptark
from functools import reduce
from math import gcd
import re
from algorithms.frequency_analysis import FrequencyAnalysisSimple

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letter_to_i = dict(zip(alphabet, range(len(alphabet))))
i_to_letter = dict(zip(range(len(alphabet)), alphabet))

class Vigenere(Cryptark):

    def encode(self, message: str, encode_args: list[str]) -> str:
        space_indecies = self._find_spaces(message)
        key, message = self._clean_text(encode_args[0]), self._clean_text(message)
        key_set = (key * int(len(message) / len(key) + 0.5))[:len(message)]
        encripted = ''
        for s in self._split(message, key):
            i = 0
            for l in s:
                number = (letter_to_i[l] + letter_to_i[key[i]]) % len(alphabet)
                encripted += i_to_letter[number]
                i += 1
        encripted = self._join_spaces(space_indecies, encripted)
        key_set = self._join_spaces(space_indecies, key_set)
        m_final = self._join_spaces(space_indecies, message)
        return f'ENCODE->\r\nkey map: {key_set}\r\nplain:   {m_final}\r\ncipher:  {encripted}'

    def decode(self, message: str, decode_args: list[str]) -> str:
        space_indecies = self._find_spaces(message)
        key, message = self._clean_text(decode_args[0]), self._clean_text(message)
        key_set = (key * int(len(message) / len(key) + 0.5))[:len(message)]
        decripted = ''
        for s in self._split(message, key):
            i = 0
            for l in s:
                number = (letter_to_i[l] - letter_to_i[key[i]]) % len(alphabet)
                decripted += i_to_letter[number]
                i += 1
        decripted = self._join_spaces(space_indecies, decripted)
        key_set = self._join_spaces(space_indecies, key_set)
        m_final = self._join_spaces(space_indecies, message)
        return f'DECODE->\r\nkey map: {key_set}\r\nplain:   {decripted}\r\ncipher:  {m_final}'

    def _find_spaces(self, message) -> list[int]:
        return [i.start() for i in re.finditer(' ', message)]

    def _clean_text(self, text) -> str:
        return ''.join(filter(str.isalnum, text)).upper()
    
    def _split(self, message, key) -> list[str]:
        return [message[i:i + len(key)] for i in range(0, len(message), len(key))]

    def _join_spaces(self, space_indecies, text) -> str:
        for i in space_indecies: text = text[:i] + ' ' + text[i:]
        return text


class HackVigenere(Cryptark): 

    def encode(self, message: str, encode_args: list[str]) -> str:
        return super().encode(message, encode_args)

    def decode(self, message: str, decode_args: list[str]) -> str:
        message = ''.join(filter(str.isalnum, message)).upper()
        common_phrases = ['EFIQ', 'PSDLP', 'WCXYM', 'ETRL']
        key_len = self._common_factor(common_phrases, message) 
        chunked = [message[i:i + key_len] for i in range(0, len(message), key_len)]
        for n in range(0, key_len):
            FrequencyAnalysisSimple().analize(message[n::n + 1])
        return super().decode(message, decode_args)

    def _common_phrases(self, message) -> list[str]:
        set_sizes = [4, 5, 6, 7, 8]
        chunks = []
        for offset in range(0, len(message)):
            for s in set_sizes:
                chunks = [message[i:i + s] for i in range(0, len(message), s)]
                print(chunks)
        pass

    def _common_factor(self, common_phrases, message) -> int:
        factors = [abs(reduce(lambda x, y: x - y, [i.start() for i in re.finditer(phrase, message)])) for phrase in common_phrases]
        return reduce(gcd, factors)
        
            
