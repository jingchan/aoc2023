import math
import os
import re
import pickle
from itertools import combinations
import random
import decimal
from decimal import Decimal


# print(getcontext())
decimal.getcontext().prec = 100
# exit()

PATH = os.path.dirname(__file__)
EPSILON = 0.0000000000001
NUM_ANSWERS = 3000
# TEST = True
TEST = False

IN_FILE = PATH + '/2.txt'
if TEST:
    IN_FILE = PATH + '/1.txt'

DIRS = [(-1, 0, '^'), (1, 0, 'v'), (0, -1, '<'), (0, 1, '>')]

NUM_INPUTS = 5
INTERSECT_THRESHOLD = NUM_INPUTS * 0.8
INITIAL_DELTA = Decimal(0.1)


def vecmul(p1, m):
    return (p1[0] * m, p1[1] * m, p1[2] * m)


def vecdiv(p1, d):
    return (p1[0] / d, p1[1] / d, p1[2] / d)


def norm(p1):
    return ((p1[0] ** 2) + p1[1] ** 2 + p1[2] ** 2).sqrt()
    # return math.sqrt(p1[0] ** 2 + p1[1] ** 2 + p1[2] ** 2)


def vecadd(p1, v1):
    return (p1[0] + v1[0], p1[1] + v1[1], p1[2] + v1[2])


def normalized(p1):
    n = norm(p1)
    return (p1[0] / n, p1[1] / n, p1[2] / n)


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
# ### Solution to Part 1:
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
    t1 = (x0 + v_x0 * t0 - x1) / v_x1
    x = x0 + v_x0 * t0
    y = y0 + v_y0 * t0

    ret = [Decimal(0), Decimal(0), Decimal(0)]

    ret[axis1] = x
    ret[axis2] = y

    if t0 < 0:
        return None
    if t1 < 0:
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
    best_intersect_points = []
    # for i in range(len(points_xy) - 1):
    #     for j in range(i + 1, len(points_xy)):
    #         p1, p2 = points_xy[i]
    #         p3, p4 = points_xy[j]
    #         intersect = intersection(
    #             p1, vecsub(p2, p1), p3, vecsub(p4, p3), axis[0], axis[1]
    #         )
    #         if intersect:
    #             best_intersect_points.append(intersect)
    for i in range(len(points_xy)):
        p1, p2 = points_xy[i]
        p3, p4 = points_xy[(i + 1) % len(points_xy)]
        intersect = intersection(
            p1, vecsub(p2, p1), p3, vecsub(p4, p3), axis[0], axis[1]
        )
        if intersect:
            best_intersect_points.append(intersect)
    diam_val = Decimal(0)
    for i in range(len(best_intersect_points) - 1):
        for j in range(i + 1, len(best_intersect_points)):
            p1, t1 = best_intersect_points[i]
            p2, t2 = best_intersect_points[j]
            diam_val += norm(vecsub(p1, p2)) * norm(vecsub(p1, p2))

    return diam_val, best_intersect_points


