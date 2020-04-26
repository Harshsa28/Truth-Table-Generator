import parser

hades = {}
index = 0

def put_in_hash(ATOMS):
    global hades, index
    #print("hades is :", hades, " and index is :", index)
    for i in ATOMS:
        hades[i] = index
        index += 1
    #print("hades is :", hades, " and index is :", index)

def table(p):
    global hades , index
    #print("hades is :", hades, " and index is :", index)
    if p.LAST == None and p.RAST == None:
        return hades[p.symbol]
    lst = ""
    lst = lst + str(p.symbol) + ' '
    #lst.append(p.symbol)
    if p.symbol == "not":
        lst = lst + str(table(p.RAST)) + ' '
        #lst.append(table(p.RAST))
        if lst not in hades:
            hades[lst] = index
            index += 1
    else:
        num1 = table(p.LAST)
        num2 = table(p.RAST)
        if num1 < num2:
            lst = lst + str(num1) + ' ' + str(num2) + ' '
        else:
            lst = lst + str(num2) + ' ' + str(num1) + ' '

        #lst = lst + str(table(p.LAST)) + ' '
        #lst.append(table(p.LAST))
        #lst = lst + str(table(p.RAST)) + ' '
        #lst.append(table(p.RAST))
        if lst not in hades:
            hades[lst] = index
            index += 1
    #print("hades is :", hades, " and index is :", index)
    return hades[lst]



def achilles():
    [p, ATOMS] = parser.fire()
    put_in_hash (ATOMS)
    table(p)
    return [hades , ATOMS]


#print(achilles())
