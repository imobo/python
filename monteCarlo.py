import math
import random
import matplotlib.pyplot as plt


def monteCarloStdOption(flag, S, K, T, r, b, sigma, n):
    # S: spot price
    # K: strike price
    # T: Time to maturity
    # r: interest rate
    # b: cost of carry
    # sigma: volatility of underlying asset
    # n: number of simulations

    drift = (b - sigma ** 2 / 2 ) * T
    vSqrdt = sigma * math.sqrt(T)
    if flag == "c":
        z = 1
    elif flag == "p":
        z = -1
    dataSum = 0
    for i in range(0, n):
        ST = S * math.exp(drift + vSqrdt * cndInv(random.random()))
        dataSum = dataSum + max(z * (ST - K), 0)
    return math.exp(-r * T) * dataSum  / n

    
def monteCarlo(start, days):
    ndSum = 0
    steps = [start]
    for day in range(0, days):
        nd = cndInv(random.random())
        ndSum = ndSum + nd
        step = start * math.exp(ndSum)
        steps.append(step)
        #print(nd, "\t", ndSum, "\t", step)
    return steps


def cndInv(u):
    # inverse cumulative normal distribution
    a = [2.50662823884, -18.61500062529, 41.39119773534, -25.44106049637]
    b = [-8.4735109309, 23.08336743743, -21.06224101826, 3.13082909833]
    c = [0.337475482272615, 0.976169019091719, 0.160797971491821, 2.76438810333863E-02, 3.8405729373609E-03, 3.951896511919E-04, 3.21767881767818E-05, 2.888167364E-07, 3.960315187E-07]
    x = u - 0.5
    if abs(x) < 0.92:
        r = x * x
        r = x * (((a[3] * r + a[2]) * r + a[1]) * r + a[0]) / ((((b[3] * r + b[2]) * r + b[1]) * r + b[0]) * r + 1)
        return r
    else:
        r = u
        if x >= 0:
            r = 1 - u
        r = math.log(-math.log(r))
        r = c[0] + r * (c[1] + r * (c[2] + r * (c[3] + r + (c[4] + r * (c[5] + r * (c[6] + r * (c[7] + r * c[8])))))))
        if x < 0:
            r = -r
        return r


def lineGraph(data):
    x = []
    for i in range(0, len(data)):
        x.append(i)
    plt.figure()
    plt.plot(x, data)  
    plt.xlabel("Days")
    plt.ylabel("Movement")
    plt.title("Monte Carlo Simulation Result")
    plt.show()
    
#mc = monteCarlo(80, 100)
#lineGraph(mc)
flag = "p"
S = 42
K = 40
T = 0.5
r = 0.1
b = 0
sigma = 0.2
n = 1000000

optPrice = monteCarloStdOption(flag, S, K, T, r, b, sigma, n)
print("The simulation result of opition price is",round(optPrice,4))
print("Simulation parameters are:\n Spot price:", S, "\tStrike price:", K, "\tTime to maturity:", T,
      "\n Interest rate:", r, "\tCost of carry:", b, "\tVolatility:", sigma,
      "\n Simulation times:", n)
