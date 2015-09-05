__author__ = 'samuel mensah'

import numpy as np
from itertools import *


def word(n):
    """
    List all permutations of Order n

    @param n: Length/Order of number sequence
    @return: List of permutations of order n
    >>> word(2)
    ... (('1','2'),('2','1'))
    """
    perm_list = []
    for i in range(1, n+1):
        perm_list.append(i)
    perms = (p for p in permutations(perm_list))
    return perms


def alternate(perms_n):
    """
    Listing all Alternating Permutations

    @param perms_n: List of permutations of Order n
    @return: List of all alternating permutations of order n
    >>> alternate(word(3))
    ... [[1,3,2], [2,1,3], [2,3,1], [3,1,2]]
    """
    alternate_list = []
    for perm in perms_n:
        statement = perm[0] < perm[1]
        count = 0
        for i in range(1, len(perm) - 1):
            if statement == (perm[i] < perm[i + 1]):
                break
            count += 1
            statement = not statement
        if count == len(perm)-2:
            alternate_list.append(list(perm))
    return alternate_list


def up_alternate(alternate_perms):
    """
    List all Up-down permutations

    @param alternate_perms: List of alternating permutations
    @return: List of up-down alternating permutations
    >>> up_alternate(alternate(word(3)))
    ... [[1, 3, 2], [2, 3, 1]]
    """
    up_alt_list = []
    for term in alternate_perms:
        if term[0] < term[1]:
            up_alt_list.append(term)
    return up_alt_list


def down_alternate(alternate_perms):
    """
    List all Down-up permutations

    @param alternate_perms: List of alternating permutations
    @return: List of down-up alternating permutations
    >>> down_alternate(alternate(word(3)))
    ... [[2, 1, 3], [3, 1, 2]]
    """
    down_alt_list = []
    for term in alternate_perms:
        if term[0] > term[1]:
            down_alt_list.append(term)
    return down_alt_list


def permutation_diagram(term):
    """
    Permutation diagram of a permutation

    @param term: permutation of order n
    @return: returns permutation diagram of permutation of order n
    >>> permutation_diagram([3, 1, 2])
    ... [[0, 1, 0], [0, 0, 2], [3, 0, 0]]
    """
    old_perm_matrix = [[0 for _ in range(len(term))] for _ in range(len(term))]
    for i,v in enumerate(term):
        old_perm_matrix[i][v-1] = v
    new_perm_matrix = zip(*old_perm_matrix)
    return np.array(new_perm_matrix)


def locate_all_indices(perm, pattern):
    """
    Output all the lists of indices where pattern occurs in permutation and the subsequence of the pattern itself

    @param perm: permutation
    @param pattern: classical pattern of length 3
    @return: a list of lists containing index corresponding to pattern and a list of index value
    >>> locate_all_indices([3, 2, 1], [3, 2, 1])
    ... [[[0, 1, 2], [3, 2, 1]]]
    """
    indices_of_perm = []
    count = 0
    for i in range(len(perm)-2):
        for j in range(i+1, len(perm)-1):
            for k in range(j+1, len(perm)):
                if (pattern == [1, 2, 3]) and (perm[i] < perm[j]) and (perm[j] < perm[k]):
                    indices_of_perm.append([[i, j, k], [perm[i], perm[j], perm[k]]])
                    count += 1
                elif (pattern == [2, 3, 1]) and (perm[i] < perm[j]) and (perm[j] > perm[k]) and (perm[i] > perm[k]):
                    indices_of_perm.append([[i, j, k], [perm[i], perm[j], perm[k]]])
                    count += 1
                elif (pattern == [3, 1, 2]) and (perm[i] > perm[j]) and (perm[j] < perm[k]) and (perm[i] > perm[k]):
                    indices_of_perm.append([[i, j, k], [perm[i], perm[j], perm[k]]])
                    count += 1
                elif (pattern == [1, 3, 2]) and (perm[i] < perm[j]) and (perm[j] > perm[k]) and (perm[i] < perm[k]):
                    indices_of_perm.append([[i, j, k], [perm[i], perm[j], perm[k]]])
                    count += 1
                elif (pattern == [2, 1, 3]) and (perm[i] > perm[j]) and (perm[j] < perm[k]) and (perm[i] < perm[k]):
                    indices_of_perm.append([[i, j, k], [perm[i], perm[j], perm[k]]])
                    count += 1
                elif (pattern == [3, 2, 1]) and (perm[i] > perm[j]) and (perm[j] > perm[k]):
                    indices_of_perm.append([[i, j, k], [perm[i], perm[j], perm[k]]])
                    count += 1
    if count != 0:
        return indices_of_perm
    return []


def mesh_pattern_coordinate(mesh_pattern):
    """
    List all coordinates of prohibited areas in the mesh pattern

    @param mesh_pattern: 4x4 list showing prohibited areas in pattern
    @return: coordinates of prohibited areas labelled as 1
    >>> mesh_pattern_coordinate([[0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 1, 0]])
    ... [(0, 2), (2, 2), (3, 2)]
    """
    coordinate_list = []
    for rownum, row in enumerate(mesh_pattern):
        for colnum, value in enumerate(row):
           if value == 1:
               coordinate_list.append((rownum, colnum))
    return coordinate_list


