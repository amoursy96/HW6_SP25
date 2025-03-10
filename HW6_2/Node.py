# region class definitions
class Node():
    # region constructor
    def __init__(self, Name='a', Pipes=None, ExtFlow=0):
        '''
        A node in a pipe network.
        :param Name: name of the node
        :param Pipes: a list/array of pipes connected to this node
        :param ExtFlow: any external flow into (+) or out (-) of this node in L/s
        '''
        # region attributes
        self.name = Name
        self.pipes = Pipes if Pipes is not None else []  # Avoid mutable default argument
        self.extFlow = ExtFlow
        # endregion
    # endregion

    # region methods
    def getNetFlowRate(self):
        '''
        Calculates the net flow rate into this node in L/s
        :return: the net flow rate into this node
        '''
        Qtot = self.extFlow  # Start with the external flow
        for p in self.pipes:
            # Retrieves the pipe flow rate (+) if into node (-) if out of node. See class for pipe.
            Qtot += p.getFlowIntoNode(self.name)
        return Qtot
    # endregion
# endregion