# region class definitions
class Loop():
    # region constructor
    def __init__(self, Name='A', Pipes=None):
        '''
        Defines a loop in a pipe network. Note: the pipes must be listed in order. The traversal of a pipe loop
        will begin at the start node of Pipe[0] and move in the positive direction of that pipe. Hence, loops
        can be either CW or CCW traversed, depending on which pipe you start with. Should work fine either way.
        :param Name: name of the loop
        :param Pipes: a list/array of pipes in this loop
        '''
        # region attributes
        self.name = Name
        self.pipes = Pipes if Pipes is not None else []  # Avoid mutable default argument
        # endregion
    # endregion

    # region methods
    def getLoopHeadLoss(self):
        '''
        Calculates the net head loss as I traverse around the loop, in m of fluid.
        :return: the net head loss around the loop
        '''
        deltaP = 0  # initialize to zero
        if not self.pipes:
            return deltaP  # return 0 if no pipes are in the loop

        startNode = self.pipes[0].startNode  # begin at the start node of the first pipe
        for p in self.pipes:
            # calculates the head loss in the pipe considering loop traversal and flow directions
            phl = p.getFlowHeadLoss(startNode)
            deltaP += phl
            # move to the next node
            startNode = p.endNode if startNode != p.endNode else p.startNode
        return deltaP
    # endregion
# endregion