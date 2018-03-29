from Graph import Graph
import random as rd
import numpy.matlib as m
import time


def calculate_cost(sol,g):
    res = 0
    for i in range (len(sol)-1):
        res += g.costs[sol[i],sol[i+1]]
    return res


def compare_solution(sol1,sol2,g):
    return calculate_cost(sol1,g) - calculate_cost(sol2,g)


def change_solution(sol,g,temp):
    sol2 = exchange(sol)
    delta = compare_solution(sol2,sol,g)
    if delta<0:
        return sol2
    else:
        a = rd.random()
        if a < m.exp(-delta/temp):
            return sol2 #probabilité non-nulle d'adopter la solution même si celle-ci est moins bonne
        else:
            return sol


def exchange(sol):
    sol2 = sol.copy()
    possible = list(range(1,len(sol)-2))
    i = rd.choice(possible)
    possible.remove(i)
    j = rd.choice(possible)
    sol2[i],sol2[j]=sol2[j],sol2[i]
    return sol2


def main():
    N = 17
    g = Graph("N17.data")
    co = 0
    e = 0
    for k in range(10):
        s = [i for i in range(1,N)]
        rd.shuffle(s)
        sol = [0]+s+[0] #on fixe le sommet source à 0
        T0 = 1000
        begin = time.time()
        while T0 > 5:
            for i in range(N**2):
                sol = change_solution(sol,g,T0)
            T0*=0.98
        end = time.time()-begin
        print(sol)
        co+=calculate_cost(sol,g)
        e+= end
    print(co/10) #on moyenne sur 10 exemplaires
    print(e/10)


if __name__ == '__main__':
    main()