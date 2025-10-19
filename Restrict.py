from RatPlus import RatPlus
from Dihedron import Dihedron
from collections import namedtuple
import copy

def calculate():
    n = [3, -2, 0, 0, 0, 1]  # Integer coefficients of the polynumber 3-2x+x^5
    d = [[[[Dihedron(), Dihedron(), Dihedron()],
           [Dihedron(), Dihedron(), Dihedron()],
           [Dihedron(), Dihedron(), Dihedron()]],
          [[Dihedron(), Dihedron(), Dihedron()],
           [Dihedron(), Dihedron(), Dihedron()],
           [Dihedron(), Dihedron(), Dihedron()]],
          [[Dihedron(), Dihedron(), Dihedron()],
           [Dihedron(), Dihedron(), Dihedron()],
           [Dihedron(), Dihedron(), Dihedron()]]],
         [[[Dihedron(), Dihedron(), Dihedron()],
           [Dihedron(), Dihedron(), Dihedron()],
           [Dihedron(), Dihedron(), Dihedron()]],
          [[Dihedron(), Dihedron(), Dihedron()],
           [Dihedron(), Dihedron(), Dihedron()],
           [Dihedron(), Dihedron(), Dihedron()]],
          [[Dihedron(), Dihedron(), Dihedron()],
           [Dihedron(), Dihedron(), Dihedron()],
           [Dihedron(), Dihedron(), Dihedron()]]],
         [[[Dihedron(), Dihedron(), Dihedron()],
           [Dihedron(), Dihedron(), Dihedron()],
           [Dihedron(), Dihedron(), Dihedron()]],
          [[Dihedron(), Dihedron(), Dihedron()],
           [Dihedron(), Dihedron(), Dihedron()],
           [Dihedron(), Dihedron(), Dihedron()]],
          [[Dihedron(), Dihedron(), Dihedron()],
           [Dihedron(), Dihedron(), Dihedron()],
           [Dihedron(), Dihedron(), Dihedron()]]]]  # Initializing the 3x3x3x3 Dihedron matrix

    g = copy.deepcopy(d)  # Defining the generators

    t = (RatPlus(-1, 0), RatPlus(0, 1), RatPlus(1, 0))  # Generators begins with -INF, ZERO, INF

    # Populating the Generators
    for du in range(len(t)):
        for di in range(len(t)):
            for dj in range(len(t)):
                for dk in range(len(t)):
                    g[du][di][dj][dk] = Dihedron(t[du], t[di], t[dj], t[dk])

    r = []  # Roots of the Polynumber to be found. Exact or last value found in approximation.
    rpath = []  # Path of the roots found.
    q = 0  # Number of roots found
    s = [0, 0, 0, 0]  # Search index. Begins with ZERO, center of the 3x3x3x3 matrix. Can be -1, 0 or 1.
                      # Add 1 to match the index of the array (0, 1, 2).
    h = restrict(g, s)  # Searchers
    k = 0  # Number of searched levels
    min = 9999999999  # Minimum quadrance to search
    ve = []  # Verifications vector
    vq = []  # Verifications quadrance vector
    x = Dihedron()
    quad = min
    path = []
    x0 = Dihedron()
    x0 = h[s[0] + 1][s[1] + 1][s[2] + 1][s[3] + 1]
    print(f'{x0 = }')
    x = verify(x0, n)
    print(f'{x = }')
    ve.append(x)
    quad = x.quadrance()
    vq.append(quad)
    path.append([x0, s, 1/quad])
    if quad == 0:
        r[q] = x0
        q += 1
    elif quad < min:
        min = quad
    if q < len(n) - 1:
        k += 1
        ret = search(h, g, n, q, r, min, k, path, rpath, d, s)
    printAllPaths(rpath)
    print(f'{r = }')
    print(f'{path = }')
    print(f'{rpath = }')
    print('FIM.')
    return

