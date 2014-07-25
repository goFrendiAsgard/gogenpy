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

In the example, I try to find the minimum number of queens needed to occupy or attack all squares.
Please take a look at [this link](http://mathworld.wolfram.com/QueensProblem.html) for more information.

I use this configuration:
```
ga = GA_For_Queen(board_size=8, 
    population_size = 1000, max_epoch = 1000, 
    operation_rate={'mutation':40, 'crossover':40},
    elitism_rate = 10,
    new_rate = 10,
    verbose = False)
ga.execute()
```

And the result is as follow:
```
GENERATION 108
VARIATION : 495

  BENCHMARK    : fitness
  BEST GENE    : 0000000000000100100000000000000000010000000000000000000100100000
  BEST FITNESS : 266299.000000
  QUEEN COUNT  : 5
  UNCOVERED    : 0
  OVERLAPPED   : 0
  FORMATION    :
    xxxxxxxx
    xxxxx*xx
    *xxxxxxx
    xxxxxxxx
    xxx*xxxx
    xxxxxxxx
    xxxxxxx*
    xx*xxxxx
```
Good, the program shows that I need 5 queens to occupy or attack all squares in 8x8 chess-board.

Note: 
* `x` represent empty cell, while `*` represent queen position.
* I attempt several failures before finding this configuration. In genetics algorithm, there is no guarantee you will find a perfectly best solution.

Todo
----
* optimize the code
* implements genetics programming and grammatical evolution