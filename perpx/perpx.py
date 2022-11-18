import numpy as np
from matplotlib import pyplot as plt
import matplotlib.dates as md
import datetime as dt
import seaborn as sns


def norm(y):
    r = y - np.min(y)
    r = r / np.max(r)
    return r

class Instrument():
    def __init__(self, vf, neutral=False):
        self.neutral = neutral
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
        if self.neutral:
            return 0.
        s = sz * self.price
        ON = self.oi * self.price
        N = self.pool()
        top = s * (2 * ON + s) 
        bottom = 2 * N
        f = top / bottom
        vf = self.vf * np.abs(f)
        self.totvf += vf
        return f + vf
    
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
       
    def interpolate_dates(self):
        # remove the last 10 data because scattered on 2 last months
        cut = 10
        length = len(self.x) - cut

        samples = [1642824654, 1645539585, 1646301110, 1647418381, 1648100798, 1648447918, 1648738937, 1650080707, 1650515741, 1650924006, 1651632006, 1651918584, 1656052758]
        l = len(samples) - 1

        index = self.x[::int(length/l)]
        t = np.zeros((length,))
        offset = 0
        for i in range(len(samples)-1):
            t[offset:offset+int(length/l)] = np.linspace(samples[i], samples[i+1], int(length/l))
            offset += int(length/l)
        #print(t)
        # t = np.linspace(1642824654, 1660885879, len(self.x))
        dates=[dt.datetime.fromtimestamp(ts) for ts in t]
        #t = np.linspace(1642824654, 1660885879, len(self.x))
        #d = [dt.datetime.fromtimestamp(ts) for ts in t]
        self.y1 = self.y1[:-10]
        self.y2 = self.y2[:-10]
        self.y3 = self.y3[:-10]
        self.y4 = self.y4[:-10]
        self.y5 = self.y5[:-10]

        self.x = dates
        
    def plot_liquidity(self, ax, source):
        plt.ylabel("Amount in Liquidity Pool [Millions $]")
        plt.xlabel("Date [Month]")
        plt.xticks(rotation=25)
        ax.yaxis.set_major_formatter('{x:2.0f}')
        plt.plot(self.x, [i/1000000 for i in self.y1] , label="{}".format(source))
        plt.legend()
        plt.title("Evolution of Total Liquidity")
        sns.set()
        
    def plot_trader_pnl(self, ax, source):
        #plot 2
        plt.ylabel("Traders' PNL [Millions $]")
        plt.xlabel("Date [Month]")
        plt.xticks(rotation=25)
        ax.yaxis.set_major_formatter('{x:2.0f}')
        plt.plot(self.x, [i/1000000 for i in self.y2], label="{}".format(source))
        plt.legend()
        plt.title("Evolution of Traders' PNL")
        sns.set()
        
    def plot_trader_net_position(self, ax, source):
        #plot 3
        plt.ylabel("Traders' net positions [ETH]")
        plt.xlabel("Date [Month]")
        plt.xticks(rotation=25)
        plt.plot(self.x, self.y3, label="{}".format(source))
        plt.legend()
        plt.title("Evolution of Traders' net positions")
        sns.set()
        
    def plot_price(self, ax, source):
        #xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
        #ax=plt.gca()
        #ax.xaxis.set_major_formatter(xfmt)
        plt.ylabel("Price [$]")
        plt.xlabel("Date [Month]")
        plt.xticks(rotation=25)
        plt.plot(self.x, self.y5, label="{}".format(source))
        plt.legend()
        plt.title("Evolution of Ethereum Price")
        sns.set()
        
    def plot(self):
        #plot 1
        plt.ylabel("$")
        plt.xlabel("Date [Month]")
        plt.xticks(rotation=25)
        plt.plot(self.x, self.y1 , label="Liquidity pool")
        plt.legend()
        plt.show()
        
        #plot 2
        plt.ylabel("$")
        plt.xlabel("Date [Month]")
        plt.xticks(rotation=25)
        plt.plot(self.x, self.y2, label="Traders' pnl")
        plt.legend()
        plt.show()
        
        #plot 3
        plt.ylabel("$")
        plt.xlabel("Date [Month]")
        plt.xticks(rotation=25)
        plt.plot(self.x, self.y3, label="Traders' net positions")
        plt.legend()
        plt.show()
        
        #plot 4
        #plt.plot(self.x, norm(self.y4), label="Imbalance")
        plt.xticks(rotation=25)
        #xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
        #ax=plt.gca()
        #ax.xaxis.set_major_formatter(xfmt)
        plt.ylabel("$")
        plt.xlabel("Date [Month]")
        plt.plot(self.x, self.y5, label="Price")
        plt.legend()
        plt.show()