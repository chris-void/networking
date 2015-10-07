# schedulers.py - the schedulers to use in the simulation
#
# CS655 simulation assignment
# Jeffrey Finkelstein
# October 2011
"""Provides schedulers and schedule items for use in the simulation.

The schedulers have a base class of `Scheduler`, and the defined scheduler
implementations include:

* `FIFO`, a naive first-in, first-out queue
* `RoundRobin`, a naive round-robin queue, which simply maintains a FIFO queue
  for each user providing inputs
* `DeficitRoundRobin`, a round-robin with a deficit counter for each user

Each scheduler allows enqueuing and dequeuing objects of the class `Item`. Each
scheduler also allows the possibility of specifying, on instantiation, a SimPy
`Monitor` or `Tally` object which will make observations on each enqueue and
dequeue call, recording the length (in number of waiting packets) of the queue.

"""
# TODO use a loop and `yield` statements in each `dequeue()` function?

import logging
logger = logging.getLogger(__name__)
"""The logger for this module."""


class Item(object):
    """An item with an owner and a length which can be scheduled."""

    def __init__(self, owner, length):
        """Creates the item with the specified `owner` (an integer) and
        `length`.

        """
        self.owner = owner
        self.length = length
        self.arrival_time = -1
        self.first_processed_time = -1

    def __str__(self):
        """Returns the string representation of this item."""
        return 'Item[owner: {0}, length: {1}]'.format(self.owner, self.length)


class Scheduler(object):
    """Unimplemented base class for other schedulers to extend."""

    def __init__(self, monitor=None):
        """Instantiates this scheduler (with access to the specified SimPy
        `Monitor` or `Tally` object, if it is not `None`).

        The specified SimPy `Monitor` or `Tally` object will record the length
        of the queue of waiting items of this scheduler after each enqueue and
        dequeue. The monitor should have been instantiated with a `sim`
        argument, which specifies the simulation in which the monitor is
        running. This is necessary for recording observation times.

        Subclasses may override this function.

        """
        self.monitor = monitor

    def enqueue(self, item, *args, **kw):
        """Enqueues the specified `item` and records the observation of the new
        length of the queue on the monitor specified in the constructor of this
        class (if not `None`).

        Positional and keyword arguments are passed on to the `_enqueue`
        function, which must be implemented by subclasses.

        """
        self._enqueue(item, *args, **kw)
        if self.monitor is not None:
            self.monitor.observe(len(self), t=self.monitor.sim.now())

    def dequeue(self, *args, **kw):
        """Removes and returns the element at the head of the queue and records
        the observation of the new length of the queue on the monitor specified
        in the constructor of this class (if not `None`).

        Positional and keyword arguments are passed on to the `_dequeue`
        function, which must be implemented by subclasses.

        """
        result = self._dequeue(*args, **kw)
        if self.monitor is not None:
            self.monitor.observe(len(self), t=self.monitor.sim.now())
        return result

    def _dequeue(self):
        """Dequeues the next item.

        Intentionally unimplemented in this class. Subclasses must implement
        this function.

        """
        pass

    def _enqueue(self, item):
        """Enqueues the specified item.

        Intentionally unimplemented in this class. Subclasses must implement
        this function.
        """
        pass


class FIFO(Scheduler):
    """A first-in, first-out scheduler which is just a naive queue processor.

    """
    def __str__(self):
        """Returns the string representation of the current state of this
        scheduler, which includes the queued items.

        """
        return '[' + ', '.join(str(item) for item in self.queue) + ']'

    def __len__(self):
        """Returns the number of items in this queue."""
        return len(self.queue)

    def __contains__(self, item):
        """Returns `True` if and only if `item` is contained in this queue."""
        return item in self.queue

    def __init__(self, *args, **kw):
        """Initializes an empty queue for incoming items.

        Positional and keyword arguments are passed to the constructor of the
        superclass.

        """
        super(FIFO, self).__init__(*args, **kw)
        self.queue = []

    def _enqueue(self, item):
        """Enqueues the specified item."""
        self.queue.append(item)

    def peek(self):
        """Returns (without removing) the next item in the queue which will be
        dequeued.

        """
        if len(self.queue) == 0:
            return None
        return self.queue[0]

    def _dequeue(self):
        """Removes and returns the next item from the queue, or `None` if the
        queue is empty.

        """
        if len(self.queue) == 0:
            return None
        return self.queue.pop(0)


