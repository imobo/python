import math
import random
import matplotlib.pyplot as plt


def winener(N, a=None, b=None):
    """
    @ para: N - int - simulate time
    @ para: a - int - constant mu
    @ para: b - int - constant sigma
    @ output: X - list - simulation result
    """
    T = 1.0
    N = N + 1
    dt = T / (N - 1)
    dx = [0] * N
    X = [0] * N
    for i in range(1, N):
        r = random.gauss(0, 1)
        if a == None or b == None:
            # Winener: dx = dz = ND(0,1) * sqrt(dt)
            dx[i] = r * math.sqrt(dt)
        else:
            # Generalized Winener: dx = a * dt + b * dz
            dx[i] = (a * dt) + (b * r * math.sqrt(dt))
        X[i] = X[i-1] + dx[i]
    return X


def ito(N):
    T = 1.0
    N = N + 1
    dt = T / (N - 1)
    dx = [0] * N
    X = [0] * N
    for i in range(1, N):
        # ND(0,1)
        r = random.gauss(0, 1)
        # get a(mu) and b(sigma)
        a = max(0, X[i]) ** 1/2
        b = max(1, i)
        # dx = a(x, t) * dt + b(x, t) * dz
        dx[i] = (a * dt) + (b * r * math.sqrt(dt))
        X[i] = X[i-1] + dx[i]
    return X


def lineGraph(data,title):
    x = []
    for i in range(0, len(data)):
        x.append(i)
    plt.figure()
    plt.plot(x, data)  
    plt.xlabel("Days")
    plt.ylabel("Movement")
    title = title + " Result"
    plt.title(title)
    plt.show()


def multiLineGraph(times, n, title):
    plt.figure()
    for t in range(0, times):
        data = winener(n)
        x = []
        for i in range(0, len(data)):
            x.append(i)
        plt.plot(x, data)
    plt.xlabel("Days")
    plt.ylabel("Movement")
    title = title + " Result"
    plt.title(title)
    plt.show()


n = 1000
a = 0.3
b = 1.5
#lineGraph(winener(n),"Winener process")
#lineGraph(winener(n,a,b),"Generalized Winener process")
#lineGraph(ito(n),"Ito process")
multiLineGraph(1000, 100, "Multipule Winener process")
