from cryptark import Cryptark
from algorithms.helpers.rabinmiller import generate_large_prime
from algorithms.helpers.math import mod_inverse
from math import gcd
import os, random
from log import log

DEFAULT_BLOCK_SIZE = 128 # 1024 bits
BYTE_SIZE = 256

# Textbook RSA. NOT secure for real world applications.
class RSA(Cryptark):

    def encode(self, message: str, encode_args: list[str]) -> str:
        try: block_size, byte_size = int(encode_args[0]), int(encode_args[1])
        except: block_size, byte_size = DEFAULT_BLOCK_SIZE, BYTE_SIZE
        key_size, n, e = self._read_key_file('keys/pubkey.txt')
        if key_size < block_size * 8:
            log.error(f'Block size is {block_size * 8} bits and key size is {key_size} bits.')
            return None
        encrypted_blocks = [str(pow(block, e, n)) for block in self._get_blocks_from_text(message, block_size, byte_size)]
        return f"\r\n{len(message)}_{block_size}_{','.join(encrypted_blocks)}"

    def decode(self, message: str, decode_args: list[str]) -> str:
        prv_file = 'keys/prvkey.txt'
        key_size, n, d = self._read_key_file(prv_file)
        message_len, block_size, e_message = message.split('_')
        if key_size < int(block_size) * 8:
            log.error(f'Block size is {int(block_size) * 8} bits and key size is {key_size} bits.')
            return None
        decrypted_blocks = [pow(b, d, n) for b in [int(block) for block in e_message.split(',')]]
        return self._get_text_from_blocks(decrypted_blocks, int(message_len), int(block_size))

    def _read_key_file(self, file_name):
        with open(file_name, 'r') as f:
            key_size, n, EorD = f.read().split(',')
        return (int(key_size), int(n), int(EorD))

    def _get_blocks_from_text(self, message, block_size, byte_size):
        bytes = message.encode('ascii')
        block_ints = []
        for block_s in range(0, len(bytes), block_size):
            block_int = 0
            for i in range(block_s, min(block_s + block_size, len(bytes))):
                block_int += bytes[i] * (byte_size ** (i % block_size))
            block_ints.append(block_int)
        return block_ints

    def _get_text_from_blocks(self, block_ints, message_len, block_size):
        message = []
        for block_int in block_ints:
            blockMessage = []
            for i in range(block_size - 1, -1, -1):
                if len(message) + i < message_len:
                    asciiNumber = block_int // (BYTE_SIZE ** i)
                    block_int = block_int % (BYTE_SIZE ** i)
                    blockMessage.insert(0, chr(asciiNumber))
            message.extend(blockMessage)
        return ''.join(message)

class RSAKeyGen(Cryptark):

    def encode(self, message: str, encode_args: list[str]) -> str:
        key_size = int(message)
        p = generate_large_prime(key_size)
        q = generate_large_prime(key_size)
        n = p * q
        while True:
            e = random.randrange(2 ** (key_size - 1), 2 ** (key_size))
            if gcd(e, (p - 1) * (q - 1)) == 1: break
        d = mod_inverse(e, (p - 1) * (q - 1))
        pub, prv = 'keys/pubkey.txt', 'keys/prvkey.txt'
        os.makedirs(os.path.dirname(pub), exist_ok=True)
        os.makedirs(os.path.dirname(prv), exist_ok=True)
        with open(pub, 'w') as f: f.write(f'{key_size},{n},{e}')
        with open(prv, 'w') as f: f.write(f'{key_size},{n},{d}')
        return f'Generated at: keys/pubkey.txt & keys/prvkey.txt'


    def decode(self, message: str, decode_args: list[str]) -> str:
        return super().decode(message, decode_args)
