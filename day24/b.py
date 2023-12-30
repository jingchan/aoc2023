import math
import os
import re
import pickle
from itertools import combinations
import random

PATH = os.path.dirname(__file__)
EPSILON = 0.0000000000001
NUM_ANSWERS = 3000
# TEST = True
TEST = False

IN_FILE = PATH + '/2.txt'
if TEST:
    IN_FILE = PATH + '/1.txt'

DIRS = [(-1, 0, '^'), (1, 0, 'v'), (0, -1, '<'), (0, 1, '>')]


def vecmul(p1, m):
    return (p1[0] * m, p1[1] * m, p1[2] * m)


def vecdiv(p1, d):
    return (p1[0] / d, p1[1] / d, p1[2] / d)


def norm(p1):
    return math.sqrt(p1[0] ** 2 + p1[1] ** 2 + p1[2] ** 2)


def vecadd(p1, v1):
    return (p1[0] + v1[0], p1[1] + v1[1], p1[2] + v1[2])


def normalized(p1):
    norm = math.sqrt(p1[0] ** 2 + p1[1] ** 2 + p1[2] ** 2)
    return (p1[0] / norm, p1[1] / norm, p1[2] / norm)


# |a||b|cos(theta) = a dot b
def dotproduct(p1, p2):
    return p1[0] * p2[0] + p1[1] * p2[1] + p1[2] * p2[2]


def vecsub(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2])


def v2cross(p1, p2):
    return p1[0] * p2[1] - p1[1] * p2[0]


def crossproduct(p1, p2):
    return (
        p1[1] * p2[2] - p1[2] * p2[1],
        p1[2] * p2[0] - p1[0] * p2[2],
        p1[0] * p2[1] - p1[1] * p2[0],
    )


def timeto(p1, v1, target):
    return (target[0] - p1[0]) / v1[0]


# ### Derive line intersection formula from line equations.
#
# let x be intersection between p1 and p2
# let d be diff between p1 and p2
# x = x0 + v_x0*t0 = x1 + v_x1*t1
#     (x0 + v_x0*t0 - x1) / v_x1 = t1
# y = y0 + v_y0*t0 = y1 + v_y1*t1
#     (y0 + v_y0*t0 - y1) / v_y1 = t1
#
#     x0*v_y1 + v_x0*v_y1*t0 - x1*v_y1 = y0*v_x1 + v_y0*v_x1*t0 - y1*v_x1
#     v_x0*v_y1*t0 - v_y0*v_x1*t0 = y0*v_x1 - y1*v_x1 - x0*v_y1 + x1*v_y1
#     t0*(v_x0*v_y1 - v_y0*v_x1) = y0*v_x1 - y1*v_x1 - x0*v_y1 + x1*v_y1
#     t0 = (y0*v_x1 - y1*v_x1 - x0*v_y1 + x1*v_y1) / (v_x0*v_y1 - v_y0*v_x1)
#     t1 = (x0 + v_x0*t0 - x1) / v_x1
def intersection(p1, v1, p2, v2, axis1, axis2):
    p1 = (p1[axis1], p1[axis2])
    p2 = (p2[axis1], p2[axis2])
    v1 = (v1[axis1], v1[axis2])
    v2 = (v2[axis1], v2[axis2])

    # Rename variables
    x0 = p1[0]
    y0 = p1[1]
    x1 = p2[0]
    y1 = p2[1]
    v_x0 = v1[0]
    v_y0 = v1[1]
    v_x1 = v2[0]
    v_y1 = v2[1]

    if v_x0 * v_y1 - v_y0 * v_x1 == 0:
        # print('nointersect', p1, v1, p2, v2)
        return None
    t0 = (y0 * v_x1 - y1 * v_x1 - x0 * v_y1 + x1 * v_y1) / (
        v_x0 * v_y1 - v_y0 * v_x1
    )
    x = x0 + v_x0 * t0
    y = y0 + v_y0 * t0

    ret = [0, 0, 0]
    ret[axis1] = x
    ret[axis2] = y

    if t0 < 0:
        return None
    return (ret, t0)


def veceq(v1, v2):
    return (v1[0] / v2[0] == v1[1] / v2[1] == v1[2] / v2[2]) or (
        v1[0] / v2[0] == v1[1] / v2[1] == v1[2] / v2[2]
    )


# Given a list of points give a number that represents how non linear they are.
#
# If this is equal to 0, then points are linear.
def nonlinearity(points):
    total = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            for k in range(j + 1, len(points)):
                v1 = vecsub(points[j], points[i])
                v2 = vecsub(points[k], points[i])
                # v1 = normalized(v1)
                # v2 = normalized(v2)
                total += norm(crossproduct(v1, v2))
    return total


def project_to_plane(p1, normal):
    return vecsub(p1, vecmul(normal, dotproduct(p1, normal)))


