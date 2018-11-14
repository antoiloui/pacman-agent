from pacman_module.game import Agent
from pacman_module.pacman import Directions
import math



class PacmanAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        self.nb_ghosts = 0
        self.visited = set()

    def get_info(self, state):
        """Returns information about a state to uniquely identify it.
        Arguments:
        ----------
        - `state`: the current game state.

        Returns:
        ----------
        Tuple of 
            -the hash value of Pacmans position, 
            -the hash value of the food matrix 
            -the tuple of ghost positions
        """
        pos = state.getPacmanPosition()
        food = state.getFood()
        ghost_pos = state.getGhostPositions()        

        return tuple([hash(pos), hash(food), tuple(ghost_pos)])
    
    def max_value(self, state, alpha, beta, ghost_index):
        """
        Arguments:
        ----------
        - `state`: the current game state.
        - `alpha`: the value of the best (i.e., highest-value) choice we have
        found so far at any choice point along the path for MAX.
        - `beta`: the value of the best (i.e., lowest-value) choice we have
        found so far at any choice point along the path for MIN.
        - `ghost_index`: the index of the ghost agent.

        Returns:
        ----------
        The max utility value of the successor nodes.
        """
        # Check the terminal test
        if state.isWin():
            return state.getScore()
        if state.isLose():
            return - math.inf
        
        # Initialize value
        value = - math.inf

        # Add the current node to the visited set
        self.visited.add(self.get_info(state))

        successors = state.generatePacmanSuccessors()
        for succ in successors:
            # Check if it was already visited
            if self.get_info(succ[0]) in self.visited:
                continue

            value = max(value, self.min_value(succ[0], alpha, beta, ghost_index))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        
        # Case in which all successors were visited
        if value == - math.inf:
            value = math.inf
        
        return value

    def min_value(self, state, alpha, beta, ghost_index):
        """
        Arguments:
        ----------
        - `state`: the current game state.
        - `alpha`: the value of the best (i.e., highest-value) choice we have
        found so far at any choice point along the path for MAX.
        - `beta`: the value of the best (i.e., lowest-value) choice we have
        found so far at any choice point along the path for MIN.
        - `ghost_index`: the index of the ghost agent.

        Returns:
        ----------
        The min utility value of the successor nodes.
        """
        # Check the terminal test
        if state.isWin():
            return state.getScore()
        if state.isLose():
            return - math.inf
        
        # Initialize value
        value = math.inf

        # Add the current node to the visited set
        self.visited.add(self.get_info(state))

        successors = state.generateGhostSuccessors(ghost_index)
        for succ in successors:
            if ghost_index > 1:
                value = min(value, self.min_value(succ[0], alpha, beta, ghost_index-1))
            else:
                value = min(value, self.max_value(succ[0], alpha, beta, self.nb_ghosts))
                
            if value <= alpha:
                return value
            beta = min(beta, value)
        
        # Case in which all successors were visited
        if value == math.inf:
            value = - math.inf

        return value

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move according to the
        Alphabeta algorithm.
        Arguments:
        ----------
        - `state`: the current game state. 

        Return:
        -------
        - The best legal move as defined in `game.Directions`, according to
        the Alphabeta algorithm.
        """
        self.visited = set()
        values = list()
        actions = list()
        alpha = - math.inf
        beta = math.inf

        # Get the number of ghosts in the layout
        self.nb_ghosts = state.getNumAgents() - 1

        # Add the current node to the visited set
        self.visited.add(self.get_info(state))

        # For each successor of the current node  
        pac_successors = state.generatePacmanSuccessors()
        for next_state, next_action in pac_successors:
            value = self.min_value(next_state, alpha, beta, self.nb_ghosts)
            if value >= beta:
                return next_action
            alpha = max(alpha, value)

            values.append(value)
            actions.append(next_action)

        index = values.index(max(values))

        return actions[index]
