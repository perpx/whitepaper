import numpy as np
from matplotlib import pyplot as plt

class Instrument():
    def __init__(self, vf):
        self.x = []
        self.y1 = []
        self.y2 = []
        self.y3 = []
        self.y4 = []
        self.y5 = []
        self.vf = vf
        
        self.pl = 0.
        
        self.oi = 0.
        self.cost = 0.
        
        self.pos = {}
        self.costs = {}
        
        self.price = 0.
        self.batch = []
        self.totvf = 0.
        
    def provide(self, N):
        self.pl += N
        
    def redeem(self, N):
        self.pl -= N
        
    def imbalance(self):
        return (self.oi * self.price) / self.pool()
    
    def fees(self, sz):
        s = sz * self.price
        ON = self.oi * self.price
        N = self.pool()
        top = s * (2 * ON + s) 
        bottom = 2 * N
        f = top / bottom
        vf = self.vf * np.abs(f)
        self.totvf += vf
        return 0.
        #return f + vf
    
    def update_price(self, price):
        self.price = price
        for b in self.batch:
            f = self.fees(b[1])
            #self.pl += f
            c = price * b[1] + f
            self.cost += c
            self.oi += b[1]
            if b[0] not in self.costs:
                self.costs[b[0]] = 0
            self.costs[b[0]] += c
            if b[0] not in self.pos:
                self.pos[b[0]] = 0
            self.pos[b[0]] += b[1]
            
        self.batch = []
        
    def pool(self):
        return self.pl - (self.price * self.oi - self.cost)
            
    def pnl(self):
        return self.price * self.oi - self.cost
            
    def trade(self, account, size):
        self.batch.append((account, size))
     
    def capture(self, x):
        self.x.append(x)
        self.y1.append(self.pool())
        self.y2.append(self.pnl())
        self.y3.append(self.oi)
        self.y4.append(self.imbalance())
        self.y5.append(self.price)
        
    def plot(self):
        plt.plot(self.x, self.y1, label="Liquidity pool")
        plt.legend()
        plt.show()
        plt.plot(self.x, self.y2, label="Traders' pnl")
        plt.legend()
        plt.show()
        plt.plot(self.x, self.y3, label="Traders' net positions")
        plt.legend()
        plt.show()
        plt.plot(self.x, self.y4, label="Imbalance")
        plt.legend()
        plt.show()
        plt.plot(self.x, self.y5, label="Price")
        plt.legend()
        plt.show()