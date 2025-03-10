#region class definitions
class Fluid:
    #region constructor
    def __init__(self, mu=0.00089, rho=1000):
        '''
        Default properties are for water.
        :param mu: dynamic viscosity in Pa*s -> (kg*m/s^2)*(s/m^2) -> kg/(m*s)
        :param rho: density in kg/m^3
        '''
        #region attributes
        self.mu = mu  # dynamic viscosity
        self.rho = rho  # density
        self.nu = self.mu / self.rho  # kinematic viscosity (m^2/s)
        #endregion
    #endregion