from cryptark import Cryptark
from log import log
import re
import random
import string

# 
# Learn about this cypher: https://en.wikipedia.org/wiki/Bacon%27s_cipher
# 

class Bacon(Cryptark):
    """
    Original bacon Cypher
    """
    
    def encode(self, message, encode_args) -> str:
        """
            @param: `message` = the hidden message to encode. e.g: "KILL NO ONE"
            @param: `encode_args[0]` = the string to encode the `message` into. e.g. "did somebody say bacon? there's nothing more delicious"
            @returns: from example: "dIdsOmEbodySaYbaCoNthEResnOThInGMoReDEliciOus"
        """
        message = ''.join(filter(str.isalnum, message)).upper()
        encode_args[0] = ''.join(filter(str.isalnum, encode_args[0])).lower()
        if encode_args[0] is None: encode_args[0] = ''
        if len(message) * 5 != len(encode_args[0]): 
            log.warn(f'Message & hide string are invalid proportional sizes; {"truncating hide string" if (len(message) * 5 < len(encode_args[0])) else "adding extra character(s) to hide string."}') 
        if len(message) * 5 < len(encode_args[0]): hide_str = encode_args[0][0:(len(message) * 5)]
        else: hide_str = ''.join(re.findall('.....',f"{encode_args[0]}{''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(abs(len(message) * 5 - len(encode_args[0]))))}"))
        log.info(f'Hiding `{message}` in `{hide_str}`')
        binary = ''.join([f"{'0' * (5 - len(bin(l).replace('0b', '')))}{bin(l).replace('0b', '')}" for l in [ord(m) - (65 if ord(m) < 75 else 66 if ord(m) < 87 else 67) for m in message]])
        return ''.join([hide_str[i] if binary[i] != '1' else hide_str[i].upper() for i in range(len(binary))])

    def decode(self, message: str) -> str:
        message = ''.join(filter(str.isalnum, message))
        if len(message) % 5 != 0: log.warn('Message not divisible by 5; will be truncated.')
        log.general(re.findall('.....', message))
        pre_ascii = [int(v, 2) for v in [''.join(f) for f in [['0' if ord(l) > 90 else '1' for l in c] for c in re.findall('.....', message)]]]
        log.general([f"{'0' * (5 - len(bin(i).replace('0b', '')))}{bin(i).replace('0b', '')}" for i in pre_ascii])
        log.warn('Varible letters like (I, J, U, V) are represented by `-`')
        return ''.join(['-' if l in [8, 19] else chr(l + (65 if l < 9 else 66 if l < 20 else 67)) for l in pre_ascii])

class NewBacon(Cryptark):
    """
    New Bacon is the version of Bacon's cypher that makes varible letters 
    (I, J, U, V) have specific binary representations.
    """

    def encode(self, message, encode_args) -> str:
        """
            @param: `message` = the hidden message to encode. e.g: "KILL NO ONE"
            @param: `encode_args[0]` = the string to encode the `message` into. e.g. "did somebody say bacon? there's nothing more delicious"
            @returns: from example: "dIdSomEbodySaYBaCoNThEReSnOTHinGMOreDElIciOus"
        """
        message = ''.join(filter(str.isalnum, message)).upper()
        encode_args[0] = ''.join(filter(str.isalnum, encode_args[0])).lower()
        if encode_args[0] is None: encode_args[0] = ''
        if len(message) * 5 != len(encode_args[0]): 
            log.warn(f'Message & hide string are invalid proportional sizes; {"truncating hide string" if (len(message) * 5 < len(encode_args[0])) else "adding extra character(s) to hide string."}') 
        if len(message) * 5 < len(encode_args[0]): hide_str = encode_args[0][0:(len(message) * 5)]
        else: hide_str = ''.join(re.findall('.....',f"{encode_args[0]}{''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(abs(len(message) * 5 - len(encode_args[0]))))}"))
        log.info(f'Hiding `{message}` in `{hide_str}`')
        binary = ''.join([f"{'0' * (5 - len(bin(l).replace('0b', '')))}{bin(l).replace('0b', '')}" for l in [ord(m) - 65 for m in message]])
        return ''.join([hide_str[i] if binary[i] != '1' else hide_str[i].upper() for i in range(len(binary))])

    def decode(self, message: str) -> str:
        message = ''.join(filter(str.isalnum, message))
        if len(message) % 5 != 0: log.warn('Message not divisible by 5; will be truncated.')
        log.general(re.findall('.....', message))
        pre_ascii = [int(v, 2) for v in [''.join(f) for f in [['0' if ord(l) > 90 else '1' for l in c] for c in re.findall('.....', message)]]]
        log.general([f"{'0' * (5 - len(bin(i).replace('0b', '')))}{bin(i).replace('0b', '')}" for i in pre_ascii])
        return ''.join([chr(letter + 65) for letter in pre_ascii])
