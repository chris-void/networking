# test_schedulers.py - unit tests for the schedulers module
#
# CS655 simulation assignment
# Jeffrey Finkelstein
# October 2011
"""Unit tests for the schedulers module."""
from unittest import TestCase

from SimPy.Simulation import Tally

from simulation.schedulers import DeficitRoundRobin
from simulation.schedulers import FIFO
from simulation.schedulers import Item
from simulation.schedulers import RoundRobin

__all__ = ['DeficitRoundRobinTest', 'FIFOTest', 'RoundRobinTest',
           'SchedulerTest']


class SchedulerTest(TestCase):
    """Base class for scheduler test classes."""

    def __init__(self, *args, **kw):
        """Initializes the test case by adding the `assertItemsEqual` function
        as the equality assertion function for `Item` objects.

        """
        super(SchedulerTest, self).__init__(*args, **kw)
        self.addTypeEqualityFunc(Item, self.assertItemsEqual)

    def setUp(self, scheduler_class, *args, **kw):
        """Initializes the scheduler with the specified class for testing."""
        self.scheduler = scheduler_class(*args, **kw)

    def assertItemsEqual(self, item1, item2, msg=None):
        """Asserts that all the named attributes of the two specified Item
        objects are equal.

        """
        self.assertEqual(item1.__dict__, item2.__dict__, msg)


class FIFOTest(SchedulerTest):
    """Test class for the FIFO scheduler class."""

    def setUp(self):
        """Initializes the FIFO scheduler to test."""
        super(FIFOTest, self).setUp(FIFO)

    def test_monitor(self):
        """Tests that the monitor correctly observes the length of this queue
        on enqueue and dequeue calls.

        """
        monitor = Tally()
        self.scheduler = FIFO(monitor)
        for n in range(100):
            self.scheduler.enqueue(Item(n, n))
            self.assertEqual(n + 1, monitor.count())

    def test_len(self):
        """Tests that the scheduler correctly reports its length as the number
        of queued items.

        """
        for n in range(100):
            self.scheduler.enqueue(Item(n, n))
        self.assertEqual(100, len(self.scheduler))

    def test_enqueue_dequeue(self):
        """Tests that enqueuing items results in a queue with the correct
        ordering of items.

        """
        for n in range(100):
            self.scheduler.enqueue(Item(n, 100 * n))
        for n in range(100):
            item = self.scheduler.dequeue()
            self.assertEqual(n, item.owner)
            self.assertEqual(100 * n, item.length)
        self.assertIsNone(self.scheduler.dequeue())


