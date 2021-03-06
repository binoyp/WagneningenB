'''
Created on Nov 20, 2014

@author: Binoy Pilakkat
'''
from loadparam import ktparam,kqparam
import numpy as np
class optimum_j:

    def __init__(self):
        self.goodparams = {}
        self.index =1

    def addval(self,dec):
        self.goodparams[self.index] = dec
        self.index +=1
    def best(self,val = 0):
        out = None

        for dic in self.goodparams:
#             print "eff",self.goodparams[dic]['efficiency']
            if self.goodparams[dic]['efficiency'] > val:
                val = self.goodparams[dic]['efficiency']
                out = self.goodparams[dic]
        return out
class ktkq:
    '''
   calculation of kt and kq
    '''

    def __init__(self,aea0,z,w,t,vs,r=1143*10**3,Dia = 1.2):
        '''
        aea0 is blade area ratio
        z is number of blades
        vs in knots
        r is resistance in Newtons

        '''
        self.w = w
        self.t = t
        self.va = vs* (1- w)*.5144


        self.rho = 1025
        self.nu = 1.1881*10**-6
        self.param_kt = ktparam()
        self.param_kq = kqparam()
        self.area_ratio = aea0
        self.D = Dia
        self.Z   = z
        self.rt = r/(1-t)
        self.const_j2 =  self.rt/(self.rho*self.D**2*self.va**2)
        self.pd = np.arange(0.5,1.5,0.1)    # pitch to diameter ratio array
        self.j  = np.arange(0.01,1.5,.1)      # advance coefficient array
        dval = str(len(self.pd))+'f8'
        self.kt_curves = np.zeros_like(self.pd,dtype = (dval))
        
    def kt(self,j,pd,aea0,z):
        term_array = np.zeros(39,dtype=np.float64)
        for i in range(39):
            c = self.param_kt['c'][i]
            t = self.param_kt['t'][i]
            u = self.param_kt['u'][i]
            v = self.param_kt['v'][i]
            s = self.param_kt['s'][i]
            base = np.array([c,j,pd,aea0,z])
            exp =  np.array([1,s,t,u,v])
            term_array[i] = np.prod(np.power(base,exp))
        return np.sum(term_array)
        
    def efficiency(self,kt,kq,j):
        return (j/(2*3.14))*(kt/kq)

    def kq(self,j,pd,aea0,z):
        term_array = np.zeros(47,dtype = np.float64)
        for i in range(47):
            c = self.param_kq['c'][i]
            t = self.param_kq['t'][i]
            u = self.param_kq['u'][i]
            v = self.param_kq['v'][i]
            s = self.param_kq['s'][i]
