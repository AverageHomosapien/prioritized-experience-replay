import heapq

def heap_test():
    h = []
    heapq.heappush(h, (5, 3))
    heapq.heappush(h, (4, 5))
    heapq.heappush(h, (3, 1))
    heapq.heappush(h, (1, 13))
    #my_heap = heapq.heapify([[1,1], [2,1]])
    #my_heap.
    print(h)
    print(heapq.nsmallest(2, h))



if __name__ == "__main__":
    heap_test()
