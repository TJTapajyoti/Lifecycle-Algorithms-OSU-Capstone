from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
import numpy as np


def run_prog(sec1, tot1, a1, m1, nsec, th=0.005):
    """
    int
    float
    matrix nxn
    array n
    int
    float, optional
    """
    a = a1
    m = m1
    mainspa(sec1, tot1, nsec, a, m, th)


def mainspa(sec, tot, nsec, a, m, th):
    """
    int
    float
    int
    """
    f = 1
    v = 1
    s = nsec
    sector = sec
    total = tot
    fvp = sec
    fvp1 = 0
    fvnodeno = 0
    fv = f
    fvres2 = f * m[sec - 1]
    res = []
    node_no = []
    res2 = []
    p = []
    p1 = []
    spa_calc(s, a, sector, fv, m, th, fvp1, res, node_no, res2, p, p1)
    # print(res2)
    # print(node_no)
    # print(p)
    zipped = zip(res2, node_no, p)
    zipped.sort()
    res2, node_no, p = zip(*zipped)
    res2 = list(res2)
    node_no = list(node_no)
    p = list(p)
    # print(res2)
    # print(node_no)
    # print(p)
    spa_print(res2, node_no, sector, total, s, fvres2, th)
    # spa_print2()


# DONE
def spa_calc(s, a, sector, fv, m, th, fvp1, res, node_no, res2, p, p1):
    """
    undefined vars:
    s - int
    a - matrix
    sector - int ?
    fv - scalar
    m - array
    th - float
    fpv1 - scalar
    res - array
    node_no - array
    res2 - array
    p - array
    p1 - array
    """
    cc = 0
    v = 1
    d = -1
    m_max = max(m)
    # for depth in range(5):
    for depth in range(20000):
        # print('depth = {}'.format(depth))
        # print(res)
        # print(res2)
        # print(p)
        # print(node_no)
        # print(p1)
        # print(v)
        # print(len(res))
        # print(d)
        node_processed = False
        for i in range(s):
            # print(a)
            # print(res)
            # print(depth)
            # print(i)
            cur_index = s * depth + i - cc
            if depth == 0:    # calculation for the first parent level  # THIS IS CORRECT
                path_val = a[i][sector - 1] * fv  # calculation of path value
                calc_node_no = s * fvp1 + i + 1
            else:   # calculation for all other parent levels
                # print(p1[d] % s)
                # print(depth)
                # print(p1[d])
                # print(d)
                # print(i)
                # print(p1)
                # print(d)
                if p1[d] % s == 0:
                    # print(a[i][s - 1])
                    # print(res[depth - 1])
                    path_val = a[i][s - 1] * res[depth - 1]
                else:
                    a_term = a[i][(p1[d] % s) - 1]
                    res_term = res[depth - 1]
                    # print(a_term)
                    # print(res_term)
                    path_val = a[i][(p1[d] % s) - 1] * res[depth - 1]
                calc_node_no = s * p1[d] + i + 1
            # print(path_val)
            if path_val * m_max > th:
                # calculation of path value
                res.append(path_val)
                # NOTE BUG HERE BECAUSE APPENDING TO ARRAY
                # calculation of path value for the EEIO model
                res2.append(path_val * m[i])
                # calculation of the node number
                p.append(i)
                node_no.append(calc_node_no)
                p1.append(calc_node_no)
                node_processed = True
                v += 1
            else:
                cc += 1
        d += 1
        if d + 1 == v:
        # if not node_processed:
            break


def spa_print(res2, node_no, sector, total, s, fvres2, th):
    '''
    th
    fvres2
    sector
    total
    res2
    node_no
    s
    '''
    with open('myfile4.txt', 'w') as f:
        f.write('\n {}\n'.format(sector))
        f.write('{}  {}    zero order       {}   \n'.format(fvres2, sector,
                                                              fvres2 / total * 100))
        for i in range(len(res2) - 1, -1, -1):
            if res2[i] > th:
                node_no_decomp = mod_decomp(node_no[i], s)
                order = get_order(node_no_decomp)
                node_no_decomp.append(sector)
                node_no_decomp = [str(x) for x in node_no_decomp]
                nodes_str = '----'.join(node_no_decomp)
                f.write('{}   {}    {}   {}   \n'.format(res2[i], nodes_str, order, res2[i] / total * 100))


def get_order(a):
    if len(a) == 1:
        return 'first order'
    elif len(a) == 2:
        return 'second order'
    elif len(a) == 3:
        return 'third order'
    elif len(a) == 4:
        return 'fourth order'
    elif len(a) == 5:
        return 'fifth order'
    else:
        return 'order {}'.format(len(a))


def mod_decomp(n, base):
    decomp = []
    while n >= base:
        decomp.append(n % base)
        n = (n - decomp[-1]) // base
    decomp.append(n)
    return decomp
