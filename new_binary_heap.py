#!/usr/bin/env python
# author: Calum (AverageHomosapien)
# description: Binary heap class used in the priority experience replay
#   adapted from original custom written binary heap class

import sys
import math
import utility
import heapq
from heapq import heappush, heappop, heappushpop, heapify


class BinaryHeap(object):

    """
    param max_len: integer of the max heap length (max priority queue length)
    param priority_init: list of priority tuples
    param replace: experiences automatically replaced
    """
    def __init__(self, max_len=100000, priority_init=None, replace=True,
                batch_size = 64):
        self.replace = replace
        self.max_len = max_len
        self.batch_size = batch_size

        if priority_init is None:
            self.queue = [] # priority tuples, stored (priority, item)
            self.size = 0 # current size
        else:
            self.queue = heapify(priority_init)
        self.size = len(self.queue)

    def __repr__(self):
        print(self.queue)

    def check_full(self):
        return len(self.queue) > self.max_size

    def _insert(self, experience):
        """
        insert new experience id with priority
        param experience: experience tuple
        return: bool
        """
        self.size += 1

        if self.check_full():
            if self.replace:
                heappushpop(self.queue, experience)
            else:
                sys.stderr.write('Error: no space left to add experience id %d with priority value %f\n' % (e_id, priority))
                return False
        else:
            heappush(self.queue, (experience))
        return True

    def update(self, priority, e_id):
        """
        update priority value according its experience id
        param priority: new priority value
        param e_id: experience id
        return: bool
        """
        if e_id in self.e2p:
            p_id = self.e2p[e_id]
            self.priority_queue[p_id] = (priority, e_id)
            self.p2e[p_id] = e_id

            self.down_heap(p_id)
            self.up_heap(p_id)
            return True
        else:
            # this e id is new, do insert
            return self._insert(priority, e_id)

    def get_max_priority(self):
        """
        get max priority, if no experience, return 1
        :return: max priority if size > 0 else 1
        """
        if self.size > 0:
            return self.priority_queue[1][0]
        else:
            return 1

    def pop(self):
        """
        pop out the max priority value with its experience id
        :return: priority value & experience id
        """
        if self.size == 0:
            sys.stderr.write('Error: no value in heap, pop failed\n')
            return False, False

        pop_priority, pop_e_id = self.priority_queue[1]
        self.e2p[pop_e_id] = -1
        # replace first
        last_priority, last_e_id = self.priority_queue[self.size]
        self.priority_queue[1] = (last_priority, last_e_id)
        self.size -= 1
        self.e2p[last_e_id] = 1
        self.p2e[1] = last_e_id

        self.down_heap(1)

        return pop_priority, pop_e_id

    def get_priority(self):
        """
        get all priority value
        :return: list of priority
        """
        return list(map(lambda x: x[0], self.priority_queue.values()))[0:self.size]

    def get_e_id(self):
        """
        get all experience id in priority queue
        :return: list of experience ids order by their priority
        """
        return list(map(lambda x: x[1], self.priority_queue.values()))[0:self.size]

    def priority_to_experience(self, priority_ids):
        """
        retrieve experience ids by priority ids
        :param priority_ids: list of priority id
        :return: list of experience id
        """
        return [self.p2e[i] for i in priority_ids]
