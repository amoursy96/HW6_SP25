#region imports
from scipy.optimize import fsolve
from Resistor import Resistor
from VoltageSource import VoltageSource
from Loop import Loop
#endregion

#region class definitions
class ResistorNetwork():
    #region constructor
    def __init__(self):
        """
        The resistor network consists of Loops, Resistors and Voltage Sources.
        This is the constructor for the network and it defines fields for Loops, Resistors and Voltage Sources.
        You can populate these lists manually or read them in from a file.
        """
        #region attributes
        self.Loops = []  # initialize an empty list of loop objects in the network
        self.Resistors = []  # initialize an empty a list of resistor objects in the network
        self.VSources = []  # initialize an empty a list of source objects in the network
        #endregion
    #endregion

    #region methods
    def BuildNetworkFromFile(self, filename):
        """
        This function reads the lines from a file and processes the file to populate the fields
        for Loops, Resistors and Voltage Sources
        :param filename: string for file to process
        :return: nothing
        """
        try:
            FileTxt = open(filename, "r").read().split('\n')  # reads from file and splits into lines
            print(f"Reading file: {filename}")  # Debug statement
            LineNum = 0
            # erase any previous
            self.Resistors = []
            self.VSources = []
            self.Loops = []
            while LineNum < len(FileTxt):
                lineTxt = FileTxt[LineNum].lower().strip()
                if len(lineTxt) < 1:
                    pass  # skip empty lines
                elif lineTxt[0] == '#':
                    pass  # skip comment lines
                elif "resistor" in lineTxt:
                    print(f"Found resistor at line {LineNum + 1}")  # Debug statement
                    LineNum = self.MakeResistor(LineNum, FileTxt)
                elif "source" in lineTxt:
                    print(f"Found source at line {LineNum + 1}")  # Debug statement
                    LineNum = self.MakeVSource(LineNum, FileTxt)
                elif "loop" in lineTxt:
                    print(f"Found loop at line {LineNum + 1}")  # Debug statement
                    LineNum = self.MakeLoop(LineNum, FileTxt)
                LineNum += 1
            print("Resistors in network:", [r.Name for r in self.Resistors])  # Debug statement
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")  # Debug statement

    def MakeResistor(self, N, Txt):
        """
        Make a resistor object from reading the text file
        :param N: (int) Line number for current processing
        :param Txt: [string] the lines of the text file
        :return: a resistor object
        """
        R = Resistor()  # instantiate a new resistor object
        N += 1  # <Resistor> was detected, so move to next line in Txt
        while N < len(Txt):  # Ensure we don't go out of bounds
            txt = Txt[N].lower().strip()  # retrieve line from Txt and make it lower case
            if "resistor" in txt:
                break  # Stop if we encounter the next resistor
            if "name" in txt:
                R.Name = txt.split('=')[1].strip()
            if "resistance" in txt:
                R.Resistance = float(txt.split('=')[1].strip())
            N += 1
        print(f"Added resistor: Name = {R.Name}, Resistance = {R.Resistance}")  # Debug statement
        self.Resistors.append(R)  # append the resistor object to the list of resistors
        return N

    def MakeVSource(self, N, Txt):
        """
        Make a voltage source object from reading the text file
        :param N: (int) Line number for current processing
        :param Txt: [string] the lines of the text file
        :return: a voltage source object
        """
        VS = VoltageSource()
        N += 1
        while N < len(Txt):  # Ensure we don't go out of bounds
            txt = Txt[N].lower().strip()
            if "source" in txt:
                break  # Stop if we encounter the next source
            if "name" in txt:
                VS.Name = txt.split('=')[1].strip()
            if "value" in txt:
                VS.Voltage = float(txt.split('=')[1].strip())
            if "type" in txt:
                VS.Type = txt.split('=')[1].strip()
            N += 1
        self.VSources.append(VS)
        return N

    def MakeLoop(self, N, Txt):
        """
        Make a Loop object from reading the text file
        :param N: (int) Line number for current processing
        :param Txt: [string] the lines of the text file
        :return: a resistor object
        """
        L = Loop()
        N += 1
        while N < len(Txt):  # Ensure we don't go out of bounds
            txt = Txt[N].lower().strip()
            if "loop" in txt:
                break  # Stop if we encounter the next loop
            if "name" in txt:
                L.Name = txt.split('=')[1].strip()
            if "nodes" in txt:
                txt = txt.replace(" ", "")
                L.Nodes = txt.split('=')[1].strip().split(',')
            N += 1
        self.Loops.append(L)
        return N

    def AnalyzeCircuit(self):
        """
        Use fsolve to find currents in the resistor network.
        :return:
        """
        # need to set the currents to that Kirchoff's laws are satisfied
        i0 = [1.0, 1.0, 1.0]  # define an initial guess for the currents in the circuit
        i = fsolve(self.GetKirchoffVals, i0)
        # print output to the screen
        print("I1 = {:0.1f}".format(i[0]))
        print("I2 = {:0.1f}".format(i[1]))
        print("I3 = {:0.1f}".format(i[2]))
        return i

    def GetKirchoffVals(self, i):
        """
        This function uses Kirchoff Voltage and Current laws to analyze this specific circuit
        KVL:  The net voltage drop for a closed loop in a circuit should be zero
        KCL:  The net current flow into a node in a circuit should be zero
        :param i: a list of currents relevant to the circuit
        :return: a list of loop voltage drops and node currents
        """
        # set current in resistors in the top loop.
        self.GetResistorByName('ad').Current = i[0]  # I_1 in diagram
        self.GetResistorByName('bc').Current = i[0]  # I_1 in diagram
        self.GetResistorByName('cd').Current = i[2]  # I_3 in diagram
        # set current in resistor in bottom loop.
        self.GetResistorByName('ce').Current = i[1]  # I_2 in diagram
        # calculate net current into node c
        Node_c_Current = sum([i[0], i[1], -i[2]])

        KVL = self.GetLoopVoltageDrops()  # two equations here
        KVL.append(Node_c_Current)  # one equation here
        return KVL

    def GetElementDeltaV(self, name):
        """
        Need to retrieve either a resistor or a voltage source by name.
        :param name:
        :return:
        """
        for r in self.Resistors:
            if name == r.Name:
                return -r.DeltaV()
            if name[::-1] == r.Name:
                return -r.DeltaV()
        for v in self.VSources:
            if name == v.Name:
                return v.Voltage
            if name[::-1] == v.Name:
                return -v.Voltage

    def GetLoopVoltageDrops(self):
        """
        This calculates the net voltage drop around a closed loop in a circuit based on the
        current flowing through resistors (cause a drop in voltage regardless of direction of traversal) or
        the value of the voltage source that have been set up as positive based on the direction of traversal.
        :return: net voltage drop for all loops in the network.
        """
        loopVoltages = []
        for L in self.Loops:
            # Traverse loops in order of nodes and add up voltage drops between nodes
            loopDeltaV = 0
            for n in range(len(L.Nodes)):
                if n == len(L.Nodes) - 1:
                    name = L.Nodes[0] + L.Nodes[n]
                else:
                    name = L.Nodes[n] + L.Nodes[n + 1]
                loopDeltaV += self.GetElementDeltaV(name)
            loopVoltages.append(loopDeltaV)
        return loopVoltages

    def GetResistorByName(self, name):
        """
        A way to retrieve a resistor object from self.Resistors based on resistor name
        :param name:
        :return:
        """
        for r in self.Resistors:
            if r.Name == name:
                return r
        print(f"Resistor '{name}' not found in the network.")  # Debug statement
        return None
    #endregion