class RoundRobinTest(SchedulerTest):
    """Test class for the round-robin scheduler class."""

    def setUp(self):
        """Initializes the round-robin scheduler to test."""
        super(RoundRobinTest, self).setUp(RoundRobin)

    def test_len(self):
        """Tests that the scheduler correctly reports the number of packets
        waiting for all users.

        """
        for user_num in range(10):
            for num_items in range(user_num):
                self.scheduler.enqueue(Item(user_num, 1))
        expected_total = sum(range(10))
        self.assertEqual(expected_total, len(self.scheduler))

    def test_enqueue_dequeue(self):
        """Tests that enqueuing items places each item in the correct order and
        in the correct queue for each user.

        """
        # user number n should get items of length 10n+0, 10n+1, 10n+2, ...
        for item_num in range(10):
            for user_num in range(10):
                item = Item(user_num, 10 * user_num + item_num)
                self.scheduler.enqueue(item)
        # there are 10 items for each of the 10 users
        for n in range(100):
            item = self.scheduler.dequeue()
            self.assertEqual((n % 10) * 10 + (n // 10), item.length)
            self.assertEqual(n % 10, item.owner)
        self.assertIsNone(self.scheduler.dequeue())

    def test_peek(self):
        """Tests that the peek() function returns the packet at the head of the
        next user's queue.

        """
        # enqueue items in reverse numerical order
        for n in range(9, -1, -1):
            self.scheduler.enqueue(Item(n, 100))
        # items should be dequeued in the order in which they were added, since
        # the numbers were added to the active list in that order
        for n in range(9, -1, -1):
            peeked_item = self.scheduler.peek()
            self.assertEqual(n, peeked_item.owner)
            dequeued_item = self.scheduler.dequeue()
            self.assertIs(peeked_item, dequeued_item)
        self.assertEqual(0, len(self.scheduler))

    def test_len(self):
        """Tests that the length is correctly reported as the total number of
        waiting packets.

        """
        for n in range(100):
            self.scheduler.enqueue(Item(n % 10, 100))
            self.assertEqual(n + 1, len(self.scheduler))


class DeficitRoundRobinTest(SchedulerTest):
    """Test class for the deficit round-robin scheduler class."""

    def setUp(self):
        """Initializes the deficit round-robin scheduler to test with the
        default quantum size.

        """
        super(DeficitRoundRobinTest, self).setUp(DeficitRoundRobin,
                                                 quantum=500)

    def test_lengths_equal_quantum(self):
        """Tests that for lengths of exactly the quantum size, each scheduled
        item is dequeued as in the naive round-robin scheduler.

        """
        scheduler2 = RoundRobin()
        item1 = Item(0, 500)
        item2 = Item(0, 500)
        item3 = Item(1, 500)
        item4 = Item(1, 500)
        for item in item1, item2, item3, item4:
            self.scheduler.enqueue(item)
            scheduler2.enqueue(item)
        self.assertEqual(scheduler2.dequeue(), self.scheduler.dequeue())
        # returns None when item length < deficit
        self.assertIsNone(self.scheduler.dequeue())
        self.assertEqual(scheduler2.dequeue(), self.scheduler.dequeue())
        # returns None when item length < deficit
        self.assertIsNone(self.scheduler.dequeue())
        self.assertEqual(scheduler2.dequeue(), self.scheduler.dequeue())
        self.assertEqual(scheduler2.dequeue(), self.scheduler.dequeue())

    def test_small_lengths(self):
        """Tests that when items smaller than the quantum size are enqueued and
        dequeued, the deficit size for the queuing user increases.

        """
        self.scheduler = DeficitRoundRobin()
        enqueued_item = Item(0, 400)
        self.scheduler.enqueue(enqueued_item)
        dequeued_item = self.scheduler.dequeue()
        self.assertEqual(enqueued_item, dequeued_item)
        self.assertNotEqual(100, self.scheduler.deficits[0])
        self.assertEqual(0, self.scheduler.deficits[0])

        self.scheduler.enqueue(enqueued_item)
        dequeued_item = self.scheduler.dequeue()
        self.assertEqual(enqueued_item, dequeued_item)
        self.assertNotEqual(200, self.scheduler.deficits[0])
        self.assertEqual(0, self.scheduler.deficits[0])

    def test_large_lengths(self):
        """Tests that when items larger than the quantum size are enqueued, the
        deficit size grows until it is larger than the length of the item.

        """
        self.scheduler = DeficitRoundRobin(quantum=500)
        enqueued_item = Item(0, 600)
        self.scheduler.enqueue(enqueued_item)
        dequeued_item = self.scheduler.dequeue()
        self.assertIsNone(dequeued_item)
        dequeued_item = self.scheduler.dequeue()
        self.assertIs(enqueued_item, dequeued_item)
        # deficit gets reset when there are no packets left in user's queue
        self.assertNotEqual(400, self.scheduler.deficits[0])
        self.assertEqual(0, self.scheduler.deficits[0])

    def test_multiple_packets_dequeued(self):
        """Tests that multiple packets are dequeued if the quantum is large
        enough.

        """
        item1 = Item(0, 100)
        item2 = Item(0, 200)
        item3 = Item(0, 700)
        item4 = Item(1, 250)
        item5 = Item(1, 250)
        item6 = Item(1, 500)
        self.scheduler.enqueue(item1)
        self.scheduler.enqueue(item2)
        self.scheduler.enqueue(item3)
        self.scheduler.enqueue(item4)
        self.scheduler.enqueue(item5)
        self.scheduler.enqueue(item6)
        self.assertIs(item1, self.scheduler.dequeue())
        self.assertIs(item2, self.scheduler.dequeue())
        self.assertIsNone(self.scheduler.dequeue())
        self.assertEqual(200, self.scheduler.deficits[0])
        # since there was a deficit, user 0's round ended, but was re-added to
        # the active list
        self.assertIn(0, self.scheduler.active_list)
        self.assertIn(1, self.scheduler.active_list)
        self.assertIs(item4, self.scheduler.dequeue())
        self.assertIs(item5, self.scheduler.dequeue())
        self.assertEqual(0, self.scheduler.deficits[1])
        self.assertIn(0, self.scheduler.active_list)
        # 1 is the current user, so it is not currently in the active list
        self.assertNotIn(1, self.scheduler.active_list)
        # next packet is too large, so return None and switch to user 0
        self.assertIsNone(self.scheduler.dequeue())
        self.assertIs(item3, self.scheduler.dequeue())
        self.assertIs(item6, self.scheduler.dequeue())
