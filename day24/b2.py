# %%


PATH = os.path.dirname(__file__)
IN_FILE = PATH + '/2.txt'

f = open(IN_FILE, 'r')
st = []
for line in f.readlines():
    line = line.strip()
    pos = [int(x) for x in line.split(' @ ')[0].split(', ')]
    vel = [int(x) for x in line.split(' @ ')[1].split(', ')]
    st.append((pos, vel))
    # grid.append(list(line))


# # v = [0.9611890119460773, -0.23008670339787538, -0.152235975490755]
#     # v = [0.8161500531774176, 0.5532476800966718, -0.16678157921709794]
#     # points = [[p, vecadd(p, vecmul(v, 10**12))] for p, v in st]
#     points = [[p, vecadd(p, vecmul(v, 10**12))] for p, v in st[:100]]
# %%
import math
from decimal import Decimal, getcontext

getcontext().prec = 100


def vecsub(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2])


def project_to_plane(p1, normal):
    return vecsub(p1, vecmul(normal, dotproduct(p1, normal)))


def vecmul(p1, m):
    return (p1[0] * m, p1[1] * m, p1[2] * m)


def dotproduct(p1, p2):
    return p1[0] * p2[0] + p1[1] * p2[1] + p1[2] * p2[2]


def vecdiv(p1, d):
    return (p1[0] / d, p1[1] / d, p1[2] / d)


def vecadd(p1, v1):
    return (p1[0] + v1[0], p1[1] + v1[1], p1[2] + v1[2])


def norm(p1):
    return ((p1[0] ** 2) + p1[1] ** 2 + p1[2] ** 2).sqrt()


# %%
soln_v = (
    Decimal(
        '0.8338469323242109228509496744432200440338028452456110780359116462001089279650001967854811012135528057'
    ),
    Decimal(
        '-0.5499205575184760208049273838621954391751166489179031042696699937750498678846225626852022635124915333'
    ),
    Decimal(
        '0.04781917891465008876564585946627811774522499833060494278039788750958927489123342257184112180641875070'
    ),
)
print(norm(soln_v))
# soln_v = (-0.3693305798577347, 0.896682421249508, -0.24404007499603284)
points = [[p, vecmul(v, Decimal(10**10))] for p, v in st[:10]]
projected = [
    (project_to_plane(p, soln_v), project_to_plane(v, soln_v))
    for p, v in points
]
normal = (Decimal(0), Decimal(0), Decimal(1))
projected = [
    (project_to_plane(p, normal), project_to_plane(v, normal))
    for p, v in points
]
print(projected)

# %%
soln_p = (
    Decimal(
        '212027599315279.6271292417353710932170342591550309943365678785079930845606526517518753243280253983235'
    ),
    Decimal(
        '346036002624324.8122158405759559815260604833819123030965386838035283539876009669834177694331431614053'
    ),
)
print(soln_p)
# '212027599315279.6271292417353710931993739191251120059494479440760827267864449419791451291696362021972'
# '346036002624324.8122158405759559814988416358288002276995099634147670710659933658215585368503266703637'
tvals = [
    ((soln_p[0] - p[0]) / v[0], (soln_p[1] - p[1]) / v[1]) for p, v in projected
]
print(tvals)
# 212027599315297.12, 346036002624378.8

# p0: 272441739892584.812, 306192985182661.178, 0.000, t: 0.131
