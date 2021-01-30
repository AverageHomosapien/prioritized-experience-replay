#!/usr/bin/python
# -*- encoding=utf-8 -*-
# author: Ian
# e-mail: stmayue@gmail.com
# description:

import sys
import math
import random
import numpy as np
import binary_heap


class Experience(object):

    def __init__(self, max_size=100000, alpha=0.7, beta_zero=0.5, batch_size=32,
                learn_start=1000, total_steps = 100000, partition_num = 100):
        self.max_size = max_size
        self.alpha = alpha
        self.beta_zero = beta_zero
        self.batch_size = batch_size
        self.learn_start = learn_start
        self.total_steps = total_steps
        self.partition_num = partition_num

        self.index = 0
        self.record_size = 0
        self.isFull = False
        self.exp_queue = {}

        self.queue = binary_heap.BinaryHeap(max_len = self.max_size,
                                            batch_size = self.batch_size)
        self.distributions = self.build_distributions()
        self.beta_grad = (1 - self.beta_zero) / float(self.total_steps - self.learn_start)


    def build_distributions(self):
        """
        preprocess pow of rank
        (rank i) ^ (-alpha) / sum ((rank i) ^ (-alpha))
        :return: distributions, dict
        """
        res = {}
        n_partitions = self.partition_num
        partition_num = 1
        # each part size
        partition_size = int(math.floor(self.max_size / n_partitions))

        for n in range(partition_size, self.max_size + 1, partition_size):
            if self.learn_start <= n <= self.max_size:
                distribution = {}
                # P(i) = (rank i) ^ (-alpha) / sum ((rank i) ^ (-alpha))
                pdf = list(
                    map(lambda x: math.pow(x, -self.alpha), range(1, n + 1))
                )
                pdf_sum = math.fsum(pdf)
                distribution['pdf'] = list(map(lambda x: x / pdf_sum, pdf))
                # split to k segment, and than uniform sample in each k
                # set k = batch_size, each segment has total probability is 1 / batch_size
                # strata_ends keep each segment start pos and end pos
                cdf = np.cumsum(distribution['pdf'])
                strata_ends = {1: 0, self.batch_size + 1: n}
                step = 1 / float(self.batch_size)
                index = 1
                for s in range(2, self.batch_size + 1):
                    while cdf[index] < step:
                        index += 1
                    strata_ends[s] = index
                    step += 1 / float(self.batch_size)

                distribution['strata_ends'] = strata_ends

                res[partition_num] = distribution

            partition_num += 1

        return res

    def store(self, experience):
        """
        store experience in the tuple - form (s1, a, r, s2, t)
        :param experience: tuple
        :return: bool - inserted
        """
        if self.queue.is_full():
            sys.stderr.write('Insert failed\n')
            return False
        self.queue.push(experience)
        return True

    def retrieve(self, indices):
        """
        get experience from indices
        :param indices: list of experience id
        :return: experience replay sample
        """
        return [self._experience[v] for v in indices]

    def update_priority(self, indices, delta):
        """
        update priority according indices and deltas
        :param indices: list of experience id
        :param delta: list of delta, order correspond to indices
        :return: None
        """
        for i in range(0, len(indices)):
            self.queue.update(math.fabs(delta[i]), indices[i])

    def sample(self, global_step):
        """
        sample a mini batch from experience replay
        :param global_step: now training step
        :return: experience, list, samples
        :return: w, list, weights
        :return: rank_e_id, list, samples id, used for update priority
        """
        if self.record_size < self.learn_start:
            sys.stderr.write('Record size less than learn start! Sample failed\n')
            return False, False, False

        dist_index = math.floor(self.record_size / self.max_size * self.partition_num)
        # issue 1 by @camigord
        partition_size = math.floor(self.max_size / self.partition_num)
        partition_max = dist_index * partition_size
        distribution = self.distributions[dist_index]
        rank_list = []
        # sample from k segments
        for n in range(1, self.batch_size + 1):
            index = random.randint(distribution['strata_ends'][n] + 1,
                                   distribution['strata_ends'][n + 1])
            rank_list.append(index)

        # beta, increase by global_step, max 1
        beta = min(self.beta_zero + (global_step - self.learn_start - 1) * self.beta_grad, 1)
        # find all alpha pow, notice that pdf is a list, start from 0
        alpha_pow = [distribution['pdf'][v - 1] for v in rank_list]
        # w = (N * P(i)) ^ (-beta) / max w
        w = np.power(np.array(alpha_pow) * partition_max, -beta)
        w_max = max(w)
        w = np.divide(w, w_max)
        # rank list is priority id
        # convert to experience id
        rank_e_id = self.queue.priority_to_experience(rank_list)
        # get experience id according rank_e_id
        experience = self.retrieve(rank_e_id)
        return experience, w, rank_e_id
