from sys import argv

def build_list(cons, digits):
    res = cons + ' b ('
    for d in digits:
        res += cons + ' '+ d + ' ('
    res += 'Nil'
    for _ in digits:
        res += ')'
    return res + ').'
print(build_list('cons', argv[1]))