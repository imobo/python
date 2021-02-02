import math
import random

def monteCarlo(start, days):
    ndSum = 0
    movement = []
    for day in range(0, days):
        nd = normCdfInv(random.random())
        ndSum = ndSum + nd
        move = start * math.exp(ndSum)
        movement.append(move)
    return movement
        

def rationalApproximation(t):
    # Abramowitz and Stegun formula 26.2.23.
    # The absolute value of the error should be less than 4.5 e-4.
    c = [2.515517, 0.802853, 0.010328]
    d = [1.432788, 0.189269, 0.001308]
    numerator = (c[2]*t + c[1])*t + c[0]
    denominator = ((d[2]*t + d[1])*t + d[0])*t + 1.0
    result = t - numerator / denominator
    return result

def normCdfInv(p):
    if p > 0.0 and p < 1:
        if p < 0.5:
            # F^-1(p) = - G^-1(p)
            t = math.sqrt(-2.0*math.log(p))
            result = -rationalApproximation(t)
            return result
        else:
            # F^-1(p) = G^-1(1-p)
            t = math.sqrt(-2.0*math.log(1.0-p))
            result = rationalApproximation(t)
            return result
    else:
        print("Invaild p for normCdfInv")

mc = monteCarlo(10, 10)
print(mc)
