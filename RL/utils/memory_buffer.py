import random
import numpy as np

from collections import deque
from .sumtree import SumTree


class MemoryBuffer(object):

    def __init__(self, buffer_size, with_per=False):

        if(with_per):

            self.alpha = 0.5
            self.epsilon = 0.01
            self.buffer = SumTree(buffer_size)
        else:

            self.buffer = deque()
        self.count = 0
        self.with_per = with_per
        self.buffer_size = buffer_size

    def memorize(self, state, action, reward, done, new_state, error=None):

        experience = (state, action, reward, done, new_state)
        if(self.with_per):
            priority = self.priority(error[0])
            self.buffer.add(priority, experience)
            self.count += 1
        else:
            if self.count < self.buffer_size:
                self.buffer.append(experience)
                self.count += 1
            else:
                self.buffer.popleft()
                self.buffer.append(experience)

    def priority(self, error):
        return (error + self.epsilon) ** self.alpha

    def size(self):
        return self.count

    def sample_batch(self, batch_size):

        batch = []

        if(self.with_per):
            T = self.buffer.total() // batch_size
            for i in range(batch_size):
                a, b = T * i, T * (i + 1)
                s = random.uniform(a, b)
                idx, error, data = self.buffer.get(s)
                batch.append((*data, idx))
            idx = np.array([i[5] for i in batch])
        elif self.count < batch_size:
            idx = None
            batch = random.sample(self.buffer, self.count)
        else:
            idx = None
            batch = random.sample(self.buffer, batch_size)

        s_batch = np.array([i[0] for i in batch])
        a_batch = np.array([i[1] for i in batch])
        r_batch = np.array([i[2] for i in batch])
        d_batch = np.array([i[3] for i in batch])
        new_s_batch = np.array([i[4] for i in batch])
        return s_batch, a_batch, r_batch, d_batch, new_s_batch, idx

    def update(self, idx, new_error):
        self.buffer.update(idx, self.priority(new_error))

    def clear(self):
        if(self.with_per):
            self.buffer = SumTree(buffer_size)
        else:
            self.buffer = deque()
        self.count = 0