#            print c
            base = np.array([c,j,pd,aea0,z])
            exp =  np.array([1,s,t,u,v])
            term_array[i] = np.prod(np.power(base,exp))
        return np.sum(term_array)

    def generate_kt_curves(self):
        """
        Generate kt curve for each p/d ratio
        .5 <= p/d <= 1.5
        area ratio is constant and is declared at init
        z is constant and is declared at init
        j is 0 to 1.5
        """

        dval = str(len(self.j))+'f8'
        kt_array = np.zeros_like(self.pd,dtype = (dval))
        dkt_array = np.zeros_like(self.pd,dtype = (dval))
        area_rat = self.area_ratio

        for i in range(np.shape(kt_array)[0]):
            curArr = np.zeros_like(self.j,dtype = np.float64)
            dcurArr = np.zeros_like(self.j,dtype = np.float64)
            for j in range(len(self.j)):
                curArr[j] = self.kt(self.j[j], self.pd[i], area_rat, self.Z)
                delkt = np.nan_to_num(self.Delta_kt(curArr[j], self.j[j], area_rat,\
                                                      self.pd[i], self.Z))
                dcurArr[j] =curArr[j]+ delkt
            kt_array[i] = curArr
            dkt_array[i]= dcurArr
        return [kt_array,dkt_array]

    def generate_kq_curves(self):
        """
        Generate kq curve for each p/d ratio
        .5 <= p/d <= 1.5
        area ratio is constant and is declared at init
        z is constant and is declared at init
        j is 0 to 1.5
        """
        dval = str(len(self.j))+'f8'
        kq_array = np.zeros_like(self.pd,dtype = (dval))
        dkq_array = np.zeros_like(self.pd,dtype = (dval))
        area_rat = self.area_ratio
        for i in range(np.shape(kq_array)[0]):
            curArr = np.zeros_like(self.j,dtype = np.float64)
            dcurArr = np.zeros_like(self.j,dtype = np.float64)
            for j in range(len(self.j)):
                curArr[j] = self.kq(self.j[j], self.pd[i], area_rat, self.Z)
                delkq =np.nan_to_num(self.Delta_kq(curArr[j], self.j[j], area_rat,\
                                                      self.pd[i], self.Z))
                dcurArr[j] =curArr[j]+ delkq
            kq_array[i] = curArr
            dkq_array[i] = dcurArr

        return [kq_array,dkq_array]

    def n(self,v,j,d):
        """
        calculate n using j
        """
        if j == 0:
            return 0
        return v/(j*d)
    def chord(self,bar,d,z):
        return (2.073*bar*d)/z
    def Delta_kt(self,kt,j,area_rat,pd,z):
        """

        """
        vr = np.sqrt((0.7*np.pi*self.va/j)**2 + self.va**2)
        Rn = (vr * self.chord(area_rat,self.D,self.Z))/self.nu

        out = 0.000353485-(0.00333758*area_rat*j**2)\
        -(0.00478125*area_rat*pd*j**2)\
        +(0.000257792*(np.log10(Rn)-0.301)**2*area_rat*j**2)\
        +(0.0000643192*(np.log10(Rn)-0.301)* pd**6*j**2)\
        -(0.0000110636*(np.log10(Rn)-0.301)**2*pd**6*j**2)\
        -(0.0000276305*(np.log10(Rn)-0.0)**2*z*area_rat*j**2)\
        +(0.0000954*(np.log10(Rn)-0.301)*z*area_rat*pd*j)\
        +(0.0000032049*(np.log10(Rn)-0.301)*z**2*area_rat*pd**3*j)
        if Rn <> 2*10**6:
            return out
        else:
            return 0
    def Delta_kq(self,kq,j,area_rat,pd,z):
        vr = np.sqrt((0.7*np.pi*self.va/j)**2+self.va**2)
        Rn = (vr * self.chord(area_rat,self.D,self.Z))/self.nu
        out = -0.000591412\
         +0.00696898*pd\
         -0.0000666654*z*pd**6\
         +0.0160818*area_rat**2\
         -0.000938091*(np.log10(Rn)-0.301)*pd\
         -0.00059593*(np.log10(Rn)-0.301)*pd**2\
         +0.0000782099*(np.log10(Rn)-0.301)**2*pd**2\
         +0.0000052199*(np.log10(Rn)-0.301)*z*area_rat*j**2\
         -0.00000088528*(np.log10(Rn)-0.301)**2*z*area_rat *pd*j\
         +0.0000230171*(np.log10(Rn)-0.301)*z*pd**6\
         -0.00000184341*(np.log10(Rn)-0.301)**2*z *pd**6\
         -0.00400252*(np.log10(Rn)-0.301)*area_rat**2\
         +0.000220915*(np.log10(Rn)-0.301)**2*area_rat**2
        if Rn <> 2*10**6:
            return out
        else:
            return 0


    def kt_j2(self,inpclass,plot=0):
        ktarr = self.generate_kt_curves()[1]
        x = self.j
        y = self.j**2 * self.const_j2
        cur = np.polyfit(x,y,2)
        poly_ktarr = [(self.pd[i],np.polyfit(self.j,ktarr[i],3)) for i in range(np.shape(ktarr)[0])]
        j_eta  = np.zeros(len(poly_ktarr),dtype = ([('n','f8'),('eta','f8'),\
                                                    ('pd','f8')]))
        jind = 0
        for eachpol in poly_ktarr:
            eqn = np.polysub(eachpol[1], cur)
            roots =np.roots(eqn)
            roots = roots[roots>0]
            selected_j = roots[roots<1.5]
            kq = self.kq(selected_j,eachpol[0],self.area_ratio,self.Z)
            delkq = self.Delta_kq(kq, selected_j, self.area_ratio,eachpol[0],\
                                      self.Z)
            kq = kq + delkq
            kt = np.polyval(eachpol[1], selected_j)
            eff = self.efficiency(kt, kq, selected_j)
            inpclass.addval({'pd':eachpol[0],'aea0':self.area_ratio,\
                             'j':selected_j,"efficiency":eff,\
                             'kq':kq,'kt':kt,'n':self.va/(selected_j*self.D)})
            j_eta[jind]= tuple([self.va/(selected_j*self.D),eff,eachpol[0]])
            jind +=1
        if plot:
            plot.addplot(j_eta,self.area_ratio)

def Optimum_n(bestdic,h,va,D,T,cavCheck):
    """
    bestdic.keys()
    ['bar', 'j', 'aea0', 'efficiency', 'kq', 'pd', 'kt', 'z','n']
    """
    n_eta= np.zeros(len(bestdic),dtype = ([('pd','f2'),('n','f2'),\
                                           ('eta','f2'),('bar','f2'),\
                                           ('z',"i2"),('cavitation','f2')]))

    i = 0
    for dic in bestdic:
        cno = cavitationNo(h, va, dic['n'], D)
        tto = toh(T,dic['pd'],va,dic['n'],D)
        sig=cavitationPercent(cno, tto)
        n_eta[i] =tuple([dic['pd'],dic['n'],dic['efficiency'],dic['bar'],dic['z'],sig])
