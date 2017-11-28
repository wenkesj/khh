# -*- coding: utf-8 -*-
from __future__ import print_function

import enum, unittest

from khh import KHeavyHitters


Dozen = 12
HalfDozen = Dozen / 2
BakersDozen = Dozen + 1
Bushel = 125


class Fruits(enum.Enum):
  Apple = 'apple'
  Orange = 'orange'
  Banana = 'banana'
  Strawberry = 'strawberry'
  Kiwi = 'kiwi'
  Mango = 'mango'


class KHeavyHittersTest(unittest.TestCase):
  """
  Tests for KHeavyHitters
  """
  def test_add(self):
    k = 5
    counts = dict()
    khh = KHeavyHitters(k)

    # add a single banana
    khh.add(Fruits.Banana)

    # add a dozen apples
    for i in range(Dozen):
      khh.add(Fruits.Apple)
    counts[Fruits.Apple] = i

    # add 2 "bushel"s of mangos, we like mangos
    for i in range(Bushel * 2):
      khh.add(Fruits.Mango)
    counts[Fruits.Mango] = i

    # add a bakers oranges
    for i in range(BakersDozen):
      khh.add(Fruits.Orange)
    counts[Fruits.Orange] = i

    # add a "bushel"
    for i in range(Bushel):
      khh.add(Fruits.Strawberry)
    counts[Fruits.Strawberry] = i

    top_k = khh.top_k()
    for f, v in counts.items():
      if v >= (len(khh) / k):
        self.assertTrue(f in top_k)
