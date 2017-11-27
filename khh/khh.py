# -*- coding: utf-8 -*-
from __future__ import absolute_import

import math, time

import numpy as np

from .pqueue import PriorityQueue


class KHeavyHitters(object):
  def __init__(self, k,
               eps=.00001, confidence=.99, k_factor=1,
               dtype=np.int32, random_state=0):
    """Create a new KHeavyHitters sketch.

    This is a solution to the problem:
      Given a data stream of length m and a parameter k,
      find all elements that occur atleast m/k times.

    Args:
      k: finds elements of atleast m/k times.
      eps: computes the width `int(math.ceil(2 / eps))`.
      confidence: computes the depth `int(math.ceil(-math.log(1 - confidence) / math.log(2)))`.
      k_factor: optional, factor to multiply k by to example the table size.
      dtype: datatype of the underlying table.
      random_state: a `RandomState` object, see `numpy.random.RandomState`.
    """
    self._k = int(k * math.log(k, 10)) * int(k_factor)
    if not isinstance(random_state, np.random.RandomState):
      self._random_state = np.random.RandomState(random_state)
    else:
      self._random_state = random_state
    self._items = dict()
    self._width = int(math.ceil(2 / eps))
    self._depth = int(math.ceil(-math.log(1 - confidence) / math.log(2)))
    self._sketch_table = np.zeros((self._depth, self._width), dtype=dtype)
    self._hash_vector = self._random_state.randint(low=0, high=np.iinfo(dtype).max,
                                                   size=self._depth, dtype=dtype)
    self._size = 0
    self._priority_queue = PriorityQueue()
    self.__k__ = k

  def __str__(self):
    return '<KHeavyHitters(k={})>'.format(self.__k__)

  def _hash(self, item, idx):
    """Hashes an item with the given index idx"""
    info = np.iinfo(self._hash_vector.dtype)
    h = self._hash_vector[idx] * item
    h += h >> info.bits
    h &= info.max
    return h % self._width

  def _add_long(self, item, count, return_min=True):
    """Adds an item to the sketch and returns the minimum/maximum count"""
    compare = lambda x, y: x < y if return_min else lambda x, y: x > y
    h = self._hash(item, 0)
    self._sketch_table[0, h] += count
    target = self._sketch_table[0, h]
    for i in range(1, self._depth):
      h = self._hash(item, i)
      self._sketch_table[i, h] += count
      if compare(self._sketch_table[i, h], target):
        target = self._sketch_table[i, h]
    self._size += count
    return target

  def _hash_item(self, item):
    """Default hashing for object ids compatible with the table."""
    return hash(item) if not hasattr(item, "id") else item.id

  def query(self, item):
    """Queries the sketch for the minimum response of the table.

    Args:
      item: object with "id" field or is hashable without it.
    """
    hash_code = self._hash_item(item)
    minimum = self._sketch_table[0, self._hash(hash_code, 0)]
    for i in range(1, self._depth):
      h = self._hash(hash_code, i)
      if self._sketch_table[i, h] < minimum:
        minimum = self._sketch_table[i, h]
    return minimum

  def add(self, item, update_func=None):
    """Adds an item to the sketch.

    Args:
      item: object with "id" attribute or is hashable without it (i.e. overrides `__hash__`).
      update_func: optionally, callback with (item, probed) as a parameters when a colission is detected.
    """
    probed = None
    hash_code = self._hash_item(item)
    count = self._add_long(hash_code, 1, return_min=True)
    probes = [hash_code] if not hasattr(item, "ids") else [hash_code, item.ids]

    for hash_code in probes:
      if hash_code in self._items:
        probed = self._items[hash_code]
        del self._items[hash_code]
      if probed is not None:
        break

    if probed is None:
      self._items[hash_code] = item
      self._priority_queue.push(hash_code, count)
    else:
      pid = self._hash_item(probed)
      self._priority_queue.remove(pid)
      if update_func is not None:
        update_func(item, probed)
      self._items[pid] = probed
      self._priority_queue.push(pid, count)

    if len(self._priority_queue) > (self._k):
      removed = self._priority_queue.pop()
      if removed in self._items:
        del self._items[removed]

  def k(self):
    """Return the top-k of the sketch

    Returns:
      the top-k of the sketch
    """
    return [self._items[top] for top in self._priority_queue.nlargest(self.__k__)]

  @property
  def shape(self):
    """Return the shape of the CMS table.

    Returns:
      the shape of the underlying CMS table.
    """
    return (self._width, self._depth)

  def __getitem__(self, query):
    return self.query(query)

  def __contains__(self, query):
    return self.query(query) != 0

  def __len__(self):
    return self._size

  push = add
  append = add
  top = k
