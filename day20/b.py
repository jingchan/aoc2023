import math
import os
import re

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + '/1.txt'
IN_FILE = PATH + '/2.txt'
# IN_FILE = PATH + '/3.txt'

dirs = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]


def getsources(m, name):
    return [k for k, v in m.items() if name in v[1]]


def solve(m, end, c):
    q = list(m.keys()) + ['rx']
    while len(q) > 0:
        print('q', sorted(q))
        print('c', sorted(c))
        print('clen', len(c))
        name = q.pop(0)
        if name in c:
            continue
        print(name)

        if name == 'rx':
            srcs = getsources(m, name)
            ls = []
            ag = False
            for s in srcs:
                if s not in c:
                    if s not in q:
                        q.append(s)
                    ag = True
                else:
                    ls.append(c[s][0])
            if len(ls) == 0:
                q.append(name)
                continue
            c[name] = (min(ls), [-999])
            print('returning')
            return c[name]
            break
        tar = m[name][1]
        if m[name][0] == 'b':
            c[name] = ([1], [])
            for t in tar:
                if t in c:
                    c.pop(t)
                    q.append(t)
            continue
        elif m[name][0] == '%':
            srcs = getsources(m, name)
            ls = []
            ag = False
            for s in srcs:
                if s not in c:
                    if s not in q:
                        q.append(s)
                    # ag = True
                else:
                    ls.extend(c[s][0])
                    ls.extend([2 * x for x in c[s][0]])
                    ls.sort()
            if len(ls) == 0:
                q.append(name)
                continue
            c[name] = (
                [l for i, l in enumerate(ls) if i % 2 == 1],
                [l for i, l in enumerate(ls) if i % 2 == 0],
            )
            for t in tar:
                if t in c:
                    c.pop(t)
                    q.append(t)
            continue
        elif m[name][0] == '&':
            srcs = getsources(m, name)
            ls = []
            hs = []
            ag = False
            mls = []
            mhs = []
            shs = []
            for s in srcs:
                if s not in c:
                    if s not in q:
                        q.append(s)
                    ag = True
                else:
                    if c[s][1] == []:
                        if s not in q:
                            q.append(s)
                        ag = True
                    else:
                        ls.extend(c[s][0])
                        mls.append(min(c[s][0]))
                        ls.sort()
                        hs.extend(c[s][1])
                        shs.append(c[s][1])
                        mhs.append(min(c[s][1]))
                        hs.sort()
            if ag:
                q.append(name)
                continue

            maxofmin = max([h for h in mhs])
            if name == 'jj':
                print(name, 'srcs', srcs)
                print(name, 'mhs', mhs)
                print(name, 'maxofmin', maxofmin)
                exit()

            c[name] = (
                [maxofmin],
                # [h for h in hs if h >= maxofmin],
                ls + [h for h in hs if h < maxofmin],
            )
            # print(name, 'hs', shs)
            # if name == 'rk':
            #     exit()

            # if name == 'xz':
            #     print(name, 'hs', shs)
            #     print(name, 'ls', ls)
            #     print(name, 'maxmin', maxofmin)
            #     print(name, 'cname', c[name])
            #     exit()
            to_drop = []
            for t in tar:
                if t in c:
                    to_drop.append(t)
            for t in to_drop:
                c.pop(t)
                q.append(t)

            continue
            # return c[name]
        raise Exception('Unknown type')


