# khh
K- Heavy Hitters data-structure implemented in `python`. [This is a nice reference](http://theory.stanford.edu/~tim/s17/l/l2.pdf) for the problem and implementation.

```sh
git clone https://github.com/wenkesj/khh.git
(cd khh && python setup.py install)
```

Trivial example:

```python
import enum

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


khh = KHeavyHitters(5)

# add a single banana
khh.add(Fruits.Banana)

# add a dozen apples
for _ in range(Dozen):
  khh.add(Fruits.Apple)

# add 2 "bushel"s of mangos, we like mangos
for _ in range(Bushel * 2):
  khh.add(Fruits.Mango)

# add a bakers dozen oranges
for _ in range(BakersDozen):
  khh.add(Fruits.Orange)

# finally, add a "bushel" of strawberries
for _ in range(Bushel):
  khh.add(Fruits.Strawberry)

print(khh.k())
# [<Fruits.Mango: 'mango'>, <Fruits.Strawberry: 'strawberry'>, <Fruits.Orange: 'orange'>]

# the reason this is 3 is because of the underlying _priority_queue,
# it aggressively tries to save space.
assert len(khh.k()) == len(khh._priority_queue)

```
