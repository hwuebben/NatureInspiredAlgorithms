import os
import numpy as np

class TSP_Problem:

    def __init__(self, problem: int = 1):
        """

        :param problem: integer, specifying the problem, valid inputs are 1,2 and 3
        :return:
        """
        if problem == 1:
            self.filename = '01.tsp'
        elif problem == 2:
            self.filename = '02.tsp'
        elif problem == 3:
            self.filename = '03.tsp'
        else:
            raise ValueError('Unknown benchmark problem, valid inputs are 1,2 or 3')
        self.distance_matrix = self.load_data()

    def load_data(self) -> np.array:
        """
        parse .tsp file into the distance matrix.
        :return:
        """
        with open('.'+os.sep+'ressources'+os.sep+self.filename,'r') as fp:
            distance_matrix = []
            for line in fp:
                row = self._parse_line(line)
                distance_matrix.append(row)
            return np.asarray(distance_matrix)

    def _parse_line(self, line: str) -> list:
        """
        parse a single line of the .tsp-file into a list of integers.
        :param line:
        :return:
        """
        row = line.split(' ')
        for i in range(len(row)-1):
            row[i] = int(row[i])
        return row

    def get_distance_matrix(self) -> np.array:
        return self.distance_matrix


