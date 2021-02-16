import math
import random
import matplotlib.pyplot as plt


def winener(N, a=None, b=None):
    T = 1.0
    N = N + 1
    dt = T / (N - 1)
    dx = [0] * N
    X = [0] * N
    for i in range(1, N):
        # ND(0,1)
        r = random.gauss(0, 1)
        if a == None or b == None:
            # Winener: dx = dz = ND(0,1) * sqrt(dt)
            dx[i] = r * math.sqrt(dt)
        else:
            # General Winener: dx = a dt * b dz
            dx[i] = (a * dt) * (b * r * math.sqrt(dt))
        X[i] = X[i-1] + dx[i]
    return X

    
def normpdf(x, mu, sigma):
    result = 1 / (sigma * math.sqrt(2 * math.pi)) * math.exp( - (x - mu) **2 / (2 * sigma **2))
    return result

"""
def normpdf(x, mean, sd):
    var = float(sd)**2
    denom = (2*math.pi*var)**.5
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    return num/denom
"""
    
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


n = 1000
a = 0.3
b = 1.5
lineGraph(winener(n),"Winener process")
lineGraph(winener(n,a,b),"General Winener process")
