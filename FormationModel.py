__author__ = 'XSheng'
__doc__ = '''
This module is the interface of formation model.
'''
import numpy as np
import scipy.special as spf

class FormationModel():

    def __init__(self, name ):
        self.ModelName = name

    def SphericalLaplace(self,u, R_D, C_D, S):
        '''
        u is the laplace variable
        R_D is the dimensionless reservoir radius
        C_D is the dimensionless storage factor
        S is skin factor
        '''
        sqrt_u = np.sqrt(u)
        sqrt_uRd = sqrt_u*R_D
        
        fu = sqrt_u*(spf.kn(1,sqrt_u)*spf.iv(0,sqrt_uRd) + spf.kn(0,sqrt_uRd)*spf.iv(1,sqrt_u)) /\
             (spf.kn(1,sqrt_u)*spf.iv(0,sqrt_uRd) - spf.kn(0,sqrt_uRd)*spf.iv(0,sqrt_u))
        pwd = 1/u*(1+S*fu)/(fu+C_D*u*(1+S*fu))
        return pwd