def search(h, g, n, q, r, min, k, path, rpath, d, s):
    ve = copy.deepcopy(d)
    vq = copy.deepcopy(d)
    va = copy.deepcopy(d)
    vx = copy.deepcopy(d)  # Quadrance of x
    qi = namedtuple('qi', ['q', 'i'])
    vs = []
    vi = []
    quad = min
    maxk = 18
    if len(r) < (len(n) - 1) * 5 and k <= maxk:
        for du in range(3):
            for di in range(3):
                for dj in range(3):
                    for dk in range(3):
                        ve[du][di][dj][dk] = verify(h[du][di][dj][dk], n)
                        vx[du][di][dj][dk] = h[du][di][dj][dk].quadrance()
                        vq[du][di][dj][dk] = ve[du][di][dj][dk].quadrance()
                        va[du][di][dj][dk] = vq[du][di][dj][dk].__abs__()
                        vs.append(qi(va[du][di][dj][dk], (du - 1, di - 1, dj - 1, dk - 1)))
                        if va[du][di][dj][dk] < quad:
                            quad = va[du][di][dj][dk]
        vs.sort()
        for ind in vs:
            if ind.q == quad:
                vi.append(ind)
        # Delete the values previously searched
        vind = []
        for ind in vi:
            du, di, dj, dk = ind.i
            for p in path:
                if h[du + 1][di + 1][dj + 1][dk + 1] == p[0]:
                    vind.append(ind)
                    break
        i = [du, di, dj, dk]
        x = h[du + 1][di + 1][dj + 1][dk + 1]
        y = ve[du + 1][di + 1][dj + 1][dk + 1]
        q = 1 / vq[du + 1][di + 1][dj + 1][dk + 1]
        qx = 1 / vx[du + 1][di + 1][dj + 1][dk + 1]
        print(f'{k = } {i = } {x = } {qx = } {y = } {q = }')
        #print(f'{h[du + 1][di + 1][dj + 1][dk + 1] = }')
        #print(f'{path = }')
        for ind in vind:
            #vi.remove(ind)
            pass
        #print(f'{g = }')
        #print(f'{h = }')
        #print(f'{ve = }')
        #print(f'{vq = }')
        #print(f'{va = }')
        #print(f'{vs = }')
        #print(f'{vi = }')
        #print(f'{quad = }')
        for ind in vi:
            du, di, dj, dk = ind.i
            path.append([h[du + 1][di + 1][dj + 1][dk + 1],
                         [du, di, dj, dk],
                         1 / vq[du + 1][di + 1][dj + 1][dk + 1]
                         ])
            if quad == 0 or k >= maxk:
                r.append(h[du + 1][di + 1][dj + 1][dk + 1])
                q += 1
                k = 0
                rpath.append(path)
                path.pop()
            else:
                min = quad
                g1 = restrict(g , [du, di, dj, dk])
                h1 = restrict(g1, [ 0,  0,  0,  0])
                k += 1
                ret = search(h1, g1, n, q, r, min, k, path, rpath, d, s)
                k -= 1
                path.pop()
    return

def verify(v, p):
    y = Dihedron()
    coef = []
    potx = Dihedron()
    for i in range(len(p)):
        coef = Dihedron(p[i])
        if i == 0:
            potx = Dihedron(1)
        else:
            potx = v**i
        term = coef * potx
        y += term
    return y

