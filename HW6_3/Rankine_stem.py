from Steam import steam

class rankine():
    def __init__(self, p_low=8, p_high=8000, t_high=None, name='Rankine Cycle'):
        '''
        Constructor for rankine power cycle. If t_high is not specified, the State 1
        is assigned x=1 (saturated steam @ p_high). Otherwise, use t_high to find State 1.
        :param p_low: the low pressure isobar for the cycle in kPa
        :param p_high: the high pressure isobar for the cycle in kPa
        :param t_high: optional temperature for State1 (turbine inlet) in degrees C
        :param name: a convenient name
        '''
        self.p_low = p_low
        self.p_high = p_high
        self.t_high = t_high
        self.name = name
        self.efficiency = None
        self.turbine_work = 0
        self.pump_work = 0
        self.heat_added = 0
        self.state1 = None
        self.state2 = None
        self.state3 = None
        self.state4 = None

    def calc_efficiency(self):
        # Calculate the 4 states
        # State 1: turbine inlet (p_high, t_high) superheated or saturated vapor
        if self.t_high is None:
            self.state1 = steam(self.p_high, x=1, name='Turbine Inlet')  # Saturated vapor
        else:
            self.state1 = steam(self.p_high, T=self.t_high, name='Turbine Inlet')  # Superheated steam

        # State 2: turbine exit (p_low, s=s_turbine inlet) two-phase
        self.state2 = steam(self.p_low, s=self.state1.s, name='Turbine Exit')

        # State 3: pump inlet (p_low, x=0) saturated liquid
        self.state3 = steam(self.p_low, x=0, name='Pump Inlet')

        # State 4: pump exit (p_high, s=s_pump_inlet) typically sub-cooled, but estimate as saturated liquid
        self.state4 = steam(self.p_high, s=self.state3.s, name='Pump Exit')
        self.state4.h = self.state3.h + self.state3.v * (self.p_high - self.p_low)

        # Calculate turbine work, pump work, and heat added
        self.turbine_work = self.state1.h - self.state2.h
        self.pump_work = self.state4.h - self.state3.h
        self.heat_added = self.state1.h - self.state4.h

        # Calculate cycle efficiency
        self.efficiency = 100.0 * (self.turbine_work - self.pump_work) / self.heat_added
        return self.efficiency

    def print_summary(self):
        if self.efficiency is None:
            self.calc_efficiency()
        print('Cycle Summary for: ', self.name)
        print('\tEfficiency: {:0.3f}%'.format(self.efficiency))
        print('\tTurbine Work: {:0.3f} kJ/kg'.format(self.turbine_work))
        print('\tPump Work: {:0.3f} kJ/kg'.format(self.pump_work))
        print('\tHeat Added: {:0.3f} kJ/kg'.format(self.heat_added))
        self.state1.print()
        self.state2.print()
        self.state3.print()
        self.state4.print()

def main():
    # Instantiate a rankine object to test it.
    rankine1 = rankine(p_low=8, p_high=8000, t_high=500, name='Rankine Cycle with Superheated Steam')
    eff = rankine1.calc_efficiency()
    print(eff)
    rankine1.print_summary()

if __name__ == "__main__":
    main()