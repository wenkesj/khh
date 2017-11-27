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
    khh = KHeavyHitters(5)

    # add a single banana
    khh.add(Fruits.Banana)

    # add a dozen apples
    for _ in range(Dozen):
      khh.add(Fruits.Apple)

    # add 2 "bushel"s of mangos, we like mangos
    for _ in range(Bushel * 2):
      khh.add(Fruits.Mango)

    # add 2 dozen oranges
    for _ in range(BakersDozen):
      khh.add(Fruits.Orange)

    # add a "bushel"
    for _ in range(Bushel):
      khh.add(Fruits.Strawberry)

    assert len(khh.k()) == len(khh._priority_queue)
