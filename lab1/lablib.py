from gx_utils import PriorityQueue


class Frontier:
    # store tuples instead of lists, solves hashing problem
    def __init__(self):
        self.pq = PriorityQueue()

    def __contains__(self, item):
        return tuple(item) in self.pq

    def __bool__(self):
        return bool(self.pq)

    def add(self, state, cost):
        self.pq.push(tuple(state), p=cost)

    def pop(self):
        return list(self.pq.pop())

