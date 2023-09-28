from sys import argv
import numpy as np
import os

def build_rule_elem(digit_list):
    if not digit_list:
        return 'tl'
    return 'cons ' + digit_list[0] + ' (' + build_rule_elem(digit_list[1:]) + ')'

def build_rule(lhs, rhs):
    o = ''
    o += '[tl] '
    o += build_rule_elem(lhs)
    o += ' --> '
    o += build_rule_elem(rhs)
    o += '.\n'
    return o

def gen_rules(base1, base2):
    base1_digits = [np.base_repr(i, base1) for i in range(base1)]
    base2_digits = [np.base_repr(i, base2) for i in range(base2)]
    output = \
'\
Digit   : Type.\n\
ListOfDigits : Type.\n\
Nil : ListOfDigits.\n\
b : Digit.\n\
def cons : Digit -> ListOfDigits -> ListOfDigits.\n\
'
    for digit in base1_digits:
        output += digit + 't : Digit. \n'
    for digit in base2_digits:
        output += digit + ' : Digit. \n'
    output += '\n'

    output += \
    build_rule(['b', '0'], ['b'])

    for v, digit in enumerate(base2_digits[1:], 1):
        o_digit1 = v // base1
        o_digit2 = v % base1
        output += build_rule(['b', digit], ['b', base2_digits[o_digit1], base1_digits[o_digit2] + 't'])
    for i1, digit1 in enumerate(base1_digits):
        for i2, digit2 in enumerate(base2_digits):
            v = i1 * base2 + i2
            o_digit1 = v // base1
            o_digit2 = v % base1
            output += build_rule([digit1 + 't', digit2], [base2_digits[o_digit1], base1_digits[o_digit2] + 't'])
    name = 'convert_' +str(base2)+'_'+str(base1)+'.dk'
    with open(name, 'w') as file:
        file.write(output)
    os.system('dk check -e ' + name)

gen_rules(int(argv[2]), int(argv[1]))