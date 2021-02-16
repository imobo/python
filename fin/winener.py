import math
import random
import matplotlib.pyplot as plt


def winener(N):
    T = 1.0
    N = N + 1
    dt = T / (N - 1)
    dx = [0] * N
    X = [0] * N
    for i in range(1, N):
        r = random.gauss(0, 1)
        dx[i] = r * math.sqrt(dt)
        X[i] = X[i-1] + dx[i]
    return X
    
    
def lineGraph(data):
    x = []
    for i in range(0, len(data)):
        x.append(i)
    plt.figure()
    plt.plot(x, data)  
    plt.xlabel("Days")
    plt.ylabel("Movement")
    plt.title("Result")
    plt.show()

n = 1000
lineGraph(winener(n))
