__author__ = 'XSheng'
__doc__ = '''
This module is the interface of formation model.
'''
import numpy as np
from scipy.special import iv,kn # bessel functions

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
            fu = sqrt_u*(kn(1,sqrt_u)*iv(0,sqrt_uRd) + kn(0,sqrt_uRd)*iv(1,sqrt_u)) /\
                 (kn(1,sqrt_u)*iv(0,sqrt_uRd) - kn(0,sqrt_uRd)*iv(0,sqrt_u))
        elif self.BC == "Closed":
            fu = sqrt_u*(kn(1,sqrt_u)*iv(0,sqrt_uRd) - kn(0,sqrt_uRd)*iv(1,sqrt_u)) /\
                 (kn(1,sqrt_u)*iv(0,sqrt_uRd) + kn(0,sqrt_uRd)*iv(0,sqrt_u))
        pwd = 1/u*(1+S*fu)/(fu+C_D*u*(1+S*fu))
        return pwd

    def InfiniteSize(self, u, C_D, S):
        """
        u is the laplace variable
        C_D is the dimensionless storage factor
        S is skin factor
        """
        sqrt_u = np.sqrt(u)
        pwd = 1/u*(kn(0,sqrt_u) + S*sqrt_u*kn(1,sqrt_u))/\
              (sqrt_u*kn(1, sqrt_u) + C_D*u*\
                                      (kn(0,sqrt_u)+S*sqrt_u*kn(1,sqrt_u)))
        return pwd

    def InfiniteSizeLineSource(self, u, C_D, S):
        """
        Simplified line source solution
        u is the laplace variable
        C_D is the dimensionless storage factor
        S is skin factor
        """
        sqrt_u = np.sqrt(u)
        pwd = 1/u*(kn(0, sqrt_u) + S)/(1+C_D*u*(kn(0,sqrt_u)+S))
        return pwd

def test():
    from InverseLaplace import InverseLaplace
    import matplotlib.pyplot as plt
    RadialFormation = FormationModel("Infinite Radial", "ConstantPressure")

    # infinite reservoir line source solution
    F = lambda u: RadialFormation.InfiniteSizeLineSource(u, 1.0, 1.0)
    invLap = InverseLaplace(F)
    t = np.arange(0.01, np.pi, 0.01)
    ft = invLap.Stehfest(t)

    # infinite reservoir spherical solution
    Fcp = lambda u:RadialFormation.SphericalLaplace(u, 10.0, 1.0, 1.0)
    invLapcp = InverseLaplace(Fcp)
    ftcp = invLapcp.Stehfest(t)

    # infinite reservoir 
    Fls = lambda u:RadialFormation.InfiniteSize(u, 1.0, 1.0)
    invLapls = InverseLaplace(Fls)
    ftls = invLapls.Stehfest(t)

    plt.plot(t,ft, \
             t, ftcp, \
             t, ftls
    )
    plt.show()
    
if __name__=="__main__":
    test()