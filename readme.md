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

Genetics Algorithm Example
--------------------------

[Please open n-queen.py](n-queen.py)

In the example, I try to find the minimum number of queens needed to occupy or attack all squares.
Please take a look at [this link](http://mathworld.wolfram.com/QueensProblem.html) for more information.

I use this configuration:
```
ga = GA_N_Queen(board_size=8, 
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

Grammatical Evolution Example
-----------------------------

[Please open math.py](math.py)

In the example, I try to find a function `f(x)` that is closest to `x^3`.
To achieve this, I make a training set contains xs and ys as follows:
```
x = np.linspace(0,99,100)
y = pow(x,3)
```

Then, I use this configuration and run the program:
```
ge = GE_Function_Prediction(
    bnf={
        '<expr>'    : ['<expr> <op> <expr>', '<func>(<expr>)','<func>(<expr>)', 'x', '<number>'],
        '<func>'    : ['np.sin', 'np.cos', 'np.tan'],
        '<op>'      : ['+', '-', '*'],
        '<number>'  : ['<int>', '<int>', '<float>'],
        '<digit>'   : ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
        '<int>'     : ['<digit>', '<digit>', '<digit><int>'],
        '<float>'   : ['<int>.<int>']
    },
    gene_size = 20,
    population_size = 100, max_epoch = 1000, 
    operation_rate={'mutation':40, 'crossover':40},
    elitism_rate = 10,
    new_rate = 10,
    verbose=True)
ge.execute()
```

And here is the result:
```
GENERATION 136
VARIATION : 47

  BENCHMARK    : fitness
  BEST GENE    : 0000111010101110011
  BEST FITNESS : 100000000000000000000.000000
  PHENOTYPE    : x * x * x
TOTAL POSSIBLE SOLUTION EVALUATED : 9390
```

It is pretty slow to find that `x^3` is equal to `x*x*x`.
May be I should do some optimization, or may be you should :)


Todo
----
* optimize the code