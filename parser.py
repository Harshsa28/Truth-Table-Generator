import sys
class AST:
    def __init__(self, LAST, RAST, symbol):
        self.LAST = LAST
        self.RAST = RAST
        self.symbol = symbol

ATOMS = set()

def get_atom(string, index):
    global ATOMS
    while (string[index] == ' '):
        index += 1
    atom = ""
    while ((index < len(string)) and string[index].isalnum()):
        atom += string[index]
        index += 1
    ATOMS.add(atom)
    return [string, index, atom]



def get_sym(string, index):
    while (string[index] == ' '):
        index += 1
    symbol = ""
    while (string[index].isalpha()):
        symbol += string[index]
        index += 1
    return [string, index, symbol]

def check_not (string, index):
    symbol = ""
    [string, index, symbol] = get_sym (string, index);
    if symbol == "not":
        return 1
    else:
        return 0



def parse(string, index): 
    while (string[index] == ' '):
        index += 1
    if string[index] == ')':
        print("error in string[index] in parse")
        sys.exit()
    if string[index] != '(':
        atom = ""
        [string, index, atom] = get_atom (string , index)
        p = AST(None, None, atom)
        return [string, index, p]
    if string[index] == '(':
        index += 1
    if check_not (string , index) == 0:
        [string, index, LAST] = parse (string, index)
    else:
        LAST = None
    [string, index, symbol] = get_sym(string, index)
    [string, index, RAST] = parse (string, index)
    p = AST (LAST, RAST, symbol)
    
    while (string[index] == ' '):
        index += 1
    if string[index] == ')':
        index += 1
    else:
        print("error 765")
        sys.exit()
    return [string, index, p]

def print_AST(p):
    if p is None:
        print(p)
        return
    print(p.symbol)
    print_AST (p.LAST)
    print_AST (p.RAST)


def fire():
    string = str(input("give formula : "))
    index = 0
    [string, index, p] = parse (string, index)
    return [p, ATOMS]





