'''
Created on Nov 22, 2014

@author: Binoy Pilakkat
'''
from matplotlib import pyplot as plt
from numpy import arange,polyfit,polyval,power
class plot_wageningen:

    '''
    Plot for wageningen B propeller series B Characteristics
    '''


    def __init__(self, j,kt,kq,pd):
        '''
        Constructor
        '''
        self.rho = 1025 #kg/m^3
        self.jvals = j
        self.ktvals= kt
        self.kqvals = kq
        self.plt = plt
        self.pd = pd
        self.fig =self.plt.figure()
        self.kt_j_plt = self.fig.add_subplot(111)


        self.plt.grid(1)

    def plot_j_kt(self):
        i =0

        self.kt_j_plt.set_ylim(0,0.9)
        self.kt_j_plt.set_ylabel(r'$K_T$')
        for kt_arr in self.ktvals[1]:
#             kt_arr[kt_arr<0] = 0
            self.kt_j_plt.text(0.3, kt_arr[3], str(self.pd[i]))


            self.kt_j_plt.plot(self.jvals,kt_arr,'k')
            i += 1



    def plot_eta(self):
        i = 0
        for ktarr in self.ktvals[1]:
            eta = [((self.jvals[v]/(2*3.14))*(ktarr[v]/self.kqvals[1][i][v])) for v in range(len(ktarr))]
            print eta
            self.kt_j_plt.plot(self.jvals,eta)
    def plot_j_kq(self):
        i =0
        self.kq_j_plt = self.kt_j_plt.twinx()

        self.kq_j_plt.set_ylabel(r'$K_Q$')
        for kq_arr in self.kqvals[1]:
            self.kq_j_plt.plot(self.jvals,kq_arr,'m')

            i += 1

    def plot_cj2(self,x,y):
        self.plot_j_kt()
        self.plot_j_kq()
        self.kt_j_plt.plot(x,y)
        self.plt.show()

class plot_eta_n:
    def __init__(self,pltt,tit):
        self.plt = pltt
        self.fig = self.plt.figure()
        self.z =tit
        self.fig.suptitle("Number of blades ="+str(tit))
        self.leg = [str(i) for i in list(arange(0.3,1.05,0.05))]
        self.plt.grid(1)
        self.eff_cur = self.fig.add_subplot(111)
        self.eff_cur.set_xlabel(r'$P/D$')
        self.eff_cur.set_ylabel(r'$\eta_0$')



        self.n_cur = self.eff_cur.twinx()
        self.n_cur.set_ylabel(r'$n - rps$')

        self.leglist1 = []
        self.leglist2 = []

    def addplot(self,arr,lab):

        x   = arange(min(arr['pd']),max(arr['pd']),0.01)
#         print x
#         raise ValueError
        p1  = polyfit(arr['pd'], arr['eta'],3)
        p2 = polyfit(arr['pd'], arr['n'], 3)
        y1 = polyval(p1, x)
        y2 = polyval(p2,x)
        self.leglist1.append(self.eff_cur.plot(x,y1,label = str(lab)))
        self.leglist2.append(self.n_cur.plot(x,y2,label = str(lab)))

    def savefig(self):
        self.plt.savefig(str(self.z)+'.png')
if __name__ == "__main__":
    import ktkq
    #-------------- input parameters  ---------------------
    vs = 20.2       # Velocity of vessel in knows
    Rt = 114.3      # Total Resistance in kiloNewtons
    D  =  1.2       # Diameter of propeller
    h = 0.5         # Propeller immersion in Meters
    Delta =143      # Displacement in tonnes
    nProp= 1        # Number of Propellers
    #------------------------------------------------------
    (w,t) = (-.02,0.07)
    va = vs*(1-w)*.5144
    T = Rt/((1-t)*nProp)
    t = ktkq.ktkq(0.3,4,w,t,vs,Rt,D)
    ktvals =  t.generate_kt_curves()
    kqvals = t.generate_kq_curves()
    x = t.j
    tes= plot_wageningen(x,ktvals,kqvals,t.pd)
    tes.plot_j_kt()
    tes.plot_j_kq()
    tes.plot_eta()
    const =t.const_j2
    y = const
    tes.plt.show()

