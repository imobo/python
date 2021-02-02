import math

def euroVanillaCall(S, K, T, r, sigma):
    # S: spot price
    # K: strike price
    # T: time to maturity
    # r: interest rate
    # sigma: volatility of underlying asset
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = (math.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    call = S * cdf(d1) - K * math.exp(-r * T) * cdf(d2)
    return call


def euroVanillaPut(S, K, T, r, sigma):
    # S: spot price
    # K: strike price
    # T: time to maturity
    # r: interest rate
    # sigma: volatility of underlying asset    
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = (math.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    put = (K * math.exp(-r * T) * cdf(-d2) - S * cdf(-d1))
    return put


def cdf(x):
    q = 1/(1 + 0.2316419 * abs(x))
    primex = 1 / math.sqrt(2 * math.pi) * math.exp(-(x * x / 2))
    dum = (1.781477937 + q * (-1.821255978 + 1.330274429 * q))
    dum = primex * (q * (0.31938153 + q * (-0.356563782 + q * dum)))
    if x < 0:
        cdfResult = dum
        return cdfResult
    else:
        cdfResult = 1 - dum
        return cdfResult


evc = euroVanillaCall(50, 100, 1, 0.05, 0.25)
evp = euroVanillaPut(50, 100, 1, 0.05, 0.25)

print("Call price is", evc) # 0.027348025148272115
print("Put price is", evp)  # 45.15029047521967
