import columns
from tabulate import tabulate

def create_atoms_cols (ATOMS):
    num_atoms = len(ATOMS)
    num_rows = 2 ** num_atoms
    atoms_cols = [[] for x in range (num_atoms)]
    atoms_cols_index = 0
    for i in range(num_atoms):
        atom = [-1 for x in range (num_rows)]
        atom_index = 0
        block = 2 ** i
        TF = int(num_rows / (2 ** (i + 1)))
        for j in range (block):
            for t in range (TF):
                atom[atom_index] = 1
                atom_index += 1
            for f in range (TF):
                atom[atom_index] = 0
                atom_index += 1
        atoms_cols[atoms_cols_index] = atom
        atoms_cols_index += 1
    return atoms_cols

def _and (hash_table_list , index1, index2 , fire , ATOMS):
    col1 = fire[index1]
    col2 = fire[index2]
    num_rows = 2 ** len(ATOMS)
    col_and = [-1 for x in range (num_rows)]
    col_and_index = 0
    for i in range(num_rows):
        col_and[col_and_index] = col1[col_and_index] * col2[col_and_index]
        col_and_index += 1
    return col_and

def _or (hash_table_list , index1 , index2 , fire , ATOMS):
    col1 = fire[index1]
    col2 = fire[index2]
    num_rows = 2 ** len(ATOMS)
    col_or = [-1 for x in range (num_rows)]
    col_or_index = 0
    for i in range(num_rows):
        if col1[col_or_index] + col2[col_or_index] > 0:
            col_or[col_or_index] = 1
        else:
            col_or[col_or_index] = 0
        col_or_index += 1
    return col_or

def _implies (hash_table_list , index1 , index2 , fire , ATOMS):
    col1 = fire[index1]
    col2 = fire[index2]
    num_rows = 2 ** len(ATOMS)
    col_implies = [-1 for x in range (num_rows)]
    col_implies_index = 0
    for i in range(num_rows):
        if col1[col_implies_index] == 1 and col2[col_implies_index] == 0:
            col_implies[col_implies_index] = 0
        else:
            col_implies[col_implies_index] = 1
        col_implies_index += 1
    return col_implies

def _not (hash_table_list , index1 , fire , ATOMS):
    col1 = fire[index1]
    num_rows = 2 ** len(ATOMS)
    col_not = [-1 for x in range (num_rows)]
    col_not_index = 0
    for i in range(num_rows):
        if col1[col_not_index] == 1:
            col_not[col_not_index] = 0
        else:
            col_not[col_not_index] = 1
        col_not_index += 1
    return col_not

def create_derived_cols (hash_table , ATOMS, fire , fire_index):
    num_atoms = len(ATOMS)
    num_rows = 2 ** num_atoms
    num_derived = len(hash_table) - num_atoms
    hash_table_index = num_atoms
    hash_table_list = list(hash_table)
    for i in range (num_derived):
        string = hash_table_list[hash_table_index]
        hash_table_index += 1
        lst = string.split(' ')
        if lst[0] == 'and':
            fire[fire_index] = _and (hash_table_list , int(lst[1]), int(lst[2]) , fire , ATOMS)
        elif lst[0] == 'or':
            fire[fire_index] = _or (hash_table_list , int(lst[1]) , int(lst[2]) , fire, ATOMS)
        elif lst[0] == 'implies':
            fire[fire_index] = _implies (hash_table_list , int(lst[1]) , int(lst[2]) , fire, ATOMS)
        elif lst[0] == 'not':
            fire[fire_index] = _not (hash_table_list , int(lst[1]) , fire, ATOMS)
        fire_index += 1
    return [fire, fire_index]
        
def atoms_titles (ATOMS, titles, titles_index):
    for x in ATOMS:
        titles[titles_index] = str(x)
        titles_index += 1
    return [titles, titles_index]

def derived_titles (titles, titles_index, hash_table_list,ATOMS):
    hash_table_index = len(ATOMS)
    num_derived = len(hash_table_list) - len(ATOMS)
    for i in range (num_derived):
        string = hash_table_list[hash_table_index]
        hash_table_index += 1
        lst = string.split(' ')
        if lst[0] != 'not':
            titles[titles_index] = titles[int(lst[1])] + ' ' + str(lst[0]) + ' ' + titles[int(lst[2])]
        else:
            titles[titles_index] = str(lst[0]) + ' ' + titles[int(lst[1])]
        titles_index += 1
    return [titles, titles_index]

def change_10_TF (fire):
    for i in range(len(fire)):
        for j in range(len(fire[i])):
            if fire[i][j] == 1:
                fire[i][j] = 'T'
            elif fire[i][j] == 0:
                fire[i][j] = 'F'
    return fire


def hades():
    [hash_table , ATOMS] = columns.achilles()
    #print("hash table is ", hash_table)
    #print("ATOMS is ", ATOMS)
    num_cols = len(hash_table)
    fire = [[] for x in range(num_cols)]
    fire_index = 0
    atoms_cols = create_atoms_cols (ATOMS)
    for x in atoms_cols:
        fire[fire_index] = x
        fire_index += 1
    #print("fire after creare_atoms_cols is :", fire)
    [fire, fire_index] =  create_derived_cols (hash_table , ATOMS, fire, fire_index)
    #print("fire after derived_atoms_cols is ", fire)
    hash_table_list = list (hash_table)
    titles = ["" for x in range (len (hash_table))]
    titles_index = 0
    [titles, titles_index] = atoms_titles (ATOMS,  titles , titles_index)
    #print("titles after atoms_titles is :" , titles)
    [titles, titles_index] = derived_titles (titles, titles_index, hash_table_list, ATOMS)
    #print("titles after derived_titles is :", titles)
    fire = change_10_TF (fire)
    transpose = list(map(list, zip(*fire)))
    #print("transpose is :", transpose)
    print(tabulate(transpose , headers = titles))

hades()
