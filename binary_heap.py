#!/usr/bin/env python
# author: Calum (AverageHomosapien)
# description: Binary heap class used in the priority experience replay
#       adapted from custom written binary heap class

import sys
import math
import heapq
from heapq import heappush, heappop, heapify

"""
Binary heap class used in the priority experience implementation.
Priorities are stored in form [(-priority, experience-id), (-priority, experience-id),..] in tuples.
Negative priorities are stored since heapq is a min-binary heap implementation
"""

class BinaryHeap(object):
    """
    param max_len: integer of the max heap length (max priority queue length)
    param priority_init: list of priority tuples
    param replace: experiences automatically replaced
    """
    def __init__(self, max_len=100000, batch_size = 64, initial_heap=None):
        self.max_len = max_len
        self.batch_size = batch_size

        if not initial_heap:
            self.queue = []
        else:
            if len(initial_heap) > self.max_len:
                sys.stderr.write('Error: Can\'t make heap larger than max len. Creating smaller heap\n')
                self.queue = []
                for i in range(self.max_len):
                    self.queue.append((-initial_heap[i][0], initial_heap[i][1]))
            else:
                self.queue = [(-i, j) for i, j in initial_heap]
            heapify(self.queue)

    def __repr__(self):
        return "{}".format(self.queue)

    def is_full(self):
        return len(self.queue) >= self.max_len

    def get_size(self):
        return len(self.queue)

    def get_max_priority(self):
    # get max priority (1 if no experiences)
        if len(self.queue) > 0:
            return -self.queue[0][0]
        else:
            return 1

    def get_priorities(self):
    # get all priority values
        return list(map(lambda x: -x[0], self.queue))[0:len(self.queue)]

    def get_e_ids(self):
    # get all experience ids
        return list(map(lambda x: x[1], self.queue))[0:len(self.queue)]

    def update(self, e_id, new_priority):
        """
        update priority value based on e_id
        param e_id: experience id
        param new_priority: new priority value
        return bool: worked?
        """
        pos = [i for i, v in enumerate(self.queue) if v[1] == e_id]
        if pos == []:
            return False
        del(self.queue[pos[0]])
        heappush(self.queue, (-new_priority, e_id))
        heapify(self.queue)
        return True

    def push(self, experience):
        """
        push new experience
        param experience: experience tuple
        return bool: worked?
        """
        if self.is_full():
            sys.stderr.write('Error: no space to add experience {} with priority {}\n'.format(experience[1], -experience[0]))
            return False
        print("{} is the experience".format(experience))
        heappush(self.queue, (-experience[0], experience[1]))
        return True

    def pop(self):
        """
        pop max priority and experience id
        return tuple: (priority & e_id)
        """
        if len(self.queue) == 0:
            sys.stderr.write('Error: no value in heap, pop failed\n')
            return False
        v = heappop(self.queue)
        return (-v[0], v[1])

    def pop_batch(self, batch_size):
        """
        pop replay experience batch
        param batch_size: (total experiences to return)
        return list of tuples: [(experience),..]
        """
        if batch_size > len(self.queue):
            sys.stderr.write('Error: not enough values in batch, batch pop failed\n')
            return False
        batch = []
        for i in range(batch_size):
            v = heappop(self.queue)
            batch.append((-v[0], v[1]))
        return batch
