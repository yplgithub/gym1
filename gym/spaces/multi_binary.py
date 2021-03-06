from collections.abc import Sequence
import numpy as np
from .space import Space


class MultiBinary(Space):
    """
    An n-shape binary space.

    The argument to MultiBinary defines n, which could be a number or a `list` of numbers.

    Example Usage:

    >> self.observation_space = spaces.MultiBinary(5)

    >> self.observation_space.sample()

        array([0, 1, 0, 1, 0], dtype=int8)

    >> self.observation_space = spaces.MultiBinary([3, 2])

    >> self.observation_space.sample()

        array([[0, 0],
               [0, 1],
               [1, 1]], dtype=int8)

    """

    def __init__(self, n, seed=None):
        if isinstance(n, (Sequence, np.ndarray)):
            self.n = input_n = tuple(int(i) for i in n)
        else:
            self.n = n = int(n)
            input_n = (n,)

        assert (np.asarray(input_n) > 0).all(), "n (counts) have to be positive"

        super().__init__(input_n, np.int8, seed)

    def sample(self):
        return self.np_random.integers(low=0, high=2, size=self.n, dtype=self.dtype)

    def contains(self, x):
        if isinstance(x, Sequence):
            x = np.array(x)  # Promote list to array for contains check
        if self.shape != x.shape:
            return False
        return ((x == 0) | (x == 1)).all()

    def to_jsonable(self, sample_n):
        return np.array(sample_n).tolist()

    def from_jsonable(self, sample_n):
        return [np.asarray(sample) for sample in sample_n]

    def __repr__(self):
        return f"MultiBinary({self.n})"

    def __eq__(self, other):
        return isinstance(other, MultiBinary) and self.n == other.n
