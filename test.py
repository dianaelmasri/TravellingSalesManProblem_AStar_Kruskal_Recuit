import queue as Q


def __lt__(self,other):
    return len(self)<len(other)


heap = Q.PriorityQueue()
heap.put('jeej')
heap.put('kek')
heap.put('topkek')
heap.put('non')
print(sorted(heap.queue)[0])

# a = [1,5,6,8,9,10,0]
# for i in a :
#     print (i)