def vecfromxyz(x, y, z):
    return normalized((x, y, z))


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
    points = [[p, vecadd(p, vecmul(v, 10**12))] for p, v in st[:NUM_INPUTS]]
    points = [
        [
            (Decimal(p1[0]), Decimal(p1[1]), Decimal(p1[2])),
            (Decimal(p2[0]), Decimal(p2[1]), Decimal(p2[2])),
        ]
        for p1, p2 in points
    ]

    # theta = 0.6112491209744113
    # phi = 2.9727962898398013
    # theta, phi = 0.611249093548586, 2.972796262405047
    theta, phi = random.random() * 2 * math.pi, random.random() * 2 * math.pi

    best_diam = Decimal(math.inf)
    best_intersect_points = []
    best_xyz = (
        Decimal(random.random() * 2 - 1),
        Decimal(random.random() * 2 - 1),
        Decimal(random.random() * 2 - 1),
    )

    # Continue progerss
    best_xyz = (
        Decimal('0.66'),
        Decimal('-0.4'),
        Decimal('0.6'),
    )
    # best_xyz = (
    #     Decimal('0.655624175224617911084123988985083997249603271484375'),
    #     Decimal('-0.4251288842746381302362124188221059739589691162109375'),
    #     Decimal('0.16136937352295088743403539410792291164398193359375'),
    # )
    v = normalized(best_xyz)
    best_diam, best_intersect_points = solve(v, points)

    delta = INITIAL_DELTA
    # while best_diam > Decimal(0.0000000000000000001) and delta > 0:

    rand_iterations = 0
    descent_iterations = 0
    reduction = Decimal(math.inf)
    while best_diam > 0 and delta > 0:
        # best_diam, best_intersect_points = solve(v, points)
        # print('run', best_diam, v, theta, phi, delta)

        # if best_diam < 20:
        #     print(best_intersect_points)

        # if best_diam < math.inf:
        print()
        if (
            len(best_intersect_points) < INTERSECT_THRESHOLD
            or (
                descent_iterations > 50
                and best_diam > 10**15
                and random.random() < 0.8
            )
            # or (
            #     descent_iterations > 50
            #     and reduction < best_diam * Decimal(0.01)
            # )
            or random.random() < 0.2
        ):
            rand_iterations += 1
            print(f'Random Search -- Iter #{rand_iterations}')
            vx = Decimal(random.random() * 2 - 1)
            vy = Decimal(random.random() * 2 - 1)
            vz = Decimal(random.random() * 2 - 1)
            # while abs(vz) < 0.12:
            #     vx = Decimal(random.random() * 2 - 1)
            #     vy = Decimal(random.random() * 2 - 1)
            #     vz = Decimal(random.random() * 2 - 1)

            v = vecfromxyz(vx, vy, vz)
            diam, intersect_points = solve(v, points)
            if (
                len(intersect_points) > len(best_intersect_points)
                and diam < best_diam
            ):
                best_diam = diam
                best_intersect_points = intersect_points
                best_xyz = (vx, vy, vz)
                delta = INITIAL_DELTA
                descent_iterations = 0
        else:
            descent_iterations += 1
            print(f'Gradient Descent -- Iter #{descent_iterations}')

            rvs = [
                vecmul(
                    normalized(
                        (
                            Decimal(random.random() * 2 - 1),
                            Decimal(random.random() * 2 - 1),
                            Decimal(random.random() * 2 - 1),
                        )
                    ),
                    delta,
                )
                for _ in range(10)
            ]

            dv_to_try = rvs
            dv_to_try += [vecmul(rv, Decimal(-1)) for rv in rvs]
            dv_to_try += [
                (delta, 0, 0),
                (0, delta, 0),
                (0, 0, delta),
                (-delta, 0, 0),
                (0, -delta, 0),
                (0, 0, -delta),
            ]

            newbest = False
            for dv in dv_to_try:
                v = vecadd(best_xyz, dv)
                diam, intersect_points = solve(v, points)
                if len(intersect_points) < len(best_intersect_points):
                    continue
                if (
                    len(intersect_points) == len(best_intersect_points)
                    and diam >= best_diam
                ):
                    continue
                reduction = best_diam - diam
                best_diam = diam
                best_intersect_points = intersect_points
                best_xyz = v
                newbest = True
                break
            if not newbest:
                # print(f'Decreasing delt from: {delta}')
                # print(f'best_diam: {best_diam:0.2f}')
                delta /= Decimal(2)
                # print('delta', delta)
                # delta /= 2
                # continue

        if best_diam <= best_diam:
            best_diam = best_diam
            v = normalized(best_xyz)
            print(f'maxdist: {best_diam:0.2f}')
            print(f'v: {v[0]:0.2f}, {v[1]:0.2f}, {v[2]:0.2f}')
            print(f'x: {best_xyz[0]}')
            print(f'y: {best_xyz[1]}')
            print(f'z: {best_xyz[2]}')
            print(f'delta: {delta}')
            print(
                'best_intersect_points',
                len(best_intersect_points),
            )
            for i, (p, t) in enumerate(best_intersect_points[:10]):
                print(f'p{i}: {p[0]:.3f}, {p[1]:.3f}, {p[2]:.3f}, t: {t:.3f}')
                # print(
                #     f'impact: ({t:.3f}, ({ip[0]:.3f}, {ip[1]:.3f}, {ip[2]:.3f}))'
                # )
            # print(f'p10: {best_intersect_points[10]}')
            ip = [
                (
                    t * Decimal(10**12),
                    vecadd(st[i][0], vecmul(st[i][1], t * Decimal(10**12))),
                )
                for i, (_, t) in enumerate(best_intersect_points)
            ]
            rev_vel = [
                vecdiv(vecsub(p2, p), (t2 - t))
                for ((t, p), (t2, p2)) in zip(ip[:-1], ip[1:])
            ]
            for i, p in enumerate(rev_vel[:10]):
                print(f'ans{i}: vel:({p[0]:0.5f}, {p[1]:0.5f}, {p[2]:0.5f})')
            rev_pos = [
                vecsub(p, vecmul(v, t)) for ((t, p), v) in zip(ip, rev_vel)
            ]
            for i, p in enumerate(rev_pos[:10]):
                print(f'ans{i}: pos:({p[0]:0.5f}, {p[1]:0.5f}, {p[2]:0.5f})')

            for p in rev_pos[:1]:
                print(f'{p[0] + p[1] + p[2]:.5f}')

    print('best_diam', best_diam)
    print('best_xyz:', best_xyz)
    print('intersections', best_intersect_points)

