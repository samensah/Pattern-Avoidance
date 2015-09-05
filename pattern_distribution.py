__author__ = 'samuel'

from itertools import permutations
import numpy as np
from itertools import *

#import sys
#sys.stdout = open('/home/samuel/Dropbox/Files/Essay Combinatorics/AIMSEssay/myoutput.txt', 'w')


mesh_pattern = np.array([[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]])



def word(n):
    """
    List all permutations of Order n

    @param n: Length/Order of number sequence
    @return: List of permutations of order n
    >>> word(2)
    ... (('1','2'),('2','1'))
    """
    perm_list=[]
    for i in range(1,n+1):
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
    up_alt_list = []
    for term in alternate_perms:
        if term[0] < term[1]:
            up_alt_list.append(term)
    return up_alt_list


def down_alternate(alternate_perms):
    down_alt_list = []
    for term in alternate_perms:
        if term[0] > term[1]:
            down_alt_list.append(term)
    return down_alt_list


def permutation_diagram(term):
    """
    @param term: permutation
    @return: returns permutation diagram of permutation
    """
    old_perm_matrix = [[0 for _ in range(len(term))] for _ in range(len(term))]
    for i,v in enumerate(term):
        old_perm_matrix[i][v-1] = v
    new_perm_matrix = zip(*old_perm_matrix)
    return np.array(new_perm_matrix)


def locate_all_indices(perm, pattern):
    """ Output all the lists of indices where pattern occurs in permutation
    @param perm: permutation
    @param pattern: pattern of length 3
    @return: a list of lists containing index corresponding to pattern and a list of index value
    >>> locate_all_indices([3,2,1], [3,2,1])
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
    @param mesh_pattern: 4x4 matrix showing prohibited areas labelled as 1
    @param perm: permutation
    @param pattern: pattern
    @return: x & y ranges of prohibited areas in permutation diagram
    >>> prohibited_area([[0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]], [3,1,2,4], [3, 1, 2])
    ... [[(1, 2), (0, 1)], [(1, 2), (1, 2)], [(1, 2), (2, 3)]]
    """
    xy_ranges = []
    #horizontal range for prohibited area in perm diagram
    for term1,term2 in locate_all_indices(perm, pattern):
        for coordinate in mesh_pattern_coordinate(mesh_pattern):
            a = coordinate[0]
            b = coordinate[1]
            if b== 0:
                (c, d) = [0, term1[b]]
            elif b==3:
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
            xy_ranges.append([(c,d),(e,f), term2])
    return xy_ranges

def inclusion_test(area, perm):
    return [x for x in area if x in perm] == []


def check_prohibit_area(mesh_pattern, perm, pattern):
    if locate_all_indices(perm, pattern) == []:
        return 0
    else:
        prohibited = []
        prohibited_new = []
        for terms in prohibited_area(mesh_pattern, perm, pattern):
            prohibited.append(terms)
        for key, group in groupby(prohibited, lambda t: t[2]):
            prohibited_new.append(list(group))
        count = 0
        for term in prohibited_new:
            check_local = []
            for hori, vert, term2 in term:
                for i, j in enumerate(permutation_diagram(perm)):
                    if i > (vert[0]-1) and i < (vert[1]+1):
                        section = j[hori[0]:hori[1]+1]
                        #print(section)
                        a = [x for x in perm if x not in term2]
                        statement = inclusion_test(section, a)
                        check_local.append(statement)
            check_local = list(set(check_local))
            if True in check_local and len(check_local) == 1:
                count += 1
        return count

def occurences(tokens,words):
    count = 0
    for i in range(0,len(words),1):
        if (words[i] == tokens):
            count += 1
    return count




if __name__ == '__main__':
    mesh_pattern = np.array([[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]])
    pattern = [3,1,2]


    mylist = []
    for i in down_alternate(alternate(word(7))):
    #for i in up_alternate(alternate(word(2))):
    #for i in alternate(word(7)):
        mylist.append(check_prohibit_area(mesh_pattern, i, pattern))
    for num in list(set(mylist)):
        print(occurences(num, mylist), 'permutations contains', num , 'occurrences of pattern',pattern)
