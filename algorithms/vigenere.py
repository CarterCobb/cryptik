from cryptark import Cryptark
from functools import reduce
from math import gcd, ceil
from log import log
import re
from algorithms.frequency_analysis import FrequencyAnalysisSimple
from algorithms.caesar import Caesar
from colorama import init, Fore, Style

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alphabet_frequencies = [l for l in alphabet]
letter_frequencies = [8.2,1.5,2.8,4.3,13,2.2,2,6.1,7,0.15,0.77,4,2.4,6.7,7.5,1.9,0.095,6,6.3,9.1,2.8,0.98,2.4,0.15,2,0.074]
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
        common_phrases = ['UFEIUJPGP', 'PLRLFSFNPB', 'VZUL', 'JPGP']
        key_len = self._common_factor(common_phrases, message)
        possible_letters = []
        print('Key length:',key_len)
        chunked = [message[i:i + key_len] for i in range(0, len(message), key_len)]
        for n in range(0, key_len):
            msg = ''
            try:
                for chunk in chunked: msg += chunk[n]
            except: pass
            new_ln = '\r\n\r\n' if n > 0 else ''
            log.info(f"{new_ln}{'+' * 60} L{n + 1} {'+' * 60}\r\n")
            log.algo(f"{' ' * 20} General Frequencies{' ' * 20}{' ' * 25} Key[{n}] Frequencies{' ' * 20}")
            freq, lrg_perc, lrg_ltr_cnt, f_mapped = FrequencyAnalysisSimple().get_frequencies(msg)
            possible_letters.append(self._print_chart(freq, lrg_perc, lrg_ltr_cnt, f_mapped, n))
        return f"\r\nPossible Key: {''.join(possible_letters)}; uses letters: {', '.join(possible_letters)}"

    def _common_phrases(self, message) -> list[str]:
        set_sizes = [4, 5, 6, 7, 8]
        chunks = []
        for offset in range(0, len(message)):
            for s in set_sizes:
                chunks = [message[i:i + s] for i in range(0, len(message), s)]
                print(chunks)
        pass

    def _common_factor(self, common_phrases, message) -> int:
        factors = [abs(reduce(lambda x, y: x - y, [i.start() for i in re.finditer(phrase, message)][:2])) for phrase in common_phrases]
        return reduce(gcd, factors)

    def _round_up(self, x):
        return int(ceil(x / 5.0)) * 5
        
    def _print_chart(self, freqencies, largest_percent, lrg_ltr_cnt, f_mapped, index):
        log.info(f'Most Prominent Letter: {Fore.YELLOW}{lrg_ltr_cnt}')
        shift_alphabet_e = Caesar()._shift([chr(i + 65) for i in range(0,26)], 30 - ord(lrg_ltr_cnt) - 65)
        a_indicies = [shift_alphabet_e.index('A')]
        line_count = self._round_up(largest_percent)
        lines = [[' ' for _ in range(len(freqencies))] for _ in range(line_count + 1)]
        basic_lines = [[' ' for _ in range(len(freqencies))] for _ in range(line_count + 1)]
        for l in range(0, line_count):
            for f in range(0, len(freqencies)):
                if freqencies[f][list(freqencies[f].keys())[0]]['percent'] >= l: lines[l][f] = 'X'
                else: lines[l][f] = ' '
                if letter_frequencies[f] >= l: basic_lines[l][f] = 'X'
                else: basic_lines[l][f] = ' '
        for l in range(len(lines) - 1, 0, -1):
            chart_line = ''.join(f"{l}{' ' if l >= 10 else '  '}| {' '.join(basic_lines[l])}")
            chart_line += '    *    '
            chart_line += ''.join(f"{l}{' ' if l >= 10 else '  '}| {' '.join(lines[l])}")
            print(chart_line)
        print(f"{'-' * 56}    *    {'-' * 56}")
        alphabet_str = [list(f.keys())[0] for f in freqencies]
        print(f"     {' '.join(alphabet_str)}    *         {' '.join([f'{Fore.GREEN}{alphabet_str[l]}' if l in a_indicies else f'{Fore.WHITE}{alphabet_str[l]}' for l in range(0,len(alphabet_str))])}")
        key_line1 = f"     {' ' * ((len(alphabet_str) * 2) - 1)}    *    E:   {' '.join([f'{Fore.YELLOW}{l}' if l == 'A' else f'{Fore.WHITE}{l}' for l in shift_alphabet_e])}"
        print(key_line1)
        # possible_u = 0
        # while True:
        #     try:
        #         i_input = int(input('What inxex should `U` be placed?\r\n-> '))
        #         if i_input < 0 or i_input > 25: raise Exception()
        #         possible_u = i_input
        #         break
        #     except:
        #         print('invlaid index: [0-25]')
        # shift_alphabet_b = Caesar()._shift([chr(i + 65) for i in range(0,26)], possible_u + 2)
        # print(f"     {' '.join(alphabet_str)}    *         {' '.join([f'{Fore.GREEN}{alphabet_str[l]}' if l in a_indicies else f'{Fore.WHITE}{alphabet_str[l]}' for l in range(0,len(alphabet_str))])}")
        # key_line1 = f"     {' ' * ((len(alphabet_str) * 2) - 1)}    *    E:   {' '.join([f'{Fore.YELLOW}{l}' if l == 'A' else f'{Fore.WHITE}{l}' for l in shift_alphabet_e])}"
        # print(key_line1)
        # key_line2 = f"     {' ' * ((len(alphabet_str) * 2) - 1)}    *    U:   {' '.join([f'{Fore.YELLOW}{l}' if l == 'A' else f'{Fore.WHITE}{l}' for l in shift_alphabet_b])}"
        # print(key_line2)
        # a_indicies.append(shift_alphabet_b.index('A'))
        # while True:
        #     try:
        #         i_input = input('Continue? [y/n]\r\n-> ')
        #         if i_input.lower() == 'y' or i_input.lower() == 'n': 
        #             if i_input.lower() == 'y': break
        #         else: raise Exception()
        #     except:
        #         print('invlaid input [y/n]')
        possible_letters = [f'{alphabet_str[l]}' for l in range(0,len(alphabet_str)) if l in a_indicies]
        print(f'Possible Key[{index}] values:', ', '.join(possible_letters))
        return possible_letters[0]

    def _find_valley_index(self, valley, f_mapped):
        # print(valley)
        # print(f_mapped)
        threshold_idicies = []
        subset_i = []
        for i in range(0, len(f_mapped)):
            if f_mapped[i] <= 3.5 :
                threshold_idicies.append(i)
        print(threshold_idicies)
        for i in threshold_idicies:
            try:
                if f_mapped[i + 1] <= 3.5:
                    subset_i.append(i)
            except:
                if f_mapped[0] <= 3.5:
                    subset_i.append(0)
        print(subset_i)
        
       