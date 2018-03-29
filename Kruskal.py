import numpy as np
import copy
kruskal = None


class UnionFind(object):
    def __init__(self, n):
        self.n = n
        self.parent = np.array(range(n))
        self.rnk = np.zeros(n)

    def reset(self):
        self.parent = np.array(range(self.n))
        self.rnk = np.zeros(self.n)

    def add(self, e):
        x = self.find(e.source)
        y = self.find(e.destination)
        if self.rnk[x] > self.rnk[y]:
            self.parent[y] = x
        else:
            self.parent[x] = y
        if self.rnk[x] == self.rnk[y]:
            self.rnk[y] += 1

    def makes_cycle(self, e):
        return self.find(e.source) == self.find(e.destination)

    def find(self, u):
        if u != self.parent[u]:
            return self.find(self.parent[u])
        else:
            return u


class Kruskal(object):
    def __init__(self, g):
        self.uf = UnionFind(g.N)
        self.g = g

    def getMSTCost(self, sol, source, opt):
        cost = 0
        edge_list = self.g.edges

        if opt == 1: #MST closest : on exclut le noeud courant de l'arbre
            edge_selection = [e for e in edge_list if not (e.source in sol.visited or e.destination in sol.visited)]

        elif opt == 2:
            a = sol.visited[:-1] + [source] #MST source : on exclut la source de l'arbre
            edge_selection = [e for e in edge_list if not (e.source in a or e.destination in a)]

        else: # le MST "normal" : on prend tous les noeuds non-visités, dont la source, et le noeud courant
            edge_selection = [e for e in edge_list if not (e.source in sol.visited[:-1] or e.destination in sol.visited[:-1])]


        A = self.uf
        edge_selection.sort(key=lambda x: x.cost)
        for e in edge_selection:
            if not A.makes_cycle(e):
                A.add(e)
                cost += e.cost
        A.reset()
        return cost