# 512.0625772381853 (0.8338469323240469, -0.5499205575186785, 0.047819178915179957) xyz: 0.8927753504535679, -0.5887837436686355, 0.05119858640651676 delta: 1.8189894035458565e-14
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

# Gradient Descent -- Iter #298
# maxdist: 0.00
# v: 0.82, -0.54, -0.20
# x: 0.8389502578747874795476429730618980063057593249775231767535365774511720370410113345552101829797274561
# y: -0.5532861915733365456514921399404632010215655411047546684038148838339457089818319967906045165535037591
# z: -0.2070830050430690425641850329057996726511280385074399078288301783313576427112047798696639246057510130
# delta: 6.01853107621011237489551983210235363799862604460832296202441874927658361365038964504983012339129483E-37
# best_intersect_points 10
# p0: 272441739892584.812, 306192985182661.178, 0.000, t: 0.131
# p1: 272441739892584.812, 306192985182661.178, 0.000, t: 0.423
# p2: 272441739892584.812, 306192985182661.178, 0.000, t: 0.632
# p3: 272441739892584.812, 306192985182661.178, 0.000, t: 0.552
# p4: 272441739892584.812, 306192985182661.178, 0.000, t: 0.574
# p5: 272441739892584.812, 306192985182661.178, 0.000, t: 0.532
# p6: 272441739892584.812, 306192985182661.178, 0.000, t: 0.331
# p7: 272441739892584.812, 306192985182661.178, 0.000, t: 0.421
# p8: 272441739892584.812, 306192985182661.178, 0.000, t: 1.003

# Gradient Descent -- Iter #1363
# maxdist: 0.00
# v: 0.81, -0.53, -0.26
# x: 0.8401610865202343186457177827031437963738343045111292244152497292119796211174430859053731878429473941
# y: -0.5540847308950649269921579642199944750279050610395977680731396063620224024573818200952998801544886360
# z: -0.2673349496037643293830284196329110503282021538060527932576665199618612845102020180035984356601807784
# delta: 6.4690793791235122097150029950374356856305569490224744040491183226562913235545497974564976414189845E-174
# best_intersect_points 12
# p0: 286829865497347.670, 296704042131491.407, 0.000, t: 0.131
# p1: 286829865497347.670, 296704042131491.407, 0.000, t: 0.423
# p2: 286829865497347.670, 296704042131491.407, 0.000, t: 0.632
# p3: 286829865497347.670, 296704042131491.407, 0.000, t: 0.552
# p4: 286829865497347.670, 296704042131491.407, 0.000, t: 0.574
# p5: 286829865497347.670, 296704042131491.407, 0.000, t: 0.532
# p6: 286829865497347.670, 296704042131491.407, 0.000, t: 0.331
# p7: 286829865497347.670, 296704042131491.407, 0.000, t: 0.421
# p8: 286829865497347.670, 296704042131491.407, 0.000, t: 1.003
# p9: 286829865497347.670, 296704042131491.407, 0.000, t: 0.728

