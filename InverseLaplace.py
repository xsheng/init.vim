__author__ = 'XSheng'
__doc__ = '''
This module is the interface of inverse laplace methods for computing ideal response of well testing.
'''
import numpy as np
import scipy as sci
from cmath import log
from numpy import pi, cos, sin, sqrt, exp, real
from numpy.fft import ifft

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

    def Iseger(self, Delta, k):
        """
        "Numerical Transform Inversion Using Gaussian Quadrature" developed by Peter Den Iseger
        """
        M = pow(2,k)
        M2 = 8*M
        a = 44/M2
        n = 16
        if n == 16:
            _lambda = [0.0,
                4.44089209850063e-016,
                6.28318530717958     ,
                12.5663706962589     ,
                18.8502914166954     ,
                25.2872172156717     ,
                34.296971663526      ,
                56.1725527716607     ,
                170.533131190126
            ]
            beta = [0.0,
                1,
                1.00000000000004,
                1.00000015116847,
                1.00081841700481,
                1.09580332705189,
                2.00687652338724,
                5.94277512934943,
                54.9537264520382
            ]
        if n == 32:
            _lambda = [0.0,
                0               ,
                6.28318530717958,
                12.5663706143592,
                18.8495559215388,
                25.1327412287184,
                31.4159265359035,
                37.6991118820067,
                43.9823334683971,
                50.2716029125234,
                56.7584358919044,
                64.7269529917882,
                76.7783110023797,
                96.7780294888711,
                133.997553190014,
                222.527562038705,
                669.650134867713
            ]
            beta = [0.0,
                1 ,
                1 ,
                1 ,
                1 ,
                1 ,
                1.00000000000895 ,
                1.00000004815464 ,
                1.00003440685547 ,
                1.00420404867308 ,
                1.09319461846681 ,
                1.51528642466058 ,
                2.4132076646714  ,
                4.16688127092229 ,
                8.3777001312961 ,
                23.6054680083019,
                213.824023377988
            ]

        if n == 48:
            _lambda = [0.0,
                0 		 ,
                6.28318530717957 ,
                12.5663706143592 ,
                18.8495559215388 ,
                25.1327412287183 ,
                31.4159265358979 ,
                37.6991118430775 ,
                43.9822971502571 ,
                50.2654824574367 ,
                56.5486677646182 ,
                62.8318530747628 ,
                69.1150398188909 ,
                75.3984537709689 ,
                81.6938697567735 ,
                88.1889420301504 ,
                95.7546784637379 ,
                105.767553649199 ,
                119.58751936774  ,
                139.158762677521 ,
                168.156165377339 ,
                214.521886792255 ,
                298.972429369901 ,
                497.542914576338 ,
                1494.71066227687
            ]
            beta = [0.0,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1.00000000000234,
                1.00000000319553,
                1.00000128757818,
                1.00016604436873,
                1.00682731991922,
                1.08409730759702,
                1.3631917322868 ,
                1.85773538601497,
                2.59022367414073,
                3.73141804564276,
                5.69232680539143,
                9.54600616545647,
                18.8912132110256,
                52.7884611477405,
                476.448331869636
            ]

        F = self.F
        f_hat_jk = np.zeros((n/2+1, M2+1))
        f_hat = np.zeros(M2+1)
        for k in range(0, M2+1, 1): # 0...M2
            for j in range(1, n/2+1, 1):    # 1...n/2
                f_hat_jk[j][k] = real(F(complex(a,_lambda[j]+2*pi*k/M2)/Delta))
            for j in range(1, n/2+1, 1):    # 1...n/2
                f_hat[k] += beta[j]*f_hat_jk[j][k]
            f_hat[k] *= 2.0/Delta
        for j in range(1, n/2+1, 1):    # 1...n/2
            f_hat[0] += beta[j]*(f_hat_jk[j][0] + f_hat_jk[j][M2])
        f_hat[0] *= 1.0/Delta

        #f = 1/M2*real(ifft(f_hat))
        f = np.zeros(M2)
        for l in range(0, M2):
            for k in range(0, M2):
                f[l] += f_hat[k]*cos(2*pi*l*k/M2)
            f[l] *= 1.0/M2

        for l in range(0, M):
            f[l] = exp(a*l)*f[l]
            
        return f[0:M]



    
def test():
    import matplotlib.pyplot as plt
    
    def tstF(u):
        return 1.0/(u*u+1)

    invLaplace = InverseLaplace(tstF)
    t = np.arange(0.01, np.pi*2, 0.01)
    sint = sin(t)
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
    
    """
    k = 7
    M = pow(2,k)
    tn = np.arange(0, M, 1)*10.0/M
    fn = invLaplace.Iseger(10.0/M, k)

    plt.plot(
        tn,fn,
        tn, sin(tn)
    )
    plt.show()
    """

if __name__ == "__main__":
    test()