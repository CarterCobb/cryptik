import json
import re
import os
from turtle import back
from cryptark import Cryptark
from log import log
import yaml

class Concealment(Cryptark):

    def encode(self, message: str, encode_args) -> str:
        # Use nltk to get words to generate sentences 
        return super().encode(message, encode_args)

    def decode(self, message: str) -> str:
        log.warn('Results varry and will output all possibliites in YAML format.')
        log.info(f'IN: {message}')
        return '\r\n' + yaml.dump({
            'last_char': self._last_char(message),
            'stair_case': self._staircase(message),
            'stair_reverse': self._staircase_reverse(message),
            'double_helix': self._double_helix(message),
            'helix_joined': self._double_helix_joined(message),
            'stair_n': self._staticase_n_based(message),
            'n_letter': self._letter_based(message),
            'n_letter_w_offest': self._n_offset(message),
        }, default_flow_style=False, sort_keys=False)

    # ---------------------------- TYPES ----------------------------

    def _letter_based(self, message):
        min_m = self._min_word(message)
        log.warn(f'Smallest `n` length is {min_m}; will not calculate beyond that length')
        res = [{'n': i + 1, 'res': ''} for i in range(min_m)]
        for n in range(min_m):
            for word in self._safe_split(message):
                res[n]['res'] += word[n]
        return res

    def _n_offset(self, message): 
        message = ''.join(filter(str.isalnum, message))
        min_of, max_of = 0, len(message) - 1
        res = []
        while min_of != max_of:
            for i in range(1, max_of):
                res.append({
                    'offest': i - 1,
                    'possibilities': [{'n': j - 1, 'res': message[i::j]} for j in range(1, len(message))]
                })
            min_of += 1
        with open('n_offest.json', 'w') as f: f.write(json.dumps(res))
        return 'See output file `n_offset.json`'

    def _last_char(self, message) -> str:
        return ''.join([''.join(filter(str.isalnum, f))[-1:] for f in message.split(' ')])

    def _staircase(self, message, i = 0):
        res = ''
        for word in self._safe_split(message):
            if i > len(word) - 1: i = 0
            res += word[i]
            i += 1
        return res
    
    def _staircase_reverse(self, message):
        split_m = self._safe_split(message)
        i = len(split_m[0]) - 1
        res = split_m[0][i]
        for word in split_m[1:]:
            if i - 1 < len(word) - 1 and i - 1 > 0: i -= 1
            elif i - 1 == 0: i -= 1
            else: i = len(word) - 1
            res += word[i]
        return res

    def _staticase_n_based(self, message):
        min_m = self._min_word(message)
        res = [{'n': i + 1, 'res': ''} for i in range(min_m)]
        for n in range(min_m):
            res[n]['res'] = self._staircase(message, n)
        return res

    def _double_helix(self, message):
        return {
            'helix_n_1': self._staircase(message),
            f'helix_n_{len(self._safe_split(message)[0])}': self._staircase_reverse(message)
        }

    def _double_helix_joined(self, message):
        a_helix = self._staircase(message)
        b_helix = self._staircase_reverse(message)
        return ''.join([a_helix[i] + b_helix[i] for i in range(len(a_helix))])

    # ---------------------------- HELPERS ----------------------------

    def _safe_split(self, message) -> str:
        return [''.join(filter(str.isalnum, f)) for f in message.split(' ')]

    def _min_word(self, message) -> str:
        return len(min(self._safe_split(message), key=len))
