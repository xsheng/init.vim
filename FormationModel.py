__author__ = 'XSheng'
__doc__ = '''
This module is the interface of formation model.
'''
import numpy as np
from scipy.special import iv,kn # bessel functions
from numpy import sqrt, real
from cmath import tanh, cosh, sinh

def coth(x):
    return cosh(x)/sinh(x)

I1 = lambda x: iv(1, real(x))
I0 = lambda x: iv(0, real(x))
K1 = lambda x: kn(1, real(x))
K0 = lambda x: kn(0, real(x))


class FormationModel():

    def __init__(self, name, BC ):
        """
        Name = Model Name
        BC = "ConstantPressure" or "Closed"
        """
        self.ModelName = name # Model Name
        self.BC = BC # Model Boundary Condition, fixed pressure

    def SphericalLaplace(self,u, R_D, C_D, S):
        """
        laplace solution of ideal one-layer spherical reservoir model with constant pressure boundary
        u is the laplace variable
        R_D is the dimensionless reservoir radius
        C_D is the dimensionless storage factor
        S is skin factor
        """
        sqrt_u = np.sqrt(u)
        sqrt_uRd = sqrt_u*R_D
        if self.BC == "ConstantPressure":
            fu = sqrt_u*(K1(sqrt_u)*I0(sqrt_uRd) + K0(sqrt_uRd)*I1(sqrt_u)) /\
                 (K1(sqrt_u)*I0(sqrt_uRd) - K0(sqrt_uRd)*I0(sqrt_u))
        elif self.BC == "Closed":
            fu = sqrt_u*(K1(sqrt_u)*I0(sqrt_uRd) - K0(sqrt_uRd)*I1(sqrt_u)) /\
                 (K1(sqrt_u)*I0(sqrt_uRd) + K0(sqrt_uRd)*I0(sqrt_u))
        pwd = 1/u*(1+S*fu)/(fu+C_D*u*(1+S*fu))
        return pwd

    def InfiniteSize(self, u, C_D, S):
        """
        u is the laplace variable
        C_D is the dimensionless storage factor
        S is skin factor
        """
        sqrt_u = np.sqrt(u)
        pwd = 1/u*(K0(sqrt_u) + S*sqrt_u*K1(sqrt_u))/\
              (sqrt_u*K1(sqrt_u) + C_D*u*
                                   (K0(sqrt_u)+S*sqrt_u*K1(sqrt_u)))
        return pwd

    def InfiniteSizeLineSource(self, u, C_D, S):
        """
        Simplified line source solution
        u is the laplace variable
        C_D is the dimensionless storage factor
        S is skin factor
        """
        sqrt_u = sqrt(u)
        pwd = 1/u*(K0(sqrt_u) + S)/(1+C_D*u*(K0(sqrt_u)+S))
        return pwd

    def func_f_steady(self, _omega, _lambda, u):
        return (_omega*(1-_omega)*u + _lambda)/((1-_omega)*u + _lambda)

    def func_f_plate(self, _omega, _lambda, u):
        return _omega + sqrt(_lambda*(1-_omega)/3/u)*tanh(sqrt(3*(1-_omega)*u/_lambda))

    def func_f_spherical(self, _omega, _lambda, u):
        tmp = 15*(1-_omega)*u/_lambda
        return _omega + 1.0/5*_lambda/u*(sqrt(tmp)*coth(sqrt(tmp)) -1)

    def func_f_cylinder(self, _omega, _lambda, u):
        """
        f(u) = \omega +2*\sqrt((1-\omega)*\lambda/(15u)) * I_1(\sqrt((1-\omega)*\lambda/(15u)))/I_0(\sqrt((1-\omega)*\lambda/(15u)))
        """
        tmp = (1-_omega)*_lambda/15/u
        return _omega + 2*sqrt(tmp)*I1(tmp)/I0(tmp)

    def InfiniteSizeDualPoro(self, f,  u, c_D, S):
        return self.InfiniteSize(f(u)*u, c_D, S)



def test():
    from InverseLaplace import InverseLaplace
    import matplotlib.pyplot as plt
    RadialFormation = FormationModel("Infinite Radial", "ConstantPressure")

    # infinite reservoir line source solution
    F = lambda u: RadialFormation.InfiniteSizeLineSource(u, 1.0, 1.0)
    invLap = InverseLaplace(F)
    t = np.arange(0.01, 10*np.pi, 0.1)
    ft = invLap.Stehfest(t)

    # infinite reservoir spherical solution
    Fcp = lambda u:RadialFormation.SphericalLaplace(u, 10.0, 1.0, 1.0)
    invLapcp = InverseLaplace(Fcp)
    ftcp = invLapcp.Stehfest(t)

    # infinite reservoir 
    Fls = lambda u:RadialFormation.InfiniteSize(u, 1.0, 1.0)
    invLapls = InverseLaplace(Fls)
    ftls = invLapls.Stehfest(t)

    # infinite dual porosity reservoir
    _omega = 0.5
    _lambda = 0.1   # lambda value has a great impact on latter period pressure response
    f = lambda u: RadialFormation.func_f_cylinder(_omega, _lambda, u)
    Fdp = lambda u: RadialFormation.InfiniteSizeDualPoro(f, u, 1.0, 1.0 )
    invLapDp = InverseLaplace(Fdp)
    ftdp = invLapDp.Stehfest(t)
    ft_dehoog  = np.zeros_like(t)
    for i in range(0, len(t), 1):
        ft_dehoog[i] = invLapDp.DeHoog(t[i])

    plt.plot(#t, ft,
             #t, ftcp,
             #t, ftls,
             t, ftdp,
             t, ft_dehoog
    )
    plt.show()
    
if __name__=="__main__":
    test()