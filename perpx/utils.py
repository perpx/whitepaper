import numpy as np

def sortino(p, freq):
    p = np.array(p)
    rets = (p[1:] / p[:-1]) - 1.
    N = (1000 * 60 * 60 * 24 * 365) / freq
    return (np.mean(rets) * N) / (np.std(rets[rets < 0.]) * np.sqrt(N))
def sharpe(p, freq):
    p = np.array(p)
    rets = (p[1:] / p[:-1]) - 1.
    N = (1000 * 60 * 60 * 24 * 365) / freq
    return (np.mean(rets) * N) / (np.std(rets) * np.sqrt(N))

