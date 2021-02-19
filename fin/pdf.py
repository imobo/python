import math

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

