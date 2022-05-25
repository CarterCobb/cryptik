from cryptark import Cryptark
import re
from log import log

WEIGHTS = ['E','T','A','O','I','N','S','H','R','D','L','C','U','M','W','F','G','Y','P','B','V','K','J','X','Q','Z'] # Most common weight 

class FrequencyAnalysis(Cryptark):

    def encode(self, message: str, encode_args: list[str]) -> str:
        return super().encode(message, encode_args)

    def decode(self, message: str, decode_args: list[str]) -> str:
        message = ''.join(re.sub(r'[^a-zA-Z\s]', u'', message, flags=re.UNICODE).upper().splitlines()) 
        print('Length:',len(message))
        alpha_map = [{f'{chr(i + 65)}': {'count': 0, 'percent': 0}} for i in range(0, 26)]
        for l in message:
            if not l.isspace():
                i = 0
                for i_ in range(0, len(alpha_map)):
                    if l in alpha_map[i_]: i = i_
                alpha_map[i][l]['count'] = alpha_map[i][l]['count'] + 1
                alpha_map[i][l]['percent'] = (alpha_map[i][l]['count'] / len(message)) * 100
        res = sorted(alpha_map, key = lambda i: list(i.values())[0]['count'], reverse=True)
        for m in res: print(m)
        final_map = [list(i.keys())[0] for i in res]
        print('frequencies:',final_map)
        log.info(f'MSSAGE: {message}')  
        self._calculate(message, final_map)
        while True:
            try:
                shuffle = input("Swap letters? ['L1 L2' to swap] ['done' to end]\r\n-> ")
                if shuffle.lower().strip() == 'done': break
                letters = shuffle.upper().split(' ')
                i1, i2 = WEIGHTS.index(letters[0]), WEIGHTS.index(letters[1])
                WEIGHTS[i1], WEIGHTS[i2] = WEIGHTS[i2], WEIGHTS[i1]
                self._calculate(message, final_map)
                letter_map = dict(zip(WEIGHTS, final_map)) 
                sorted_letter_map = {key:letter_map[key] for key in sorted(letter_map)}
                print(f"\r\nplain:  {' '.join(sorted_letter_map.keys())}\r\ncipher: {' '.join([sorted_letter_map[i] for i in sorted_letter_map.keys()])}")
            except: print("Invlaid Try again")
        letter_map = dict(zip(WEIGHTS, final_map)) 
        sorted_letter_map = {key:letter_map[key] for key in sorted(letter_map)}
        return f"\r\nplain:  {' '.join(sorted_letter_map.keys())}\r\ncipher: {' '.join([sorted_letter_map[i] for i in sorted_letter_map.keys()])}"

    def _calculate(self, message, final_map): 
        formatted_message = ''
        for l in message:
            if not l.isspace():
                formatted_message += WEIGHTS[final_map.index(l)]
            else: formatted_message += l

        log.success(formatted_message)

class FrequencyAnalysisSimple:

    def analize(self, message):
        message = ''.join(re.sub(r'[^a-zA-Z\s]', u'', message, flags=re.UNICODE).upper().splitlines()) 
        print(f'\r\n{message}')
        alpha_map = [{f'{chr(i + 65)}': {'count': 0, 'percent': 0}} for i in range(0, 26)]
        for l in message:
            if not l.isspace():
                i = 0
                for i_ in range(0, len(alpha_map)):
                    if l in alpha_map[i_]: i = i_
                alpha_map[i][l]['count'] = alpha_map[i][l]['count'] + 1
                alpha_map[i][l]['percent'] = (alpha_map[i][l]['count'] / len(message)) * 100
        res = sorted(alpha_map, key = lambda i: list(i.values())[0]['count'], reverse=True)
        final_map = [list(i.keys())[0] for i in res]
        # print(' '.join(final_map))
        # print(f"{' '.join(WEIGHTS)}\r\n{' '.join(final_map)}")
        letter_map = dict(zip(WEIGHTS, final_map)) 
        sorted_letter_map = {key:letter_map[key] for key in sorted(letter_map)}
        print(f"plain:  {' '.join(sorted_letter_map.keys())}\r\ncipher: {' '.join([sorted_letter_map[i] for i in sorted_letter_map.keys()])}")
        