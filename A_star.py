import queue as Q
import copy
from Graph import Graph
import Kruskal
from Solution import Solution
import time

SOURCE = 0

class Node(object):
    def __init__(self, v, sol, heuristic_cost=0):
        self.v = v
        self.solution = copy.deepcopy(sol)
        self.heuristic_cost = heuristic_cost

    def explore_node(self, heap, *kruskal):
        if len(self.solution.not_visited)>1:
            for n in self.solution.not_visited:
                if n==SOURCE:
                    continue

                s=Solution(self.solution)
                s.add_edge(self.v,n)
                node = Node(n,s)
                node.heuristic_cost = kruskal[0].getMSTCost(s,SOURCE) # si heuristique MST, sinon commenter
                heap.put(node)

        else:
            n=self.solution.not_visited[0]
            s=Solution(self.solution)
            s.add_edge(self.v,n)
            node = Node(n, s)
            node.heuristic_cost = 0
            heap.put(node)

    def __lt__(self,other):
        return isN2betterThanN1(other, self)


def main():
    g = Graph("N10.data")
    Kruskal.kruskal = Kruskal.Kruskal(g)
    heap = Q.PriorityQueue()
    o=0
    sol = Solution(g)
    n0 = Node(SOURCE, sol)
    while len(n0.solution.not_visited)>0:
        n0.explore_node(heap, Kruskal.kruskal)
        n0 = heap.get()
        o+=1


        #heap = Q.PriorityQueue()

    n0.solution.toString()
    print("Nodes explored : " + str(o))
    print(time.process_time())


def heuristic_cost_MST(kruskal,N1):
    return kruskal.getMSTCost(N1.solution, SOURCE)

def isN2betterThanN1(N1, N2):
    return N1.solution.cost + N1.heuristic_cost > N2.solution.cost + N2.heuristic_cost


if __name__ == '__main__':
    main()
