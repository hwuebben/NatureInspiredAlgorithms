
import numpy as np
from numpy import random
from copy import deepcopy


def get_naive_direct_neighborhood(state):
    """
    All Vectors with distance 1 in binary space are considered neighbors (basically I just flip one random bit)
    :param state:
    :return:
    """
    neighbors = []
    for i in range(len(state)):
        neighbor = deepcopy(state)
        neighbor[i] = not neighbor[i]
        neighbors.append(neighbor)
    return neighbors

def get_distance_2_neighborhood(state):
    """
    All Vectors with distance 2 in binary space are considered neighbors (This time two random bitflips instead of one)
    :param state:
    :return:
    """
    neighbors = []
    for i in range(len(state)):
        for j in range(i+1):
            
            # create all states
            neighbor = deepcopy(state)
            neighbor[i] = not neighbor[i]
            neighbor[j] = not neighbor[j]
            neighbors.append(neighbor)
    return neighbors

class HillClimber:

    def __init__(self,neigborhood_func, weight_list, value_list, weight_limit,init_mode='random',first_choice=False):
        """

        :param neigborhood_func: pointer to the neighborhood-function
        :param weight_list: list of weights
        :param value_list:  list of values, has to match the weight list in shape
        :param weight_limit: the weight limit, can be int or float
        :param init_mode:   "random" or "empty", empty state is a zero vector, random vector is a uniform-random-binary vector
        :param first_choice: select between normal hill climbing and first choice hill climbing
        :return:
        """


        self.get_neighbors = neigborhood_func

        self.weight_list = weight_list
        self.value_list = value_list
        self.weight_limit = weight_limit
        self.first_choice = False
        if init_mode == 'random':
            feasable = False

            # make sure we start at a valid state
            while(not feasable):
                self.state = self.get_random_state()
                feasable = self._check_feasable(self.state)
        elif init_mode == 'empty':
            self.state = self.get_empty_imput_state()

    def _check_feasable(self, selected_ids):
        """
        Check if validity of a state
        :param selected_ids:
        :return:
        """
        return np.sum(np.asarray(self.weight_list)[selected_ids]) < self.weight_limit

    def _get_value(self,selected_ids):
        """
        Calculate value of a state
        :param selected_ids:
        :return:
        """
        return np.sum(np.asarray(self.value_list)[selected_ids])

    def get_empty_imput_state(self):
        """
        Return a zero-state
        :return:
        """
        return [False]*len(self.weight_list)

    def get_random_state(self):
        """
        Return a random state,which may or may not be a valid state
        :return:
        """
        random_state = []
        for i in range(len(self.weight_list)):
            val = np.random.randint(0,2)
            random_state.append(val == 1)
        return random_state

    def _search_step(self):
        """
        Advance a single node (if possible) and update thate current state of the search
        :return:
        """
        neighbors = self.get_neighbors(self.state)
        best = None
        for neighbor in neighbors:

            # check of neighbour is feasable
            weight = np.sum(np.asarray(self.weight_list)[neighbor])
            if not self._check_feasable(neighbor):
                continue
            # check if a feasable solution is better than the current state
            elif self._get_value(neighbor) > self._get_value(self.state):
                best = neighbor

                # end checking for results, when in first choice mode
                if self.first_choice:
                    break

        # return current state if done, else return best neighbor
        if best == None:
            return False
        else:
            self.state = best
            return True

    def search(self):
        """
        conduct the search
        :return:
        """
        while(self._search_step()):
            print(self._get_value(self.state), self.state)
        print('Result found, with value:',self._get_value(self.state))

climber = HillClimber(get_distance_2_neighborhood,[1,2,3,4,5,6,7,8,10],[1,2,3,4,5,6,7,8,10],100,'random',True)
climber.search()
