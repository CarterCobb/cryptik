from operator import index
from cryptark import Cryptark

WEIGHTS = ['E','T','A','O','I','N','S','H','R','D','L','C','U','M','W','F','G','Y','P','B','V','K','J','X','Q','Z']

class FrequencyAnalysis(Cryptark):

    def encode(self, message: str, encode_args: list[str]) -> str:
        return super().encode(message, encode_args)

    def decode(self, message: str, decode_args: list[str]) -> str:
        message = ''.join(filter(str.isalnum, message)).upper()
        print('Length:',len(message))
        alpha_map = [{f'{chr(i + 65)}': {'count': 0, 'percent': 0}} for i in range(0, 26)]
        for l in message:
            i = 0
            for i_ in range(0, len(alpha_map)):
                if l in alpha_map[i_]: i = i_
            alpha_map[i][l]['count'] = alpha_map[i][l]['count'] + 1
            alpha_map[i][l]['percent'] = (alpha_map[i][l]['count'] / len(message)) * 100
        res = sorted(alpha_map, key = lambda i: list(i.values())[0]['count'], reverse=True)
        print('general: ', WEIGHTS)
        final_map = [list(i.keys())[0] for i in res]
        print('proposed:',final_map)
        formatted_message = ''
        for l in message:
            formatted_message += WEIGHTS[final_map.index(l)]
        print(formatted_message)
        return super().decode(message, decode_args)