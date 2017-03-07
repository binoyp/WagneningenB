'''
Created on Nov 25, 2014

@author: Binoy Pilakkat
'''
from ktkq import *

import matplotlib.pyplot as plt
from plot_wageningen import plot_eta_n,plot_wageningen
def printRep(dic):
    print "Results \n  "
    for z in dic:
        print " Optimized Propeller Parameters for No. of Blades = ",z
        for k in dic[z]:
            print k,":",dic[z][k]
def fullreport(arr,T,va,h,D):
    for dic in arr:
        cno = cavitationNo(h, va, dic[0]['n'], D)
        tooh= toh(T,dic[0]['pd'],va,dic[0]['n'],D)
        cavPerc =cavitationPercent(cno, tooh)
        print "----"*10
        for k in dic[0]:

            print k,":",dic[0][k]
        print "C.No:",cno
        print "tto:",tooh
        print "Percentage Cavitation:",cavPerc

if __name__ == '__main__':

    #-------------- input parameters  ---------------------
    vs = 20       # Velocity of vessel in knows
    Rt = 174.5     # Total Resistance in kiloNewtons
    D  =  1.1       # Diameter of propeller
    h   = 0.55         # Propeller immersion in Meters
    Delta =143      # Displacement in tonnes
    nProp= 2        # Number of Propellers
    #------------------------------------------------------
    (w,t) = (-.04,0.07)
    va = vs*(1-w)*.5144
    T = Rt/((1-t)*nProp)

    totalAnalysis= []
    bestPropellers={}
    keyVals = ['Pitch Ratio','rps','efficiency','BAR','Z','Cavitation Percent']
    for pbd in range(2,8):
        pl = plot_eta_n(plt,pbd)
        bestd =OptimizePropeller(D,w, t, vs,r=Rt*1000,z=pbd,pltcur = pl)
        totalAnalysis.append(bestd)
        plt.legend(loc=0,prop={'size':7})
        pl.savefig()

        l = Optimum_n(bestd,h,va,D,T,1)
        bestPropellers[pbd] = dict(zip(keyVals,l))


    printRep(bestPropellers)
    fullreport(totalAnalysis, T, va, h, D)
    plt.show()


