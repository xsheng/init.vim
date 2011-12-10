__author__ = 'XSheng'
__doc__ = '''
This module is the interface of inverse laplace methods for computing ideal response of well testing.
'''
import numpy as np
import scipy as sci

class InverseLaplace():
    def __init__(self, LaplaceFunc):
        '''
        Initialize the methods
        '''
        self.F = LaplaceFunc

    def Stehfest(self, t):
        '''
        Stehfest method works for smooth function
        f(t) = ln(2)/t \sum_{i=1}^{N/2}V_i*F(u),
        where u = (i*ln(2))/t is the Laplace variable,
        and
        V_i = (-1)^(N/2 + i)*sum_int((i+1)/2)^min(i, N/2) K^(N/2 +1)*(2K)! /(N/2-K)!*(K!)^2*(i-K)!*(2K-i)!,
        in which N is even number, 8, 10, or 12, (or 16).

        @param t is time
        @param F is the laplace image function
        '''
        F = self.F
        N = 16
        ln2 = np.log(2)
        FactN = sci.factorial(np.array(range(0,N+1,1)))
        #print "Factorial(1...N) = ", FactN      #debug
        
        V = np.zeros_like(range(0, N/2 +1, 1))
        for i in range(1, N/2+1, 1):
            sign = np.power(-1,N/2+i)
            for K in range(np.int((i+1)/2), np.minimum(i, N/2)+1,1):
                V[i] = V[i] + np.power(K,N/2+1)*FactN[2*K]/\
                              (FactN[N/2-K]*FactN[K]*FactN[K]*FactN[i-K]*FactN[2*K-i])
            V[i] = sign*V[i]
        #print "V[1..N/2] = ", V     #debug

        f = 0
        for i in range(1, N/2+1, 1):
            u = i*ln2/t
            f = f + V[i] * F(u)
        f = ln2/t*f
        
        return f
def test():
    import matplotlib.pyplot as plt
    def tstF(u):
        return 1.0/u/u/u

    invLaplace = InverseLaplace(tstF)
    t = np.arange(0.1, 1.0, 0.1)

    ft = np.zeros_like(t)
    for i in np.arange(0,len(t),1):
        ft[i] = invLaplace.Stehfest(t[i])

    plt.plot(t,ft)
    plt.show()

if __name__ == "__main__":
    test()