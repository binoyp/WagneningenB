# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 12:20:11 2015

@author: Binoy
"""

from loadparam import ktparam,kqparam
import numpy as np
import matplotlib
matplotlib.style.use('bmh')
import matplotlib.pyplot as plt
from tabulate import tabulate
param_kt = ktparam()
param_kq = kqparam()


def kt(j,pd,aea0,z):
    term_array = np.zeros(39,dtype=np.float64)
    for i in range(39):
        c = param_kt['c'][i]
        t = param_kt['t'][i]
        u = param_kt['u'][i]
        v = param_kt['v'][i]
        s = param_kt['s'][i]
        base = np.array([c,j,pd,aea0,z])
        exp =  np.array([1,s,t,u,v])
        term_array[i] = np.prod(np.power(base,exp))
    return np.sum(term_array)
    
    
def kq(j,pd,aea0,z):
    term_array = np.zeros(47,dtype = np.float64)
    for i in range(47):
        c = param_kq['c'][i]
        t = param_kq['t'][i]
        u = param_kq['u'][i]
        v = param_kq['v'][i]
        s = param_kq['s'][i]
#            print c
        base = np.array([c,j,pd,aea0,z])
        exp =  np.array([1,s,t,u,v])
        term_array[i] = np.prod(np.power(base,exp))
    return np.sum(term_array)
    
    
if __name__ =="__main__":
    pd = 0.75
    aea0 = 0.6
    z = 4
    jvals = np.arange(0.01,1.5,.1) 
    js =[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    
    kqs = [kq( j, pd, aea0, z) for j in js]
    kts = [kt( j, pd, aea0, z) for j in js]
        
    tab = np.transpose(np.vstack((js,kqs,kts)))
    print tabulate(tab,headers = ['j' ,'kq', 'kt'],tablefmt = "grid", stralign = 'right')
    kqvals = np.array([kq(v,pd, aea0,z)*10 for v in jvals])
    ktvals = np.array([kt(v,pd, aea0,z) for v in jvals])
    ktfit = np.polyfit(jvals,ktvals,3)
    kqfit = np.polyfit(jvals, kqvals, 3)
#    print ktfit
    plt.plot(jvals,kqvals, label = "$10 K_Q$",linewidth=1)
    plt.plot(jvals,ktvals, label = "$K_T$",linewidth=1)
#    eta_o = (jvals/2*3.14)*(ktvals/kqvals)
#    plt.plot(jvals,eta_o,label='$\eta$')
    x = np.arange(0,1.5,0.01)
    y = np.polyval(ktfit,x)
    plt.plot(x,y,'+')
    plt.grid(1)
    
    ktident =  0.16228260

    pol2 = ktfit[:]
    pol2[-1] = pol2[-1] - ktident
    polsol = np.roots(pol2)
    selj = filter(lambda x: (float(x)>0) & (float(x) <1.4), polsol)[0]
    print polsol
#    selj = polsol[-1]
    plt.hlines(ktident, 0, selj, linestyle= '--',linewidth=1)
    plt.vlines(selj,0,kt(selj,pd,aea0,z), linestyle= '--',linewidth=1)
    plt.ylim(0,0.5)
    plt.legend()
    plt.show()
    plt.title(r'$\frac{P}{D} = 0.75, A_E /A_0 = 0.6, z = 4 $')
    plt.tight_layout()
   