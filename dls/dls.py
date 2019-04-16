import numpy as np

from lmfit import Model
from scipy.constants import k, pi

# $g_1 = e^{-\Gamma t}$

# $g_2=B(1+\beta|g_1|^2)$

# $\Gamma = -Dq^2$

# $q =\frac{4\pi n}{\lambda} sin\left(\frac{\theta}{2}\right) $

# $D = \frac{kT}{6\pi\mu R_h}$

class DLS:

    """Load DLS models for fitting autocorrelation functions using the cumulant method

       A great explanation for this fitting procedure was written by Barbara Frisken

           20 August 2001 􏰥 Vol. 40, No. 24 􏰥 APPLIED OPTICS

           
        
       Arguments:
           mu_2 -- Bool
               fit second cumulant term, mu_2, to estimate polydispersity of sample
           mu_3 -- Bool
               fit third cumulant term, mu_3, to estimate skew on polydispersity

    """

    def __init__(self, mu_2=True, mu_3=False, **qkwargs):

        #self._q = self.q(**qkwargs)
        # use only simple exp function
        if not mu_2:
            self.g = Model(g)

        # fit mu_2 and mu_3
        elif mu_3:
            self.g = Model(cumulant3)

        # fit only mu_2 
        else:
            self.g = Model(cumulant2)

        self.pars = self.g.make_params(D=1e-10, B=1.0, beta=0.5, mu_2=1.0e5, mu_3=1.0)


def q(n=1.3347, lam=824e-9, theta=150.0):
    """ Calculate q (scattering vector)
    
        Arguments:
        
        n -- refractive index (1.3347 for 1% salt solution)
        lam -- wavelength of light in meters
        theta -- angle of detector
        
        Returns:
        q
        
    """
    theta = theta * (pi / 180)
    _q = (4.0 * pi * n) / lam * np.sin(theta / 2.0)
    return _q


def g(t, D, B, beta):
    return B + beta * np.exp(-2. * D * q() ** 2 * t)


def cumulant2(t, D, B, beta, mu_2):
    return B + beta * np.exp(-2. * D * q() ** 2 * t) * (1 + mu_2/2. * t**2.) ** 2.


def cumulant3(self, t, D, B, beta, mu_2, mu_3):
    return B + beta * np.exp(-2. * D * q() ** 2 * t) * (1 + mu_2/2. * t**2. - mu_3/6. * t**3. ) ** 2.


def stokes_einstein(D, viscosity, T):
    R_h = (k * T) / (6.0 * pi * viscosity * D)
    return R_h


def viscosity(T):
    """ Temperature dependence of water from Wikipedia 
        
        https://en.wikipedia.org/wiki/Temperature_dependence_of_liquid_viscosity
        
        T is in K and viscosity is in Ns/m^2
        
    """
    return 2.414e-5 * 10 ** (247.8 / (T - 140.0))
