#!/usr/bin/env python
# original author: Ian
# original e-mail: stmayue@gmail.com
#___________________________________
# current author: Calum (AverageHomosapien)
# description: Unit tests for the binary heap class

import unittest
import binary_heap
import heapq

test_data = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
                (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)]

# Adding custom negative args since comparing to binary tree
neg_2 = [(-2, 2), (-1, 1)]
neg_4 = [(-4, 4), (-2, 2), (-3, 3), (-1, 1)]
neg_8 = [(-8, 8), (-5, 5), (-7, 7), (-4, 4), (-1, 1), (-6, 6), (-3, 3), (-2, 2)]

class TestBinaryHeap(unittest.TestCase):

    def test_init(self):
        BH = binary_heap.BinaryHeap(8, initial_heap=test_data)
        self.assertEqual(BH.queue, neg_8)

    def test_empty(self):
        BH = binary_heap.BinaryHeap()
        self.assertEqual(BH.get_max_priority(), 1)
        self.assertFalse(BH.pop())
        self.assertFalse(BH.pop_batch())

    def test_full(self):
        BH = binary_heap.BinaryHeap(max_len=4, initial_heap=test_data)
        self.assertTrue(BH.is_full())
        self.assertFalse(BH.push((5,5)))
        self.assertEqual(BH.get_size(), 4)

    def test_push(self):
        BH = binary_heap.BinaryHeap(max_len=2, initial_heap=test_data)
        BH.push((3,3))
        self.assertEqual(BH.queue, neg_2)
        self.assertEqual(BH.get_max_priority(), 2)

    def test_pop(self):
        BH = binary_heap.BinaryHeap(max_len=10, initial_heap=test_data, batch_size=5)
        self.assertEqual(BH.pop(), (10, 10))
        self.assertEqual(BH.pop(), (9, 9))
        self.assertEqual(BH.pop(), (8, 8))
        self.assertEqual(BH.pop(), (7, 7))
        self.assertEqual(BH.pop(), (6, 6))
        self.assertEqual(BH.pop_batch(), [(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)])

    def test_update(self):
        BH = binary_heap.BinaryHeap(max_len = 4, initial_heap=test_data)
        self.assertFalse(BH.update(8, 10))
        self.assertTrue(BH.update(4, 5))
        self.assertEqual(BH.pop(), (5, 4))
        self.assertEqual(BH.queue, [(-3, 3), (-2, 2), (-1, 1)])

    def test_prio_id(self):
        new_test_data = [(5, 4), (4, 3), (3, 2), (2, 1), (1, 0)]
        BH = binary_heap.BinaryHeap(initial_heap=new_test_data)
        self.assertEqual(BH.get_e_ids(), [4, 3, 2, 1, 0])
        self.assertEqual(BH.get_priorities(), [5, 4, 3, 2, 1])
