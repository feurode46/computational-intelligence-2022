from gx_utils import PriorityQueue


class Frontier:
    # store tuples instead of lists, solves hashing problem
    def __init__(self):
        self.pq = PriorityQueue()

    def __contains__(self, item):
        return self.tuplize(item) in self.pq

    def __bool__(self):
        return bool(self.pq)

    def push(self, state, p):
        self.pq.push(self.tuplize(state), p=p)

    def pop(self):
        return self.listize(self.pq.pop())

    def tuplize(self, item):
        tuples = list()
        for el in item:
            tuples.append(tuple(el))
        return tuple(tuples)

    def listize(self, tuple_of_tuples):
        l = list()
        for el in tuple_of_tuples:
            l.append(list(el))
        return l

    @property
    def length(self):
        return len(self.pq.data_set)


class State:
    def __init__(self, data):
        self._data = data.copy()

    def __hash__(self):
        return hash(bytes(self._data))

    def __eq__(self, other):
        return bytes(self._data) == bytes(other._data)

    def __lt__(self, other):
        return bytes(self._data) < bytes(other._data)

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return repr(self._data)

    @property
    def data(self):
        return self._data

    def copy_data(self):
        return self._data.copy()
