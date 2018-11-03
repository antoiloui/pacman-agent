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
        self.depth = 5
    
    def manhattan_distance(self,xy1, xy2):
        """Returns the Manhattan distance between points.
        Arguments:
        ----------
        - `xy1`: the first point.
        - `xy2`: the second point.

        Returns:
        ----------
        The Manhattan distance between points xy1 and xy2.
        """
        return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

    def score_evaluation(self, state):
        """Returns the score of the state.
        Arguments:
        ----------
        - `state`: the current game state.

        Returns:
        ----------
        The score of the given state.
        """
        return state.getScore()

    def custom_evaluation(self, state):
        """Returns a custum utility value of the state.
        Arguments:
        ----------
        - `state`: the current game state.

        Returns:
        ----------
        The custom utility value at a given state.
        """
        score = 0
        ghost_dist = 0
        closest_food = math.inf
        closest_ghost = math.inf
        nb_foods_left = math.inf

        food_list = state.getFood().asList()
        pacman_pos = state.getPacmanPosition()
        ghost_list = state.getGhostPositions()
        current_score = state.getScore()

        # If pacman wins the game
        if state.isWin():
            return math.inf
        # If pacman loses the game
        if state.isLose():
            return - math.inf

        # Get the distance from pacman to the closest food
        food_dist = [self.manhattan_distance(pacman_pos, food_pos) for food_pos in food_list]
        closest_food = min(food_dist)

        # Get the distances from pacman to the closest ghost
        ghost_dist = [self.manhattan_distance(pacman_pos, ghost_pos) for ghost_pos in ghost_list]
        closest_ghost = min(ghost_dist)
        
        # Get the number of foods left
        nb_foods_left = len(food_list)

        # Compute score
        score = 1 * current_score + \
                2 * max(closest_ghost, 4) + \
                -1.5 * closest_food + \
                -4  * nb_foods_left

        return score


    def alphabeta_decision(self, state, depth, nb_ghosts):
        """Returns the best legal action according to the minimax algorithm.
        Arguments:
        ----------
        - `state`: the current game state.
        - `depth`: the biggest autorized depth before evaluation.
        - `nb_ghosts`: the number of ghosts in the grid.

        Returns:
        ----------
        The best legal action for the defined maximal depth.
        """
        values = list()
        actions = list()
        alpha = - math.inf
        beta = math.inf

        pac_successors = state.generatePacmanSuccessors()
        for next_state, next_action in pac_successors:
            value = self.min_value(next_state, alpha, beta, depth, nb_ghosts)
            if value >= beta:
                return next_action

            alpha = max(alpha, value)
            values.append(value)
            actions.append(next_action)

        index = values.index(max(values))

        return actions[index]
    
    def max_value(self, state, alpha, beta, depth, ghost_index):
        """
        Arguments:
        ----------
        - `state`: the current game state.
        - `depth`: the biggest autorized depth before evaluation.
        - `ghost_index`: the index of the ghost agent.

        Returns:
        ----------
        The max utility value of the successor nodes.
        """
        # Check the terminal test
        if state.isWin() or state.isLose() or depth == 0:
            return self.custom_evaluation(state)  # Returns the utility value
        
        # Initialize value
        value = - math.inf

        pac_successors = state.generatePacmanSuccessors()
        for pac_successor in pac_successors:
            value = max(value, self.min_value(pac_successor[0], alpha, beta, depth-1, ghost_index))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        
        return value

    def min_value(self, state, alpha, beta, depth, ghost_index):
        """
        Arguments:
        ----------
        - `state`: the current game state.
        - `depth`: the biggest autorized depth before evaluation.
        - `ghost_index`: the index of the ghost agent.

        Returns:
        ----------
        The min utility value of the successor nodes.
        """
        # Check the terminal test
        if state.isWin() or state.isLose() or depth == 0:
            return self.custom_evaluation(state)  # Returns the utility value
        
        # Initialize value
        value = math.inf

        ghost_successors = state.generateGhostSuccessors(ghost_index)
        for ghost_successor in ghost_successors:
            if ghost_index > 1:
                value = min(value, self.min_value(ghost_successor[0], alpha, beta, depth, ghost_index-1))
            else:
                value = min(value, self.max_value(ghost_successor[0], alpha, beta, depth-1, self.nb_ghosts))
            if value <= alpha:
                return value
            beta = min(beta, value)

        return value

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.
        Arguments:
        ----------
        - `state`: the current game state. 

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """
        # Get the number of ghosts in the layout
        self.nb_ghosts = state.getNumAgents() - 1

        # Compute next move
        next_move = self.alphabeta_decision(state, self.depth, self.nb_ghosts)
        return next_move
