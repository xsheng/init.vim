__author__ = 'XSheng'
__doc__ = '''
This module is the interface of inverse laplace methods for computing ideal response of well testing.
'''
import numpy as np
import scipy as sci

class InverseLaplace():
    def __init__(self, LaplaceFunc):
        """
        Initialize the methods
        """
        self.F = LaplaceFunc

    def Stehfest(self, t):
        """
        Stehfest method works for smooth function
        f(t) = ln(2)/t \sum_{i=1}^{N}V_i*F(u),
        where u = (i*ln(2))/t is the Laplace variable,
        and
        V_i = (-1)^(N/2 + i)*sum_int((i+1)/2)^min(i, N/2) K^(N/2 +1)*(2K)! /(N/2-K)!*K!*(K-1)!*(i-K)!*(2K-i)!,
        in which N is even number, 8, 10, or 12, (or 16).

        @param t is time
        @param F is the laplace image function
        """
        F = self.F
        N = 10
        N2 = N/2
        ln2 = np.log(2)
        G = sci.factorial(np.array(range(0,N+1,1))) # factorial 0!...N!
        
        V = np.zeros_like(range(0, N +1, 1))
        sign = 1
        if N2 % 2:
            sign = -1
        for i in range(1, N+1, 1):
            kmin = (i+1)/2
            kmax = np.minimum(i, N2)
            sign = -sign
            for K in range(kmin, kmax+1, 1):
                V[i] += np.power(K,N2)*G[2*K]/\
                              (G[N/2-K]*G[K]*G[K-1]*G[i-K]*G[2*K-i])
            V[i] = sign*V[i]
        #print "V[1..N] = ", V     #debug

        f = np.zeros_like(t)
        for j in range(0, len(t), 1):
            ln2t = ln2/t[j]
            u = 0
            for i in range(1, N+1, 1):
                u += ln2t # u = i*ln2/t
                f[j] += V[i] * F(u)
            f[j] = ln2t*f[j]
        
        return f

    def GaussLegendre(self, t, n, c):
        """
        
        """
        pass

    
def test():
    import matplotlib.pyplot as plt
    
    def tstF(u):
        return 1.0/(u*u+1)

    invLaplace = InverseLaplace(tstF)
    t = np.arange(0.01, np.pi/2.0, 0.01)
    sint = np.sin(t)
    ft = invLaplace.Stehfest(t)

    plt.plot(t,ft,
             t, sint,
             t, np.abs(ft - sint)
    )
    plt.show()

if __name__ == "__main__":
    test()