#region classes
class Resistor():
    #region constructor
    def __init__(self, R=1.0, i=0.0, name='ab'):
        """
        Defines a resistor to have a self.Resistance, self.Current, and self.Name
        :param R: resistance in Ohm (float)
        :param i: current in amps (float)
        :param name: name of resistor by alphabetically ordered pair of node names
        """
        #region attributes
        self.Resistance = R  # Set the resistance of the resistor
        self.Current = i     # Set the current through the resistor
        self.Name = name     # Set the name of the resistor
        self.V = self.DeltaV()  # Calculate the voltage drop across the resistor
        #endregion
    #endregion

    #region methods
    def DeltaV(self):
        """
        Calculates voltage change across resistor.
        :return:  voltage drop across resistor as a float
        """
        self.V = self.Current * self.Resistance  # Calculate voltage drop using Ohm's Law
        return self.V
    #endregion
#endregion