#         print n_eta[i]
        i += 1

    bestindex=0
    index = 0
    besteff = 0

    for eff in n_eta['eta']:
        cno = cavitationNo(h, va, n_eta[index][1], D)
        tto = toh(T,n_eta[index][0],va,n_eta[index][1],D)
        if n_eta[index]['cavitation']<> 0:

            if eff > besteff:
                besteff =eff
                bestindex=index
        index += 1



    return n_eta[bestindex]


def OptimizePropeller(D,w,t,speed,r=0,z =3,pltcur=0):
    dicbar={2:np.array([0.3]),\
            3:np.array([0.3,0.5,0.65,0.8]),\
            4:np.array([0.4,0.55,0.7,0.85,1.0]),\
            5:np.array([0.45,0.6,0.75,]),\
            6:np.array([0.5,0.65,0.8]),\
            7:np.array([0.55,0.7,0.85])}

    bar = dicbar[z]

    bladeno = z
    bestvals = []

    for ratio in bar:

        curcalc = ktkq(ratio,bladeno,w,t,speed,Dia = D,r=r)
        curopt = optimum_j()
        curcalc.kt_j2(curopt,pltcur)
        cbest = curopt.best(.4)
        cbest['z'] =  bladeno
        cbest['bar']  = ratio

        bestvals.append(cbest)

    return bestvals
def cavitationNo(h,va,n,D):
    vr2 = (0.7*np.pi*n*D)**2+va**2
    patm = 101
    pv = 1.1
    rho = 1.025
    return (patm-pv+(rho * 9.81*h))/(0.5*rho*vr2)
def toh(T,pd,va,n,D):
    rho = 1.025
    vr2 = (0.7*np.pi*n*D)**2+va**2
    A0 = np.pi *(D**2 / 4)
    Ap =(1.067 -0.229*pd)*A0
    return (T/Ap)/(0.5*rho *vr2)
def cavitationPercent(Cno,toh):
    PO5 = lambda x :.11104 * np.log(x)+.27104
    PO10=lambda x : .1412   *np.log(x)+.3506
    PO20= lambda x : .1722* np.log(x)+.4494
    PO30= lambda x : .1882* np.log(x) +.4985

    if toh<PO5(Cno):
        return 5
    elif toh<PO10(Cno):
        return 10
    elif toh<PO20(Cno):
        return 20
    elif toh<PO30(Cno):
        return 30
    else:
        return 0
def wf_tf(v,disp):
    """
    return (wake fraction, thrust deduction factor)
    """
    fr = (0.165*v)/disp**(1/6)
    if fr>1.45:
        w = 0.056-(0.066*fr)
        t = 0.15 -(0.08*fr)
    else:
        w = (0.04*fr) - 0.1
        t = 0.02 * fr
    return (w,t)

if __name__ == "__main__":
#
#    vs = 20.2
#    Rs = 114.3 #kN
#    (w,t)= wf_tf(vs,150)
#    va = vs*(1-w)*.5144
#    T = Rs*0.5/(1-t)
#    h = 0.5
#    aea0 = 0.55
#    z = 4
#    # from plot_wageningen import plot_eta_n
#    import matplotlib.pyplot as plt
    clsktkq = ktkq(aea0,z,w,t,vs)
    (kq,dkq) = clsktkq.generate_kq_curves()
    (kt, dkt) = clsktkq.generate_kt_curves()

    fig =plt.figure()
    kt_j_plt = fig.add_subplot(111)
    kq_j_plt = kt_j_plt.twinx()
    kq_j_plt.set_ylim(0,0.2)
    kt_j_plt.set_ylim(0,1.2)
    for i in range(len(kq)):
        kq_j_plt.plot(clsktkq.j, kq[i] ,linestyle='--')
        kt_j_plt.plot(clsktkq.j, kt[i] ,linestyle = "-")
    plt.grid(1)

    
        
    
    
    for j in [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]:
        print "J:",j,"\t",
        print round(clsktkq.kq( j, 1, 0.55, 4),4)
        
        
    print round(clsktkq.kq( 0.2, 1, 0.55, 4),4)
        
    
    # for pbd in range(2,7):
    #     pl = plot_eta_n(plt,pbd)

    #     bestd =OptimizePropeller(1.2,.2, .18, 20,r=Rs*1000,z=pbd,pltcur = pl)
    #     plt.legend(loc=0,prop={'size':7})

    #     opt = Optimum_n(bestd,h=h,va=va,D=1.2,T=T,cavCheck=1)
    #     print opt
    # plt.show()




