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
    def __init__(self, max_len=100000, batch_size = 32, heap_init=None):
        self.max_len = max_len
        self.batch_size = batch_size

        if not heap_init:
            self.queue = []
        else:
            if len(heap_init) > self.max_len:
                sys.stderr.write('Error: Can\'t make heap larger than max len. Creating smaller heap\n')
                self.queue = []
                for i in range(self.max_len):
                    self.queue.append((-heap_init[i][0], heap_init[i][1]))
            else:
                self.queue = [(-i, j) for i, j in heap_init]
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
        return 1

    def get_priorities(self, e_ids= None):
        """
        returns all priorities, or priorities based on e_ids
        param priorities: list of e_ids to search for
        return list: priority values
        """
        if e_ids is None:
            return list(map(lambda x: -x[0], self.queue))[0:len(self.queue)]
        return [v for i, v in self.queue if -i in e_ids] #

    def get_experiences(self, priorities= None):
        """
        returns all e_ids, or e_ids based on priorities
        param priorities: list of priorities to search for
        return list: priority values
        """
        if priorities is None:
            return list(map(lambda x: x[1], self.queue))[0:len(self.queue)]
        return [v for i, v in self.queue if -i in priorities]

    def update(self, experience, new_priority):
        """
        update priority value based on experience
        param experience: experience id
        param new_priority: new priority value
        return bool: worked?
        """
        pos = [i for i, v in enumerate(self.queue) if v[1] == experience]
        if pos == []:
            return False
        del(self.queue[pos[0]])
        heappush(self.queue, (-new_priority, experience))
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
        heappush(self.queue, (-experience[0], experience[1]))
        return True

    def pop(self):
        """
        pop max priority and experience id
        return tuple: (priority & (experience))
        """
        if len(self.queue) == 0:
            sys.stderr.write('Error: no value in heap, pop failed\n')
            return False
        v = heappop(self.queue)
        return (-v[0], v[1])

    def pop_batch(self):
        """
        pop replay experience batch
        param batch_size: (total experiences to return)
        return list of tuples: [(experience),..]
        """
        if self.batch_size > len(self.queue):
            sys.stderr.write('Error: not enough values in batch, batch pop failed\n')
            return False
        batch = []
        for i in range(self.batch_size):
            v = heappop(self.queue)
            batch.append((-v[0], v[1]))
        return batch
