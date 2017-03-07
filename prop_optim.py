# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 12:20:11 2015

@author: Binoy
"""

from loadparam import ktparam,kqparam
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
param_kt = ktparam()
param_kq = kqparam()


def kt(j,pd,aea0,z):
    """
    Calculate kt = Thrust coefficient
    j = advance velocity
    pd = pitch ratio
    aea0 = BAR
    z = Number of blades
    """
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
    """
    Calculate kq = Torque coefficient 
    j = advance velocity
    pd = pitch ratio
    aea0 = BAR
    z = Number of blades
    """
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

def ktpds(j, pds,aeao,z):
    """
    Calculate kt = Thrust coefficient  for different pitch ratios
    j = advance velocity as array
    pd = pitch ratio as array
    aea0 = BAR
    z = Number of blades 
    returns
    kt for pd / j
    +------+-------------+-------------+------------+-------------+
    | j/pd |         0.6 |         0.8 |        1.0 |         1.2 |
    +======+=============+=============+============+=============+
    """
    nj = len(j)
    
    outArr = np.zeros((nj), dtype =[('j','f8')]+ [ (str(pd), 'f8') for pd in pds])

    for row in range(nj):
        outArr[row] =  np.array([j[row]]+[ kt(j[row], pd, aea0,z) for pd in pds])

    return outArr

def kqpds(j, pds,aeao,z):
    """
    Calculate kq = Torque coefficient  for different pitch ratios
    j = advance velocity as array
    pd = pitch ratio as array
    aea0 = BAR
    z = Number of blades    
    
    Return numpy structured array
    kq for pd / j
    +------+-------------+-------------+------------+-------------+
    | j/pd |         0.6 |         0.8 |        1.0 |         1.2 |
    +======+=============+=============+============+=============+
    """    
    nj = len(j)
    
    outArr = np.zeros((nj), dtype =  [('j','f8')] +[(str(pd), 'f8') for pd in pds])
    
    for row in range(nj):
        outArr[row] =  np.array([j[row]]+[ kq(j[row], pd, aea0,z) for pd in pds])

    return outArr

def pltTab(ax, tab):
    """
    ax = Matplotlib axis
    tab = numpy structure array
    
    
    """
    nms = tab.dtype.names
    
    for  n in nms:
        if n != 'j':
            ax.plot(tab['j'], tab[n])
    ax.set_ylim(0,1)
 

def getIntersect(x1,y1, x2, y2, deg1,deg2):
    """
    Find roots of two curves
    x1, y1 -> arrays first polynomial
    x2, y2 -> arrays second polynomial
    deg1 -> degree of x1, y1
    deg2 -> degree of x2, y2
    return intersection
    """
    fit1 = np.polyfit(x1,y1,deg1)
    fit2  = np.polyfit(x2, y2, deg2)
    eqn = fit1 - fit2
    roots = np.roots(eqn)
    return roots
    
def plotInter(ax, x, y):
    """
    Draw ordinates (x, y)
    ax - maplotlib axes object
    """
    ax.hlines(y, 0, x)
    ax.vlines(x,0,y)
    
    
if __name__ == "__main__":
    
    pds = np.arange(0.6, 1.4, 0.2)
    pdnams = [ str(i) for i in pds]
    aea0 = 0.55
    z = 4
    jvals = np.arange(0.01,1.5,.05) 
    js =[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    tabkt = ktpds(jvals, pds, aea0, z)
    tabkq = kqpds(jvals, pds, aea0, z)
    f, ax = plt.subplots()
    pltTab(ax, tabkt)
    
    print '\n kt for pd / j\n'+ tabulate(tabkt, headers= list(tabkt.dtype.names), tablefmt='grid')
#    print '\n kq for pd / j\n'+ tabulate(tabkq, headers= list(tabkt.dtype.names), tablefmt='grid')
    # Optimium n from D
    v_ship = 15 * 0.5144 # velocity in metre per seconds
    D = 5.2 # metres
    w = 0.3 # wake
    T =  525 # kilo newtons
    rho = 1.025 # t/m3
    
#    Pd = 5250 #kN
#    n = 120 /60 #rps
#    Q = Pd /(2*3.14*n)

    va = v_ship * (1- w) # advance velocity

    kt_j2 = (T / (rho * va **2 * D**2)) * jvals**2
#    kq_j2 = ((Q*n**5) / (rho * va ** 5)) *jvals**5
#    ft = np.polyfit(jvals, kt_j2, 3)
    
    
#    jj = np.arange(0,1.5,0.01)
#    yy = np.polyval(ft, jj)
#    ax.plot(jj,yy)
    ax.grid(1)
    
    optivals = np.zeros((len(pds)), dtype = [('pd','f8'),('j', 'f8'), ('kt','f8'), ('kq', 'f8'),('eta', 'f8')])
    
    row = 0 
    for j in pdnams:
        curint = getIntersect(jvals, tabkt[j], jvals, kt_j2, 3, 3)
        valans = filter(lambda x : x > 0 and x <  max(jvals), curint)
        cj = valans[0]
        ckt = kt(valans[0],float(j), aea0, z)
        ckq = kq(valans[0],float(j), aea0, z)
        eta0 = (cj * ckt)/ (ckq *2 * 3.14)
        optivals[row] = np.array([float(j), cj, ckt , ckq,eta0])
        
        plotInter(ax,  valans[0], kt(valans[0],float(j),aea0,z))
        row +=1 
    optietafit = np.polyfit(optivals['j'], optivals['eta'],3)
    j4eta = np.linspace(min(optivals['j']),max(optivals['j']),50)
    eta_fiteval = np.polyval(optietafit, j4eta)
    dereta = np.polyder(optietafit)
    optipt = np.roots(dereta)
    opti_rps = va/(optipt*D)
    print opti_rps
    plotInter(ax, optipt[1], np.polyval(optietafit,optipt[1]))
    print tabulate(optivals, headers = list(optivals.dtype.names), tablefmt ='grid')
#    print "Max eff J vals:",optipt
#    print "P/D:", np.interp(optipt,optivals['j'],optivals['pd'])
    tab_opt = np.vstack((optipt,np.polyval(optietafit,optipt),np.interp(optipt,optivals['j'],optivals['pd'])))
    ax.plot(j4eta,eta_fiteval)
    ax.plot(optivals['j'], optivals['eta'],'o')
    print tabulate(list(np.transpose(tab_opt)),headers =['j','eta','p/d'],tablefmt='grid')
    ax.plot(jvals, kt_j2)
#    
#    
#    
#    
#    
#    
#    
#    
#    
#    plt.show()

    
    #############################################################################################
#     kqs = [kq( j, pd, aea0, z) for j in js]                                               #
#     kts = [kt( j, pd, aea0, z) for j in js]                                               #
#                                                                                           #
#     tab = np.transpose(np.vstack((js,kqs,kts)))                                           #
#     print tabulate(tab,headers = ['j' ,'kq', 'kt'],tablefmt = "grid", stralign = 'right') #
#     kqvals = np.array([kq(v,pd, aea0,z)*10 for v in jvals])                               #
#     ktvals = np.array([kt(v,pd, aea0,z) for v in jvals])                                  #
#     ktfit = np.polyfit(jvals,ktvals,3)                                                    #
#     kqfit = np.polyfit(jvals, kqvals, 3)                                                  #
#     print ktfit                                                                           #
#     plt.plot(jvals,kqvals, label = "$10 K_Q$")                                            #
#     plt.plot(jvals,ktvals, label = "$K_T$")                                               #
#                                                                                           #
#     x = np.arange(0,1.5,0.01)                                                             #
#     y = np.polyval(ktfit,x)                                                               #
#     plt.plot(x,y,'+')                                                                     #
#     plt.grid(1)                                                                           #
#                                                                                           #
#     ktident =  0.12487805                                                                 #
#     pol2 = ktfit[:]                                                                       #
#     pol2[-1] = pol2[-1] - ktident                                                         #
#     polsol = np.roots(pol2)                                                               #
#     selj = filter(lambda x: (float(x)>0) & (float(x) <1.4), polsol)[0]                    #
#     print polsol                                                                          #
# #    selj = polsol[-1]                                                                    #
#     plt.hlines(ktident, 0, selj)                                                          #
#     plt.vlines(selj,0,kt(selj,pd,aea0,z))                                                 #
#     plt.ylim(0,0.5)                                                                       #
#     plt.legend()                                                                          #
#     plt.show()                                                                            #
#############################################################################################
        
   
