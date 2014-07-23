Gogenpy
=======

Go Frendi's implementation of Genetics Algorithm in Python

What's special?
---------------
* Object Oriented
* Multi Fitness Measurement

How to use?
-----------
* import gogenpy `from gogenpy import Gogenpy`
* Extends `Gogenpy` and override methods as you need
* Execute

What to override?
-----------------
* show_result(self, *args, **kwargs)
* mutation(self, benchmark)
* crossover(self, benchmark)
* new_individu(self)

Any example?
------------
[Please open rock.py](rock.py)

In the example, I try to check best possible solution of chess rock-problem (an easier version of queen problem).
The purpose is as follow:
* Minimize the uncovered cell (Every cell in the board should be accessible by any rock)
* Minimize the count of the rock
* Minimize overlapping of rock

The result is as follow:
```
GENERATION 52
VARIATION : 47

  BENCHMARK    : fitness
  BEST GENE    : 0001010000001000000101000
  BEST FITNESS : 16270.000000
  ROCK COUNT   : 5
  UNCOVERED    : 0
  OVERLAPPED   : 0
  FORMATION    :
    xxx*x
    *xxxx
    xx*xx
    xxxx*
    x*xxx
```
Note: `x` represent empty cell, while `*` represent rock position

Todo
----
* use queen or knight problem as example, rock is too easy
* optimize the code
* implements genetics programming and grammatical evolution