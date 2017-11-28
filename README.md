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
# [<Fruits.Mango: 'mango'>, <Fruits.Strawberry: 'strawberry'>, <Fruits.Orange: 'orange'>]

for f, v in counts.items():
  if v >= (len(khh) / k): # items that show up more than (n / k) times :)
    assert f in top_k
```
