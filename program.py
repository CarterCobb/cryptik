import subprocess
import sys
import pprint

pp = pprint.PrettyPrinter(indent=2)
packages = ['inquirer','art','colorama','pyyaml', 'nltk']
reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed = [r.decode().split('==')[0].lower() for r in reqs.split()]
to_install = set(packages) - set(installed)

if len(to_install) > 0:
  print('Installing dependencies:')
  for p in to_install: print(f'  - {p}')
  proc = subprocess.run([sys.executable, '-m', 'pip', 'install'] + list(to_install), capture_output=True, text=True)
  if proc.returncode > 0:
    pp.pprint(proc.stdout)
    pp.pprint(proc.stderr)
    quit(proc.returncode)
  else: print('Installed required dependancies.')

import inquirer
from art import *
from log import log
import argparse
from algorithms.bacon import Bacon, NewBacon
from algorithms.reverse import Reverse
from algorithms.concealment import Concealment
from algorithms.transposition import Transposition
from algorithms.caesar import Caesar
from algorithms.multiplicative import Multiplicative, Affine, AffineBruteForce
from algorithms.frequency_analysis import FrequencyAnalysis
from algorithms.vigenere import Vigenere, HackVigenere

class Criptak:

    def __init__(self):
        log.art(text2art('Cryptik  Cryptography  Helper', font='cybermedium'))
        parser = argparse.ArgumentParser(description='Cryptik Cryptography Helper')
        parser.add_argument('-a', '--algo', dest='algorithm', default=None, type=str, help='Algoritm to use. e.g. bacon')
        parser.add_argument('-e', '--encode', dest='encode', default=None, action='store_true', help='Set wether the program encodes the message. default: False')
        parser.add_argument('-d', '--decode', dest='decode', default=None, action='store_true', help='Set wether the program decodes the message')
        parser.add_argument('-m', '--message', dest='message', type=str, help='Message to process')
        parser.add_argument('args', nargs=argparse.REMAINDER)
        args = parser.parse_args()
        self.__dict__ = vars(args)

        get_algo = lambda: self.algorithm if self.algorithm is not None else inquirer.prompt([inquirer.List('algorithm', message='Choose an algorithm', choices=
            ['bacon', 'new-bacon', 'conceal' 'reverse', 'transposition', 'caesar', 'multi', 'affine', 'affine-hack', 'freq', 'vig', 'hack-vig']
        )])['algorithm']
        get_encode = lambda: self.encode if self.encode is not None else inquirer.confirm(message='Set to encode?')
        get_decode = lambda: self.decode if self.decode is not None else inquirer.confirm(message='Set to decode?')
        get_message = lambda: self.message if self.message is not None else inquirer.text(message='Enter a message')
        self.algorithm = get_algo()
        
        while True:
            if self.encode or self.decode: break
            e, d = get_encode(), None
            if not e: d = get_decode()
            if (e is not None and e) or (d is not None and d): 
                self.encode = e
                self.decode = d
                break
        self.message = get_message()

        log.info("Using the following algorithm:")
        log.algo(text2art(self.algorithm, font='tarty2'))

        if self.algorithm == 'bacon': self.algorithm = Bacon()
        elif self.algorithm == 'new-bacon': self.algorithm = NewBacon()
        elif self.algorithm == 'reverse': self.algorithm = Reverse()
        elif self.algorithm == 'conceal': self.algorithm = Concealment()
        elif self.algorithm == 'transposition': self.algorithm = Transposition()
        elif self.algorithm == 'caesar': self.algorithm = Caesar()
        elif self.algorithm == 'multi': self.algorithm = Multiplicative()
        elif self.algorithm == 'affine': self.algorithm = Affine()
        elif self.algorithm == 'affine-hack': self.algorithm = AffineBruteForce()
        elif self.algorithm == 'freq': self.algorithm = FrequencyAnalysis()
        elif self.algorithm == 'vig': self.algorithm = Vigenere()
        elif self.algorithm == 'hack-vig': self.algorithm = HackVigenere()
        else: raise RuntimeError(f'Algorithm `{self.algorithm}` not found')

        if self.encode: log.success(self.algorithm.encode(self.message, self.args))
        elif self.decode: log.success(self.algorithm.decode(self.message, self.args))
        else: raise RuntimeError('Must specify encode or decode')

if __name__ == '__main__': Criptak()