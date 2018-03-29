import queue as Q
import copy
from Graph import Graph
import Kruskal
from Solution import Solution
import time
SOURCE = 0

OPTION = 4
##
# Détermine le type d'heuristique utilisé (voir rapport pour la dénomination :
# 0 -> sans heuristique
# 1 -> heuristique MST
# 2 -> heuristique closest
# 3 -> heuristique departage
# 4 -> heuristique source
##

class Node(object):
    def __init__(self, v, sol, heuristic_cost=0):
        self.v = v
        self.solution = sol
        self.heuristic_cost = heuristic_cost

    def explore_node(self, heap, *kruskal):
        if len(self.solution.not_visited)>1:
            for n in self.solution.not_visited:
                if n==SOURCE:
                    continue # il reste encore des sommets à visiter avant de retourner à la source

                s=Solution(self.solution)
                s.add_edge(self.v,n)
                node = Node(n,s)

                node.heuristic_cost = heuristic(kruskal,node)
                heap.put(node)

        else: # il ne reste plus que le noeud source : on l'ajoute avec une heuristique de 0: on a complété la boucle
            n=self.solution.not_visited[0]
            s=Solution(self.solution)
            s.add_edge(self.v,n)
            node = Node(n, s)
            node.heuristic_cost = 0
            heap.put(node)

    def __lt__(self,other):
        return isN2betterThanN1(other, self)


def main():
    g = Graph("N12.data")
    Kruskal.kruskal = Kruskal.Kruskal(g)
    heap = Q.PriorityQueue()
    nodes_created=1
    nodes_explored=1
    # On inclut le noeud d'initialisation dans le calcul des noeuds créés/explorés
    # Le compter ou non n'a pas beaucoup d'importance cependant.
    sol = Solution(g)
    n0 = Node(SOURCE, sol)
    begin = time.time()
    while len(n0.solution.not_visited)>0:
        nodes_created += max(1,len(n0.solution.not_visited)-1)
        # on crée 1 noeud si on arrive à source, et le nombre restant à visiter -1 si on n'arrive pas à la source (au minimum 1)
        n0.explore_node(heap, Kruskal.kruskal)
        n0 = heap.get()
        nodes_explored+=1
    end = time.time()
    n0.solution.toString()
    print("Nodes explored : " + str(nodes_explored))
    print("Nodes created : " + str(nodes_created))
    print("Time elapsed : " + str(end-begin) + " seconds")


# 1ere heuristique complémentaire
def closest_city(N):
    cost = float('inf')
    for nod in [n for n in N.solution.not_visited if n != N.v]:
        c = N.solution.g.costs[nod, N.v]
        if c<cost:
            cost=c
    return cost

# 2e heuristique complémentaire
def closest_from_source(N, source):
    cost = float('inf')
    for nod in [n for n in N.solution.not_visited if n != N.v]:
        c = N.solution.g.costs[nod, source]
        if c<cost:
            cost = c
    return cost


def heuristic_cost_MST(kruskal,N1):
    return Kruskal.kruskal.getMSTCost(N1.solution, SOURCE, 0)


def heuristic_cost_MST_and_closest_city(kruskal,N1):
    return Kruskal.kruskal.getMSTCost(N1.solution, SOURCE, 1)+closest_city(N1)


def heuristic_cost_MST_and_closest_source(kruskal,N):
    return Kruskal.kruskal.getMSTCost(N.solution, SOURCE, 2)+closest_from_source(N,SOURCE)

def heuristic(kruskal, N):
    if OPTION == 0:
        return 0
    elif OPTION == 1 or OPTION == 3:
        return heuristic_cost_MST(kruskal,N) # Notre première implémentation du MST
    elif OPTION == 2:
        return heuristic_cost_MST_and_closest_city(kruskal,N) # MST_closest
    elif OPTION == 4:
        return heuristic_cost_MST_and_closest_source(kruskal,N) # MST_source


def isN2betterThanN1(N1, N2):
    if OPTION != 3:
        return N1.solution.cost + N1.heuristic_cost > N2.solution.cost + N2.heuristic_cost
    else: # si on fait un départage
        if N1.solution.cost + N1.heuristic_cost > N2.solution.cost + N2.heuristic_cost:
            return True
        elif N1.solution.cost + N1.heuristic_cost == N2.solution.cost + N2.heuristic_cost:
            c1 = N1.solution.cost + N1.heuristic_cost+closest_city(N1)
            c2 = N2.solution.cost + N2.heuristic_cost+closest_city(N2)
            if c1 > c2:
                return True
            elif c1==c2:
                c1+=closest_from_source(N1,SOURCE)
                c2+=closest_from_source(N2,SOURCE)
                return c1>c2
            else:
                return False
        else:
            return False


if __name__ == '__main__':
    main()
