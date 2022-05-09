import re
from cryptark import Cryptark
import math

class Transposition(Cryptark):

    def encode(self, message: str, encode_args) -> str: 
        message = ''.join(filter(str.isalnum, message))
        key = int(encode_args[0])
        ciphertext = [''] * key 
        for col in range(key):  
            pointer = col   
            while pointer < len(message):   
                ciphertext[col] += message[pointer] 
                pointer += key  
        return ''.join(ciphertext)

    def decode(self, message: str, decode_args) -> str:
        message = ''.join(filter(str.isalnum, message))
        numOfRows = int(decode_args[0])
        numOfColumns = math.ceil(len(message) / numOfRows)
        numOfShadedBoxes = (numOfColumns * numOfRows) - len(message)
        plaintext = [''] * numOfColumns
        col,row = 0, 0
        for symbol in message:
            plaintext[col] += symbol
            col += 1
            if (col == numOfColumns) or (col == numOfColumns - 1 and row >= numOfRows - numOfShadedBoxes):
                col = 0
                row += 1
        return ''.join(plaintext)