def restrict(g, pos):
    h = copy.deepcopy(g)
    pu = pos[0]
    pi = pos[1]
    pj = pos[2]
    pk = pos[3]
    for u in range(3):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if pu == -1:
                        if u == 0:
                            t = g[0][i][j][k]._u
                        elif u == 1:
                            t = RatPlus.mediant(g[0][i][j][k]._u, g[1][i][j][k]._u)
                        elif u == 2:
                            t = g[1][i][j][k]._u
                    elif pu == 0:
                        if u == 0:
                            t = RatPlus.mediant(g[0][i][j][k]._u, g[1][i][j][k]._u)
                        elif u == 1:
                            t = g[u][i][j][k]._u
                        elif u == 2:
                            t = RatPlus.mediant(g[1][i][j][k]._u, g[2][i][j][k]._u)
                    elif pu == 1:
                        if u == 0:
                            t = g[1][i][j][k]._u
                        elif u == 1:
                            t = RatPlus.mediant(g[1][i][j][k]._u, g[2][i][j][k]._u)
                        elif u == 2:
                            t = g[2][i][j][k]._u
                    if pi == -1:
                        if i == 0:
                            x = g[u][0][j][k]._i
                        elif i == 1:
                            x = RatPlus.mediant(g[u][0][j][k]._i, g[u][1][j][k]._i)
                        elif i == 2:
                            x = g[u][1][j][k]._i
                    elif pi == 0:
                        if i == 0:
                            x = RatPlus.mediant(g[u][0][j][k]._i, g[u][1][j][k]._i)
                        elif i == 1:
                            x = g[u][i][j][k]._i
                        elif i == 2:
                            x = RatPlus.mediant(g[u][1][j][k]._i, g[u][2][j][k]._i)
                    elif pi == 1:
                        if i == 0:
                            x = g[u][1][j][k]._i
                        elif i == 1:
                            x = RatPlus.mediant(g[u][1][j][k]._i, g[u][2][j][k]._i)
                        elif i == 2:
                            x = g[u][2][j][k]._i
                    if pj == -1:
                        if j == 0:
                            y = g[u][i][0][k]._j
                        elif j == 1:
                            y = RatPlus.mediant(g[u][i][0][k]._j, g[u][i][1][k]._j)
                        elif j == 2:
                            y = g[u][i][1][k]._j
                    elif pj == 0:
                        if j == 0:
                            y = RatPlus.mediant(g[u][i][0][k]._j, g[u][i][1][k]._j)
                        elif j == 1:
                            y = g[u][i][j][k]._j
                        elif j == 2:
                            y = RatPlus.mediant(g[u][i][1][k]._j, g[u][i][2][k]._j)
                    elif pj == 1:
                        if j == 0:
                            y = g[u][i][1][k]._j
                        elif j == 1:
                            y = RatPlus.mediant(g[u][i][1][k]._j, g[u][i][2][k]._j)
                        elif j == 2:
                            y = g[u][i][2][k]._j
                    if pk == -1:
                        if k == 0:
                            z = g[u][i][j][0]._k
                        elif k == 1:
                            z = RatPlus.mediant(g[u][i][j][0]._k, g[u][i][j][1]._k)
                        elif k == 2:
                            z = g[u][i][j][1]._k
                    elif pk == 0:
                        if k == 0:
                            z = RatPlus.mediant(g[u][i][j][0]._k, g[u][i][j][1]._k)
                        elif k == 1:
                            z = g[u][i][j][k]._k
                        elif k == 2:
                            z = RatPlus.mediant(g[u][i][j][1]._k, g[u][i][j][2]._k)
                    elif pk == 1:
                        if k == 0:
                            z = g[u][i][j][1]._k
                        elif k == 1:
                            z = RatPlus.mediant(g[u][i][j][1]._k, g[u][i][j][2]._k)
                        elif k == 2:
                            z = g[u][i][j][2]._k
                    h[u][i][j][k] = Dihedron(t, x, y, z)
    return h

def printPath(path, idx):
    ri = []
    for p in path:
        ri.append(p[idx])
    return ri

def printAllPaths(rpath):
    rp0 = []
    rp1 = []
    rp2 = []
    for rp in rpath:
        rp0 = printPath(rp, 0)
        rp1 = printPath(rp, 1)
        rp2 = printPath(rp, 2)
    print(f'{rp0 = }')
    print(f'{rp1 = }')
    print(f'{rp2 = }')
    return