class RoundRobin(Scheduler):
    """A naive round-robin scheduler, which maintains a queue for each user,
    and iteratively dequeues items from each one.

    """

    def __init__(self, *args, **kw):
        """Initializes a round-robin queue for an arbitrary number of users.

        Positional and keyword arguments are passed to the constructor of the
        superclass.

        """
        super(RoundRobin, self).__init__(*args, **kw)
        self.active_list = FIFO()
        self.queues = {}

    def __len__(self):
        """Returns the sum of the lengths of each of the queues, which is the
        total number of packets waiting in this scheduler.

        """
        return sum(len(queue) for queue in self.queues.values())

    def __str__(self):
        """Returns the string representation of the current state of this
        scheduler, which includes the mapping from user number to queued items
        for that user.

        """
        return str(dict((k, str(v)) for k, v in self.queues.items()))

    def _enqueue(self, item):
        """Enqueues the specified item.

        Enqueues the item on the queue belonging to the item's owner. If this
        is the first item from the item's owner, create a new queue for that
        user and enqueue the item on it. If the item's owner is not currently
        on the active list, enqueue it.

        """
        if item.owner not in self.active_list:
            self.active_list.enqueue(item.owner)
        if item.owner not in self.queues:
            self.queues[item.owner] = FIFO()
        self.queues[item.owner].enqueue(item)

    def _dequeue(self):
        """Removes and returns an item from the user at the head of the active
        list, or `None` if the active list is empty.

        """
        if len(self.active_list) == 0:
            return None
        current_user = self.active_list.dequeue()
        result = self.queues[current_user].dequeue()
        if len(self.queues[current_user]) > 0:
            self.active_list.enqueue(current_user)
        return result

    def peek(self):
        """Returns (without removing) the next item which will be dequeued."""
        if len(self.active_list) == 0:
            return None
        return self.queues[self.active_list.peek()].peek()


class DeficitRoundRobin(RoundRobin):
    """The deficit round-robin scheduler."""

    def __init__(self, quantum=9000, *args, **kw):
        """Calls the constructor of the superclass.

        The `quantum` is the length of data which is allowed to be sent per
        user per round. If the length of a user's next item is greater than the
        quantum (plus deficit from the previous round), it is not dequeued. If
        the length of a user's next item is at most the quantum (plus deficit
        from the previous round), it is dequeued and any leftover length is
        stored as deficit for the next round.

        """
        super(DeficitRoundRobin, self).__init__(*args, **kw)
        self.deficits = {}
        self.quantum = quantum
        # flag for whether this is the second (or greater) dequeued packet for
        # the current user; tells us when to provide the initial increment of
        # the deficit by the quantum size
        self.continuing_round = False
        self.current_user = None

    def _enqueue(self, item):
        """Enqueues the specified item in the queue of its owner, and sets that
        owner's deficit to zero if it was not already in the active list.

        """
        #if item.owner not in self.deficits:
        #    self.deficits[item.owner] = 0
        if item.owner not in self.queues:
            self.queues[item.owner] = FIFO()
        # if the item's owner does not have a currently active queue, and the
        # item's owner is not the user whose queue is currently being
        # processed.
        if (item.owner not in self.active_list
            and item.owner != self.current_user):
            self.active_list.enqueue(item.owner)
            self.deficits[item.owner] = 0
        self.queues[item.owner].enqueue(item)

    def _dequeue(self):
        """Removes and returns the next item from the queue of the next user in
        the active list, or returns `None` if the next item to dequeue is
        larger than the allowed length for that user for the current round, or
        returns `None` if the active list is empty.

        If the next item is larger than the allowed length for the current user
        for this round, then the item is **not** dequeued and `None` is
        returned.

        **Note**: this means that a call to `peek` may return an `Item`, but a
        call to `dequeue` at the same time may return `None`. Client code
        *must* handle this situation.

        If there is left over length in the quantum (plus previous round's
        deficit) for the current user, it is appended to the deficit length for
        that user's next round.

        Post-condition: if a user ID is in the active list, that user's queue
        is not empty.

        Post-condition: if self.current_user is `None`, then that user's queue
        is empty.

        """
        if len(self.active_list) == 0 and self.current_user is None:
            return None
        # if we are moving on to a new user's queue...
        if not self.continuing_round:
            self.current_user = self.active_list.dequeue()
            self.deficits[self.current_user] += self.quantum
            self.continuing_round = True
        result = None
        current_deficit = self.deficits[self.current_user]
        current_queue = self.queues[self.current_user]
        # if the current user has a packet to dequeue
        if len(current_queue) > 0:
            next_item_length = current_queue.peek().length
            # if the next packet is smaller than the current deficit
            if next_item_length <= current_deficit:
                result = current_queue.dequeue()
                self.deficits[self.current_user] -= result.length
            # else the next packet is too large
            else:
                self.continuing_round = False
                self.active_list.enqueue(self.current_user)
        # if we just dequeued the last packet...
        if len(self.queues[self.current_user]) == 0:
            self.continuing_round = False
            self.deficits[self.current_user] = 0
            self.current_user = None
        return result

    def peek(self):
        """Returns (without removing) the next item which will be dequeued.

        If the active list is empty, returns `None`.

        """
        # we may be in the middle of dequeuing a specific user's queue
        if self.current_user is not None:
            # never returns None, since if the queue is empty then current_user
            # is None
            return self.queues[self.current_user].peek()
        # if the active list is entirely empty, there are no packets to dequeue
        if len(self.active_list) == 0:
            return None
        # we may be in the case in which we have just emptied a queue for a
        # user but we have not yet set self.current_user to the next one
        return self.queues[self.active_list.peek()].peek()