def solve(v, points, axis=(0, 1), normal=(0, 0, 1)):
    # r = random.random()
    # if r < 1 / 3:
    #     axis = (0, 1)
    #     normal = (0, 0, 1)
    # elif r < 2 / 3:
    #     axis = (1, 2)
    #     normal = (1, 0, 0)
    # else:
    #     axis = (2, 0)
    #     normal = (0, 1, 0)
    points_plane = [
        [project_to_plane(p, v), project_to_plane(p2, v)] for p, p2 in points
    ]

    points_xy = [
        [project_to_plane(p, normal), project_to_plane(p2, normal)]
        for p, p2 in points_plane
    ]
    intersect_points = []
    for i in range(len(points_xy) - 1):
        for j in range(i + 1, len(points_xy)):
            p1, p2 = points_xy[i]
            p3, p4 = points_xy[j]
            intersect = intersection(
                p1, vecsub(p2, p1), p3, vecsub(p4, p3), axis[0], axis[1]
            )
            if intersect:
                intersect_points.append(intersect)
    diameter = -math.inf
    for i in range(len(intersect_points) - 1):
        for j in range(i + 1, len(intersect_points)):
            p1, t1 = intersect_points[i]
            p2, t2 = intersect_points[j]
            diameter = max(diameter, norm(vecsub(p1, p2)))

    return diameter, intersect_points


def vecfrom(theta, phi):
    return (
        math.cos(theta) * math.cos(phi),
        math.sin(theta) * math.cos(phi),
        math.sin(phi),
    )


with open(IN_FILE, 'r') as f:
    # line = f.readline()
    grid = []
    st = []
    for line in f.readlines():
        line = line.strip()
        pos = [int(x) for x in line.split(' @ ')[0].split(', ')]
        vel = [int(x) for x in line.split(' @ ')[1].split(', ')]
        st.append((pos, vel))
        # grid.append(list(line))

    # v = [0.9611890119460773, -0.23008670339787538, -0.152235975490755]
    # v = [0.8161500531774176, 0.5532476800966718, -0.16678157921709794]
    # points = [[p, vecadd(p, vecmul(v, 10**12))] for p, v in st]
    points = [[p, vecadd(p, vecmul(v, 10**12))] for p, v in st[:10]]

    # theta = 0.6112491209744113
    # phi = 2.9727962898398013
    # theta, phi = 0.611249093548586, 2.972796262405047
    theta, phi = random.random() * 2 * math.pi, random.random() * 2 * math.pi
    # theta, phi = 5.103099390372791, 3.388122369581825
    # theta, phi = 5.103099390372788, 3.388122369582207
    v = vecfrom(theta, phi)

    max_dist = math.inf
    last_dist = math.inf
    last_theta = None
    last_phi = None
    delta = 0.01
    while max_dist > 0:
        diameter, intersect_points = solve(v, points)
        # print('run', diameter, v, theta, phi, delta)

        if max_dist >= diameter:
            max_dist = diameter
            print(max_dist, v, f'theta/phi: {theta}, {phi}', f'delta: {delta}')
            if max_dist < 0.1:
                print(intersect_points)

        if max_dist < 10**13:
            if last_dist < diameter:
                delta /= 2
                print('delta', delta)
                if last_theta is not None:
                    theta = last_theta
                if last_phi is not None:
                    phi = last_phi
            theta_plus_dt = theta + delta
            phi_plus_dt = phi + delta
            v = vecfrom(theta_plus_dt, phi)
            ddiameter_dtheta = solve(v, points)[0] - diameter

            v = vecfrom(theta, phi_plus_dt)
            ddiameter_dphi = solve(v, points)[0] - diameter

            last_theta = theta
            last_phi = phi
            if diameter > 0.5:
                if ddiameter_dtheta < 0:
                    theta += delta
                else:
                    theta -= delta

                if ddiameter_dphi < 0:
                    phi += delta
                else:
                    phi -= delta
            else:
                if random.random() > 0.1:
                    if ddiameter_dtheta < 0:
                        theta += delta
                    else:
                        theta -= delta

                if random.random() > 0.1:
                    if ddiameter_dphi < 0:
                        phi += delta
                    else:
                        phi -= delta
        else:
            last_theta = theta
            last_phi = phi
            theta = random.random() * 2 * math.pi
            phi = random.random() * 2 * math.pi

        last_dist = diameter
        v = vecfrom(theta, phi)

    print(max_dist, v, theta, phi)
# v = (-0.3693305798577347, 0.896682421249508, -0.24404007499603284)
# 0.0625 (-0.3693305798577748, 0.8966824212495919, -0.24404007499566419) 5.103099390372793 3.388122369581827 1.7763568394002506e-16
# 0.0625 (-0.3693305798577347, 0.896682421249508, -0.24404007499603284) 5.103099390372788 3.388122369582207 1.7763568394002506e-16
# 0.0 (0.18481320367840257, 0.5309488987385587, -0.8270050463415789) 4.377424793210504 4.115352018079061
# 0.015625 (-0.8072928944781511, -0.5657345111992022, 0.16799596829474409) 0.6112490935488537 2.972796262405048 4.8828125e-17
# 984482180801536.0 Too High
# 859286305752132.0 <--??
# 855998046527682.0 <--
# 855998046527680.0
# 855998046527680.0 < Too High
# 819175790155006.0 <--- wrong
# 752169577588852.0 <--- xx
# 752169577588849.0 Too low
# 1210825739277280.0
# 1063969843105756.0
# 855998046527680.0
