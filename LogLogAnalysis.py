__author__ = 'XSheng'
from FormationModel import FormationModel as FM
import numpy as np

def Derivative(t, ft):
    """
    forward differentiation
    """
    deri = np.zeros_like(t)
    for i in range(1, len(t)):
        deri[i] = (ft[i] - ft[i-1])/(t[i] - t[i-1])
    deri[0] = deri[1]

    return deri

def test():
    from InverseLaplace import InverseLaplace
    import matplotlib.pyplot as plt
    RadialFormation = FM("Infinite Radial", "ConstantPressure")

    t = np.power(10,np.arange(-1,7,0.1))

    # infinite reservoir
    Fls = lambda u:RadialFormation.InfiniteSize(u, 1.0, 10.0)
    invLapls = InverseLaplace(Fls)
    ftls = invLapls.Stehfest(t)
    ftls_dehoog = np.vectorize(invLapls.DeHoog)(t)

    # infinite dual porosity reservoir
    _omega = 0.21
    _lambda = 0.15   # lambda value has a great impact on latter period pressure response
    f = lambda u: RadialFormation.func_f_spherical(_omega, _lambda, u)
    Fdp = lambda u: RadialFormation.InfiniteSizeDualPoro(f, u, 1.0, 10.0 )
    invLapDp = InverseLaplace(Fdp)
    ftdp = invLapDp.Stehfest(t)
    DeHoog = np.vectorize(invLapDp.DeHoog)
    ft_dehoog = DeHoog(t)

    plt.loglog(
             #t, ftls,
             #t, t*Derivative(t, ftls),
             t, ftls_dehoog,
             t, t*Derivative(t, ftls_dehoog),
             #t, ftdp,
             #t, t*Derivative(t, ftdp),
             t, ft_dehoog,
             t, t*Derivative(t, ft_dehoog)
    )
    plt.show()

if __name__=="__main__":
    test()