# Cryptik Cryptography Helper

This is a simple cryptography encoder and decoder that will ahve various algorithms added to it as time moves on.

## Supported Algorithms

| Algorithm |
| --------- |
| Bacon's Cypher |
| New Bacon's Cypher |

## Usage

The syntax is the same for each algrithm. It is subject to change as more cyphers are added. If the base `program.py` script is run without arguments it will guide you through the process of adding your custom properties.

```shell
usage: program.py [-h] [-a ALGORITHM] [-e] [-d] [-m MESSAGE] ...

Cryptik Cryptography Helper

positional arguments:
  args

options:
  -h, --help            show this help message and exit
  -a ALGORITHM, --algo ALGORITHM
                        Algoritm to use. e.g. bacon
  -e, --encode          Set wether the program encodes the message. default: False
  -d, --decode          Set wether the program decodes the message
  -m MESSAGE, --message MESSAGE
                        Message to process
```

### Example

Say we have the cypher: `dId sOmEbody SaY baCoN? thERe’s nOThInG MoRe DEliciOus.`. Lets use Bacon's Cypher as an example:

#### Decode

```shell
python program.py --algo bacon --decode --message "dId sOmEbody SaY baCoN? thERe’s nOThInG MoRe DEliciOus."
```

Simplified:

```shell
python program.py -a bacon -d -m "dId sOmEbody SaY baCoN? thERe’s nOThInG MoRe DEliciOus."
```

Output:

```shell
['dIdsO', 'mEbod', 'ySaYb', 'aCoNt', 'hERes', 'nOThI', 'nGMoR', 'eDEli', 'ciOus']
['01001', '01000', '01010', '01010', '01100', '01101', '01101', '01100', '00100']
WARNING: Varible letters like (I, J, U, V) are represented by `-`
RESULT: K-LLNOONE
```

#### Encode

```shell
python program.py -a bacon -e -m "KILLNOONE" "did somebody say bacon? theres nothing more delicious."
```

Output:

```shell
Hiding `KILLNOONE` in `didsomebodysaybacontheresnothingmoredelicious`
RESULT: dIdsOmEbodySaYbaCoNthEResnOThInGMoReDEliciOus
```