# Gradient Descent -- Iter #1128
# maxdist: 0.00
# v: 0.68, -0.45, -0.58
# x: 0.8494464352577219683927925755708301196593344328246724184850714898285978559679116173516607438534262637
# y: -0.5602084017470281081873614118459954911014965435116119175672156061952043207817051526620271572366682166
# z: -0.7265439896489099546871186296065475507176696098415769468678638309052554482633113934466372700326103958
# delta: 6.879105134148699263700994200535617837177536483849953817577601926134415579815756551184581491558265225E-137
# best_intersect_points 15
# p0: 397856222913431.778, 223482358387550.634, 0.000, t: 0.131
# p1: 397856222913431.778, 223482358387550.634, 0.000, t: 0.423
# p2: 397856222913431.778, 223482358387550.634, 0.000, t: 0.632
# p3: 397856222913431.778, 223482358387550.634, 0.000, t: 0.552
# p4: 397856222913431.778, 223482358387550.634, 0.000, t: 0.574
# p5: 397856222913431.778, 223482358387550.634, 0.000, t: 0.532
# p6: 397856222913431.778, 223482358387550.634, 0.000, t: 0.331
# p7: 397856222913431.778, 223482358387550.634, 0.000, t: 0.421
# p8: 397856222913431.778, 223482358387550.634, 0.000, t: 1.003
# p9: 397856222913431.778, 223482358387550.634, 0.000, t: 0.728

# Random Search -- Iter #1148
# maxdist: 0.00
# v: -0.79, 0.52, -0.31
# x: -0.8283156379705528409078256950312341872471768928997831411132026510098406322272927316056387424464262944
# y: 0.5462726788049524112080294695041475207127412157496482927823008923800104286419188068521914895439316275
# z: -0.3258678242218646885353983115215164220522231506881462234827210298319721135167072692241745375244788422
# delta: 1.654361225106055441578313542131137267189166192289701392083246622819337617871227053001348394900560378E-25
# best_intersect_points 20
# p0: 146963367492502.514, 388945746908880.328, 0.000, t: 0.131
# p1: 146963367492502.514, 388945746908880.328, 0.000, t: 0.423
# p2: 146963367492502.514, 388945746908880.328, 0.000, t: 0.632
# p3: 146963367492502.514, 388945746908880.328, 0.000, t: 0.552
# p4: 146963367492502.514, 388945746908880.328, 0.000, t: 0.574
# p5: 146963367492502.514, 388945746908880.328, 0.000, t: 0.532
# p6: 146963367492502.514, 388945746908880.328, 0.000, t: 0.331
# p7: 146963367492502.514, 388945746908880.328, 0.000, t: 0.421
# p8: 146963367492502.514, 388945746908880.328, 0.000, t: 1.003
# p9: 146963367492502.514, 388945746908880.328, 0.000, t: 0.728

# Gradient Descent -- Iter #422
# maxdist: 0.00
# v: -0.70, 0.46, -0.55
# x: -0.8220127084204291055528951358066050422768706609558737200251218193387260254615382920631307559117370454
# y: 0.5421159080622184782140957168043560135446028731752014054843013329224748002108743629641849403645682400
# z: -0.6449961403890742801584524087469202119863863916260320128664605100905820587970848634481085306737357464
# delta: 3.421138828918010616971241593149871754348297397773605417810596662364209586059126675678402377452184078E-50
# best_intersect_points 30
# p0: 73350311083809.446, 437493425687373.247, 0.000, t: 0.131
# p1: 73350311083809.446, 437493425687373.247, 0.000, t: 0.423
# p2: 73350311083809.446, 437493425687373.247, 0.000, t: 0.632
# p3: 73350311083809.446, 437493425687373.247, 0.000, t: 0.552
# p4: 73350311083809.446, 437493425687373.247, 0.000, t: 0.574
# p5: 73350311083809.446, 437493425687373.247, 0.000, t: 0.532
# p6: 73350311083809.446, 437493425687373.247, 0.000, t: 0.331
# p7: 73350311083809.446, 437493425687373.247, 0.000, t: 0.421
# p8: 73350311083809.446, 437493425687373.247, 0.000, t: 1.003
# p9: 73350311083809.446, 437493425687373.247, 0.000, t: 0.728
# p10: ([Decimal('73350311083809.44597426857258008113610220695942384201528707402682882402295916556155880337776215623645'), Decimal('437493425687373.2470994071062554303618537416468315886615550095539793155955408367996285918618167311681'), Decimal('0')], Decimal('0.8518784710429999999999999999999999999999999999999991932173395475873355832907877310068514472369012444'))
