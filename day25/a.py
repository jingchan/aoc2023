import math
import os
import re
import pickle
from itertools import combinations

PATH = os.path.dirname(__file__)

# TEST = True
TEST = False

IN_FILE = PATH + '/2.txt'
if TEST:
    IN_FILE = PATH + '/1.txt'

DIRS = [(-1, 0, '^'), (1, 0, 'v'), (0, -1, '<'), (0, 1, '>')]

# def haspath(s, k, graph, visited=None):
#     if visited is None:
#         visited = set()

#     if s == k:
#         return True
#     for c in graph[s]:
#         if c not in visited:
#             visited.add(c)
#             if haspath(c, k, graph, visited):
#                 return True
#     return False


def flow(s, k, graph, path=None, curflow=math.inf):
    if path is None:
        path = list()

    visited = set()

    q = [(s, math.inf, path)]

    while len(q) > 0:
        s, curflow, path = q.pop()
        # print(curflow, len(path))
        path.append(s)
        if s == k:
            return path
        for c in graph[s]:
            if c not in path and graph[s][c] > 0 and c not in visited:
                visited.add(c)
                q.append((c, min(curflow, graph[s][c]), path.copy()))
    return None


def connected(conn, s, graph, invert=None):
    if invert is None:
        invert = set()
    q = [s]
    while len(q) > 0:
        s = q.pop()
        invert.add(s)
        for c, f in graph[s].items():
            if f > 0 and c not in invert:
                q.append(c)
    return invert


def ff(group, conn, num_cuts):
    sgraph = {c: {c: 0 for c in group} for c in group}
    for it, con in conn.items():
        for c in con:
            sgraph[it][c] = 1

    for i in range(len(conn)):
        print('i', i)
        for j in range(i + 1, len(conn)):
            print('j', j)
            rgraph = sgraph.copy()
            path = flow(group[i], group[j], rgraph)

            while path is not None:
                for k in range(len(path) - 1):
                    rgraph[path[k]][path[k + 1]] -= 1
                    rgraph[path[k + 1]][path[k]] += 1
                path = flow(group[i], group[j], rgraph)
                print('flow', path)

            ngroup = connected(conn, group[i], rgraph)
            cut = set()
            for g in ngroup:
                for c in conn[g]:
                    if c not in ngroup:
                        cut.add((g, c))

            if len(cut) == num_cuts:
                print('cuts', cut)
                print(len(ngroup), len(group) - len(ngroup))
                print(len(ngroup) * (len(group) - len(ngroup)))
                return


# def getgroups(names, conn):
#     need = set(names)
#     groups = []
#     while len(need) > 0:
#         q = {need.pop()}
#         curgroup = set()
#         while len(q) > 0:
#             n = q.pop()
#             curgroup.add(n)
#             for c in conn[n]:
#                 if c in need:
#                     need.remove(c)
#                     q.add(c)
#                     curgroup.add(c)
#         groups.append(curgroup)
#     return groups


with open(IN_FILE, 'r') as f:
    # line = f.readline()
    grid = []
    st = []
    names = set()
    conn = {}
    for line in f.readlines():
        line = line.strip()
        left = line.split(': ')[0]
        right = [x for x in line.split(': ')[1].split(' ')]
        names.add(left)
        names = names.union(right)

        for r in right:
            if left not in conn:
                conn[left] = set()
            conn[left].add(r)
            if r not in conn:
                conn[r] = set()
            conn[r].add(left)

    # print(list(names))
    ff(list(names), conn, 3)
    # groups = getgroups(names, conn)

    # solve(name, conn, 3)

    # print(len(groups))

    # grid.append(list(line))
# jqt: rhn xhk nvd
# rsh: frs pzl lsr
# xhk: hfx
# cmg: qnr nvd lhk bvb
# rhn: xhk bvb hfx
# bvb: xhk hfx
# pzl: lsr hfx nvd
# qnr: nvd
# ntq: jqt hfx bvb xhk
# nvd: lhk
# lsr: lhk
# rzs: qnr cmg lsr rsh
# frs: qnr lhk lsr
