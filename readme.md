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
[Please open n-queen.py](n-queen.py)

In the example, I try to check best possible solution n-queen problem on 5x5 chess-board.
The purpose is as follow:
* Minimize the uncovered cell (Every cell in the board should be accessible by at least (and preferably) a queen)
* Minimize the count of the queen
* Minimize count of queens in the same row, column or diagonal

The result is as follow:
```
GENERATION 100
VARIATION : 77

  BENCHMARK    : fitness
  BEST GENE    : 1000000010000000010000000
  BEST FITNESS : 16272.000000
  QUEEN COUNT  : 3
  UNCOVERED    : 0
  OVERLAPPED   : 0
  FORMATION    :
    *xxxx
    xxx*x
    xxxxx
    xx*xx
    xxxxx
```
Good enough, you can use 3 queens in 5x5 chess-board

Note: `x` represent empty cell, while `*` represent queen position

Todo
----
* optimize the code
* implements genetics programming and grammatical evolution