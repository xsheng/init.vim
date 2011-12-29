__author__ = 'XSheng'
__doc__ = '''
This module is the interface of inverse laplace methods for computing ideal response of well testing.
'''
import numpy as np
import scipy as sci
from cmath import log
from numpy import pi, cos, sin, sqrt, exp, real

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

    def DeHoog(self, t):
        MAX_LAPORDER = 60   #
        DeHoogFactor = 4.0  # DeHoog time factor
        M = 40  #should be smaller than MAX_LAPORDER
        tolerance = 1e-8

        Fctrl = np.zeros(2*MAX_LAPORDER+1)*complex(0,0)
        e = np.zeros((2*MAX_LAPORDER,MAX_LAPORDER))*complex(0,0)
        q = np.zeros((2*MAX_LAPORDER,MAX_LAPORDER))*complex(0,0)
        d = np.zeros(2*MAX_LAPORDER+1)*complex(0,0)
        A = np.zeros(2*MAX_LAPORDER+2)*complex(0,0)
        B = np.zeros(2*MAX_LAPORDER+2)*complex(0,0)

        T = DeHoogFactor*t
        gamma = -0.5*log(tolerance)/T

        Fctrl[0] = 0.5*self.F(gamma)
        for i in range(1, 2*M + 1, 1):
            s = complex(gamma,i*pi/T)
            Fctrl[i] = self.F(s)

        for i in range(0, 2*M, 1):
            e[i][0] = 0.0
            q[i][1] = Fctrl[i+1]/Fctrl[i]
        e[2*M][0] = 0.0

        for r in range(1, M, 1): # 1...M-1
            for i in range(2*(M-r), -1, -1): # 2*(M-r)...0
                if i< 2*(M-r) and r > 1:
                    q[i][r] = q[i+1][r-1]*e[i+1][r-1]/e[i][r-1]
                e[i][r] = q[i+1][r] - q[i][r] + e[i+1][r-1]

        d[0] = Fctrl[0]
        for m in range(1, M+1, 1):  # 1...M
            d[2*m-1] = -q[0][m]
            d[2*m] = -e[0][m]

        z = complex(cos(pi*t/T), sin(pi*t/T))

        A[0] = 0.0
        B[0] = 1.0
        A[1] = d[0]
        B[1] = 1.0
        for n in range(2, 2*M+1 +1, 1): # 2...2*M+1
            dz = d[n-1]*z
            A[n] = A[n-1]+dz*A[n-2]
            B[n] = B[n-1]+dz*B[n-2]

        h2M = 0.5*(1.0+z*(d[2*M-1] - d[2*M]))
        R2M = -h2M*(1.0 - sqrt(1.0 + (z*d[2*M]/h2M/h2M)))

        A[2*M+1] = A[2*M] + R2M*A[2*M - 1]
        B[2*M+1] = B[2*M] + R2M*B[2*M - 1]

        return 1.0/T*exp(gamma*t)*real(A[2*M+1]/B[2*M+1])
    
def test():
    import matplotlib.pyplot as plt
    
    def tstF(u):
        return 1.0/(u*u+1)

    invLaplace = InverseLaplace(tstF)
    t = np.arange(0.01, np.pi, 0.01)
    sint = np.sin(t)
    ft = invLaplace.Stehfest(t)

    ft_dehoog  = np.zeros_like(t)
    for i in range(0, len(t), 1):
        ft_dehoog[i] = invLaplace.DeHoog(t[i])

    plt.plot(t,ft,
             t, sint,
             t, np.abs(ft - sint),
             t, ft_dehoog,
             t, np.abs(ft_dehoog - sint)
    )
    plt.show()

if __name__ == "__main__":
    test()