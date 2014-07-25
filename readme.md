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

In the example, I try to check best possible solution n-queen problem on 8x8 chess-board.
The purpose is as follow:
* Minimize the uncovered cell (Every cell in the board should be accessible by at least (and preferably) a queen)
* Minimize the count of the queen
* Minimize count of queens in the same row, column or diagonal

The result is as follow:
```
GENERATION 259
VARIATION : 243

  BENCHMARK    : fitness
  BEST GENE    : 0000010010000000000000100100000000000000000000010000000000001000
  BEST FITNESS : 266298.000000
  QUEEN COUNT  : 6
  UNCOVERED    : 0
  OVERLAPPED   : 0
  FORMATION    :
    xxxxx*xx
    *xxxxxxx
    xxxxxx*x
    x*xxxxxx
    xxxxxxxx
    xxxxxxx*
    xxxxxxxx
    xxxx*xxx
```
Good enough, you can use 6 queens in 8x8 chess-board

Note: `x` represent empty cell, while `*` represent queen position

Todo
----
* optimize the code
* implements genetics programming and grammatical evolution