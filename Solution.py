import copy

from Graph import Graph


class Solution(object):
    def __init__(self, s):
        if isinstance(s, Graph):
            self.g = s
            self.cost = 0
            self.visited = []
            self.not_visited = list(range(s.get_N()))
        elif isinstance(s, Solution):
            self.g = s.g
            self.cost = s.cost
            self.visited = copy.deepcopy(s.visited)
            self.not_visited = copy.deepcopy(s.not_visited)
        else:
            raise ValueError('you should give a graph or a solution')

    def add_edge(self, v, u):
        self.not_visited.remove(u)
        self.visited.append(u)
        self.cost+=self.g.get_edge(v,u).cost


    def toString(self):
        if len(self.visited)>0:
            print(str(self.visited[-1]))
            for edge in self.visited:
                print(str(edge) + "\n")
            print("COST = " + str(self.cost))
        else:
            return