class ResistorNetwork_2(ResistorNetwork):
    #region constructor
    def __init__(self):
        super().__init__()  # runs the constructor of the parent class
        #region attributes
        #endregion
    #endregion

    #region methods
    def AnalyzeCircuit(self):
        """
        Override AnalyzeCircuit for the second circuit.
        """
        i0 = [1.0, 1.0, 1.0]  # define an initial guess for the currents in the circuit
        i = fsolve(self.GetKirchoffVals, i0)
        # print output to the screen
        print("I1 = {:0.1f}".format(i[0]))
        print("I2 = {:0.1f}".format(i[1]))
        print("I3 = {:0.1f}".format(i[2]))
        return i

    def GetKirchoffVals(self, i):
        """
        Override GetKirchoffVals for the second circuit.
        """
        # set current in resistors in the top loop.
        self.GetResistorByName('ad').Current = i[0]  # I_1 in diagram
        self.GetResistorByName('bc').Current = i[0]  # I_1 in diagram
        self.GetResistorByName('cd').Current = i[2]  # I_3 in diagram
        # set current in resistor in bottom loop.
        self.GetResistorByName('ce').Current = i[1]  # I_2 in diagram
        # calculate net current into node c
        Node_c_Current = sum([i[0], i[1], -i[2]])

        KVL = self.GetLoopVoltageDrops()  # two equations here
        KVL.append(Node_c_Current)  # one equation here
        return KVL
    #endregion
#endregion