with open(IN_FILE, 'r') as f:
    # line = f.readline()
    input = []
    total = 0
    ht = 0
    lt = 0
    m = {}
    for line in f.readlines():
        line = line.strip()
        sec = line.split(' -> ')
        tar = sec[1].split(', ')

        if sec[0] == 'broadcaster':
            m[sec[0]] = ['b', tar, {'low': [1], 'high': []}, {}]
        elif sec[0][0] == '%':
            m[sec[0][1:]] = ['%', tar, {'low': [], 'high': []}, {}]
        else:
            m[sec[0][1:]] = ['&', tar, {'low': [], 'high': []}, {}]

    for k, v in m.items():
        sources = []
        for kj, mj in m.items():
            if k in mj[1]:
                sources.append(kj)
                m[k][3][kj] = []
    # for k, v in m.items():
    #     if v[0] == '&':
    #         for kj, mj in m.items():
    #             if k in mj[1]:
    #                 v[2][kj] = False
    #     if v[0] in ['%', '&']:
    #         for kj, mj in m.items():
    #             if k in mj[1]:
    #                 v[4][kj] = None
    cache = {}
    # print(solve(m, 'xk', cache))
    # print(solve(m, 'jj', cache))
    print(solve(m, 'rx', cache))
    print('rx', cache['rx'], getsources(m, 'rx'))
    print('gh', cache['gh'], getsources(m, 'gh'))
    print('rk', cache['rk'], getsources(m, 'rk'))
    # print('jj', cache['jj'], getsources(m, 'jj'))
    # print(solve(m, 'jj', cache))
    # print('hb', cache['hb'])
    # print('mj', cache['mj'])
    # print('gf', cache['gf'])
    # print(sorted(cache.items()))
    exit()

    step = 1
    # Remove broadcaster from m
    # m.pop('broadcaster')
    # name high low presses
    senders = [('broadcaster', 1)]
    while senders:
        name, press = senders.pop(0)
        print(name, press)
        type, tar, emits, sources = m[name]

        if type == 'b':
            for t in tar:
                m[t][2]['high'].append(press)
                m[t][2]['low'].append(2 * press)
                senders.append((t, press))

        elif type == '%':
            for t in tar:
                if m[t][0] == '%':
                    m[t][2]['high'].append(press * 2)
                    m[t][2]['low'].append(press * 4)
                    senders.append((t, press * 2))
                elif m[t][0] == '&':
                    # fix
                    if (
                        len(
                            [
                                1
                                for k, v in m[t][3].items()
                                if k != name and v == []
                            ]
                        )
                        == 0
                    ):
                        m[t][2]['low'].append(press)
                        print('addlow', t, press)
                        senders.append((t, press))
                    else:
                        m[t][2]['high'].append(press)
                        m[t][3][name].append(press)
                        # senders.append((t, press))
        elif type == '&':
            for t in tar:
                if m[t][0] == '%':
                    m[t][2]['high'].extend(emits['high'])
                    m[t][2]['low'].extend(emits['high'])
                    senders.append((t, press))
                elif m[t][0] == '&':
                    m[t][2]['high'].extend(emits['high'])
                    senders.append((t, press))

        if type in ['b', '%'] and len(tar) == 0:
            m.pop(name)
            continue

        for k, v in m.items():
            if v[0] in ['&']:
                sources = []
                for kj, mj in m.items():
                    if k in mj[1]:
                        sources.append(kj)
                if k in ['rk', 'gh', 'cd', 'zf', 'qx']:
                    continue

                # lcm = 1
                # nosignal = False
                # for s in sources:
                #     if len(m[s][2]['high']) == 0:
                #         nosignal = True
                #         break
                #     lcm = max(max(m[s][2]['high']), lcm)
                # if nosignal:
                #     continue
                # print(m[k][2]['high'], lcm)
                # m[k][2]['high'].remove(lcm)
                # m[k][2]['low'].append(lcm)
                # for t in v[1]:
                #     senders.append(t)

    print(str.join('\n', [f'{k}: {v}' for k, v in m.items()]))

    # while len(senders) > 0:
    #     nsenders = []
    #     for name, sl, sh, st in senders:
    #         type, tar= m[name]
    #         if type == 'b':
    #             for t in tar:
    #                 ttype = m[t][0]
    #                 if ttype == '%':
    #                     nsenders.append((t, sl, sh, st))
    #                 elif ttype == '&':
    #                     nsenders.append((t, sl, sh, st))
    #         elif type == '%':
    #             for t in tar:
    #                 ttype = m[t][0]
    #                 if ttype == '%':
    #                     nsenders.append((t, 2*sl+1, 2*sh+1, 2*st))
    #                 else:
    #                     # Send high unless ...
    #                     nsenders.append((t, sl, sh+1, st))
    #         elif type == '&':
    #             for t in tar:
    #                 ttype = m[t][0]
    #                 # Send high unless ...
    #                 nsenders.append((name, sl, sh, st))
    #                 if ttype == '%':
    #                     nsenders.append((t, sl, sh, st))
    #                 elif ttype == '&':
    #                     nsenders.append((t, sl, sh, st))

# broadcaster -> a, b, c
# %a -> b
# %b -> c
# %c -> inv
# &inv -> a
# ['rk', 'cd', 'zf', 'qx']
