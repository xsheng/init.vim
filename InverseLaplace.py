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
        ln2 = np.log(2)
        G = sci.factorial(np.array(range(0,N+1,1)))
        #print "Factorial(1...N) = ", G      #debug
        
        V = np.zeros_like(range(0, N +1, 1))
        for i in range(1, N+1, 1):
            sign = np.power(-1,N/2+i)
            nK = np.minimum(i, N/2)
            for K in range((i+1)/2, nK+1,1):
                V[i] = V[i] + np.power(K,N/2+1)*G[2*K]/\
                              (G[N/2-K]*G[K]*G[K]*G[i-K]*G[2*K-i])
            V[i] = sign*V[i]
        print "V[1..N] = ", V     #debug

        f = np.zeros_like(t)
        for j in range(0, len(t), 1):
            for i in range(1, N+1, 1):
                u = i*ln2/t[j]
                f[j] = f[j] + V[i] * F(u)
            f[j] = ln2/t[j]*f[j]
        
        return f

    def Stehfest1(self, t, n, c):
        if n%2 == 1:
            n += 1

        y = np.zeros_like(t)
        m = len(t)
        p = self.F

        g = np.array(range(0,n+1,1))
        h = np.array(range(0,n/2+1,1))

        g[0] = 1
        nh = n/2

        for i in range(1,n+1,1):
            g[i] = g[i-1]*i
        print g

        h[1] = 2.0/g[nh-1]
        for i in range(2, nh+1,1):
            h[i] = pow(i,nh)*g[2*i]/(g[nh-i]*g[i]*g[i-1])

        sn = 2*np.sign(nh-nh/2*2) - 1
        v = np.zeros_like(range(0,n+1,1))
        for i in range(1, n+1, 1):
            v[i] = 0
            og = np.minimum(i, nh)
            for k in range((i+1)/2, og+1, 1):
                v[i] = v[i] + h[k]/(g[i-k]*g[2*k-1])
            v[i] = sn* v[i]
            sn = -sn

        print "V = ", v
        for j in range(0, m, 1):
            tt = t[j]
            sfa = 0
            if not tt:
                tt = 1.0e-8
            a = np.log(2)/tt

            for i in range(1, n+1, 1):
                sfa = sfa + v[i]*p(c+i*a)

            sfa = np.exp(c*tt)*sfa*a
            y[j] = sfa
        return y

    def GaussLegendre(self, t, n, c):
        """
        
        """
        pass

    
def test():
    import matplotlib.pyplot as plt
    
    def tstF(u):
        return 1.0/(u*u)

    invLaplace = InverseLaplace(tstF)
    t = np.arange(0.1, 10.0, 0.1)
    ft = invLaplace.Stehfest(t)
    ft1 = invLaplace.Stehfest1(t, 10, 0)

    plt.plot(t,ft, t, ft1)
    plt.show()

if __name__ == "__main__":
    test()