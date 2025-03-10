# steam.py
import numpy as np
from scipy.interpolate import griddata

class steam:
    """
    The steam class is used to find thermodynamic properties of steam along an isobar.
    The Gibbs phase rule tells us we need two independent properties to determine
    all other thermodynamic properties. Hence, the constructor requires pressure
    and one other property.
    """
    def __init__(self, pressure, T=None, x=None, v=None, h=None, s=None, name=None):
        '''
        Constructor for steam.
        :param pressure: pressure in kPa
        :param T: Temperature in degrees C
        :param x: quality of steam (x=1 is saturated vapor, x=0 is saturated liquid)
        :param v: specific volume in m^3/kg
        :param h: specific enthalpy in kJ/kg
        :param s: specific entropy in kJ/(kg*K)
        :param name: a convenient identifier
        '''
        self.p = pressure  # pressure in kPa
        self.T = T  # temperature in degrees C
        self.x = x  # quality
        self.v = v  # specific volume in m^3/kg
        self.h = h  # specific enthalpy in kJ/kg
        self.s = s  # specific entropy in kJ/(kg*K)
        self.name = name  # a useful identifier
        self.region = None  # 'superheated', 'saturated', or 'two-phase'
        if T is None and x is None and v is None and h is None and s is None:
            return
        else:
            self.calc()

    def calc(self):
        '''
        Calculate thermodynamic properties based on the given pressure and one other property.
        '''
        # Load thermodynamic data from files
        ts, ps, hfs, hgs, sfs, sgs, vfs, vgs = np.loadtxt('sat_water_table.txt', unpack=True, skiprows=1)
        tcol, hcol, scol, pcol = np.loadtxt('superheated_water_table.txt', unpack=True, skiprows=1)

        R = 8.314 / (18 / 1000)  # ideal gas constant for water [J/(mol K)]/[kg/mol]
        Pbar = self.p / 100  # pressure in bar (1 bar = 100 kPa)

        # Get saturated properties
        Tsat = float(griddata(ps, ts, Pbar))
        hf = float(griddata(ps, hfs, Pbar))
        hg = float(griddata(ps, hgs, Pbar))
        sf = float(griddata(ps, sfs, Pbar))
        sg = float(griddata(ps, sgs, Pbar))
        vf = float(griddata(ps, vfs, Pbar))
        vg = float(griddata(ps, vgs, Pbar))

        self.hf = hf  # saturated liquid enthalpy

        # Determine which second property is given
        if self.T is not None:
            if self.T > Tsat:  # superheated
                self.region = 'Superheated'
                self.h = float(griddata((tcol, pcol), hcol, (self.T, Pbar)))
                self.s = float(griddata((tcol, pcol), scol, (self.T, Pbar)))
                self.x = 1.0
                TK = self.T + 273.14  # temperature in Kelvin
                self.v = R * TK / (self.p * 1000)  # ideal gas approximation
        elif self.x is not None:  # saturated
            self.region = 'Saturated'
            self.T = Tsat
            self.h = hf + self.x * (hg - hf)
            self.s = sf + self.x * (sg - sf)
            self.v = vf + self.x * (vg - vf)
        elif self.h is not None:
            self.x = (self.h - hf) / (hg - hf)
            if self.x <= 1.0:  # saturated
                self.region = 'Saturated'
                self.T = Tsat
                self.s = sf + self.x * (sg - sf)
                self.v = vf + self.x * (vg - vf)
            else:  # superheated
                self.region = 'Superheated'
                self.T = float(griddata((hcol, pcol), tcol, (self.h, Pbar)))
                self.s = float(griddata((hcol, pcol), scol, (self.h, Pbar)))
        elif self.s is not None:
            self.x = (self.s - sf) / (sg - sf)
            if self.x <= 1.0:  # saturated
                self.region = 'Saturated'
                self.T = Tsat
                self.h = hf + self.x * (hg - hf)
                self.v = vf + self.x * (vg - vf)
            else:  # superheated
                self.region = 'Superheated'
                self.T = float(griddata((scol, pcol), tcol, (self.s, Pbar)))
                self.h = float(griddata((scol, pcol), hcol, (self.s, Pbar)))
    def print(self):
        """
        Print a nicely formatted report of the steam properties.
        """
        print('Name: ', self.name)
        if self.x < 0.0:
            print('Region: compressed liquid')
        else:
            print('Region: ', self.region)
        print('p = {:0.2f} kPa'.format(self.p))
        if self.x >= 0.0:
            print('T = {:0.1f} degrees C'.format(self.T))
        print('h = {:0.2f} kJ/kg'.format(self.h))
        if self.x >= 0.0:
            print('s = {:0.4f} kJ/(kg K)'.format(self.s))
            if self.region == 'Saturated':
                print('v = {:0.6f} m^3/kg'.format(self.v))
                print('x = {:0.4f}'.format(self.x))
        print()