def prohibited_area(mesh_pattern, perm, pattern):
    """
    Locate horizontal and vertical ranges of prohibited areas in permutation diagram

    @param mesh_pattern: 4x4 matrix showing prohibited areas labelled as 1
    @param perm: permutation
    @param pattern: classical pattern of length 3
    @return: x & y ranges of prohibited areas in permutation diagram
    >>> prohibited_area([[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]], [3,1,2,4], [3, 1, 2])
    ... [[(1, 2), (0, 1)], [(1, 2), (1, 2)], [(1, 2), (2, 3)]]
    """
    xy_ranges = []
    #horizontal range for prohibited area in perm diagram
    for term1, term2 in locate_all_indices(perm, pattern):
        for coordinate in mesh_pattern_coordinate(mesh_pattern):
            a = coordinate[0]
            b = coordinate[1]
            if b == 0:
                (c, d) = [0, term1[b]]
            elif b == 3:
                (c, d) = [term1[b-1], len(perm)-1]
            else:
                (c, d) = [term1[b-1], term1[b]]
    #vertical range for prohibited area in perm diagram
            term02 = sorted(term2, key=int)
            if a == 0:
                (e, f) = (0, int(term02[a])-1)
            elif a == 3:
                (e, f) = (int(term02[a-1])-1, len(perm)-1)
            else:
                (e, f) = (int(term02[a-1])-1, int(term02[a])-1)
            xy_ranges.append([(c, d), (e, f), term2])
    return xy_ranges


def inclusion_test(area, perm):
    """
    @return: returns Truth value for a condition
            within check_prohibit_area function
    """
    return [x for x in area if x in perm] == []


def check_prohibit_area(mesh_pattern, perm, pattern):
    """
    Checks if a permutation contains a pattern or not and returns True if it does and False either wise

    @param mesh_pattern: 4x4 list showing prohibited areas in pattern
    @param perm: permutation
    @param pattern: classical pattern of length 3
    @return: returns Truth value of an occurrence of a pattern in a permutation
    """
    if locate_all_indices(perm, pattern) == []:
        return False
    else:
        prohibited = []
        prohibited_new = []
        for terms in prohibited_area(mesh_pattern, perm, pattern):
            prohibited.append(terms)
        for key, group in groupby(prohibited, lambda t: t[2]):
            prohibited_new.append(list(group))
        check_global = []
        for term in prohibited_new:
            check_local = []
            for hori, vert, term2 in term:
                for i, j in enumerate(permutation_diagram(perm)):
                    if i > (vert[0]-1) and i < (vert[1]+1):
                        section = j[hori[0]:hori[1]+1]
                        a = [x for x in perm if x not in term2]
                        statement = inclusion_test(section, a)
                        check_local.append(statement)
            if False in check_local:
                check_global.append(False)
            if len(set(check_local)) == 1 and check_local[0] == True:
                return True
        if len(check_global) == len(prohibited_new):
            return False


def run_program(n, type ='alternating'):
    """
    A sequence of the number of permutations avoiding a given pattern

    @param n: permutation of length n
    @param mesh_pattern: 4x4 list showing prohibited areas in pattern
    @param pattern: classical pattern of length 3
    @param type: either 'default = alternating', 'down-up', 'up-down'
    @return: a sequence of the number of each length of permutation avoiding
            the pattern up to n
    """
    if type == 'down-up':
        final_list = []
        for i in range(2, n):
            count = 0
            for term in down_alternate(alternate(word(i))):
                if check_prohibit_area(mesh_pattern, term, pattern) == False:
                    count += 1
            final_list.append(count)
        print('Number of',type, 'permutations of length n avoiding pattern starting from n=2')
        return final_list
    elif type == 'up-down':
        final_list = []
        for i in range(2, n):
            count = 0
            for term in up_alternate(alternate(word(i))):
                if check_prohibit_area(mesh_pattern, term, pattern) == False:
                    count += 1
            final_list.append(count)
        print('Number of',type, ' permutations of length n avoiding pattern starting from n=2')
        return final_list
    else:
        final_list = []
        for i in range(2, n):
            count = 0
            for term in alternate(word(i)):
                if check_prohibit_area(mesh_pattern, term, pattern) == False:
                    count += 1
            final_list.append(count)
        print('Number of',type, ' permutations of length n avoiding pattern starting from n=2')
        return final_list


def pattern_occurrence(n, type = 'alternating'):
    """
    Shows if a permutation has an occurrence of a pattern or not

    @param the length of the permutation n
    @param type of permutation
    """
    print('Permutations of length',n,'containing pattern or not, False=contains no pattern, True=contains pattern')
    if type == 'down-up':
        for i in down_alternate(alternate(word(n))):
            if check_prohibit_area(mesh_pattern, i, pattern):
                print(i, True)
                pass
            else:
                print(i, False)
    if type == 'up-down':
        for i in up_alternate(alternate(word(n))):
            if check_prohibit_area(mesh_pattern, i, pattern):
                print(i, True)
                pass
            else:
                print(i, False)
    if type == 'alternating':
        for i in alternate(word(n)):
            if check_prohibit_area(mesh_pattern, i, pattern):
                print(i, True)
            else:
                print(i, False)



if __name__ == '__main__':
    pattern = [1,2,3] #classical pattern
    mesh_pattern = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]) #1 for prohibition, 0 eitherwise

    #Print sequence of the number of permutations of length 2-n avoiding mesh_pattern
    print(run_program(9, 'up-down'))

    #Permutations of length n of a particular type with occurence of pattern or not
    pattern_occurrence(3, 'alternating')

