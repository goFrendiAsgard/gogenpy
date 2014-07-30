Gogenpy
=======

Go Frendi's implementation of Genetics Algorithm in Python

What's special?
---------------
* Object Oriented
* Multi Fitness Measurement (Not pretty useful for normal case)
* Beside Elitism and New Individu (Imigration), you are free to define your own operators
* You can add `procreation_individual` into the first population, thus ensuring that the fitness values of the populations will not lower than the solution you guessed.

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
```python
ga = GA_N_Queen(board_size=8, 
    population_size = 2000, max_epoch = 1000, 
    operation_rate={
        'mutation':20, 
        'mutation_move_queen':15,
        'mutation_kill_queen':15,
        'crossover':15},
    elitism_rate = 10,
    new_rate = 10,
    verbose = False)
```

There are 2 custom operations I add, `mutation_move_queen` and `mutation_kill_queen` which are defined as follow:

```python
    def get_queen_index_list(self, gene):
        queen_index_list = []
        for i in xrange(len(gene)):
            if gene[i] == '1':
                queen_index_list.append(i)

    def mutation_kill_queen(self, gene):
        queen_index_list = self.get_queen_index_list
        number = queen_index_list[random.randrange(len(queen_index_list))]
        gene = gene[:number] + '0' + gene[number+1:]
        return gene

    def mutation_move_queen(self, gene):
        queen_index_list = self.get_queen_index_list
        number_1 = queen_index_list[random.randrange(len(queen_index_list))]
        number_2 = random.randrange(len(gene))
        if number_1 < number_2:
            gene = gene[:number_1] + gene[number_2] + gene[number_1+1:number_2] + gene[number_1] + gene[number_2+1:]
        else:
            gene = gene[:number_2] + gene[number_1] + gene[number_2+1:number_1] + gene[number_2] + gene[number_1+1:]
        return gene
```
`mutation_kill_queen` is used to eliminate a queen from a board, while `mutation_move_queen` is used to move queen to another square

And the result is as follow:
```
GENERATION 58
VARIATION : 990

  BENCHMARK    : fitness
  BEST GENE    : 0000000000000000000100000000001000001000000000011000000000000000
  BEST FITNESS : 265984.000000
  QUEEN COUNT  : 5
  UNCOVERED    : 0
  OVERLAPPED   : 0
  FORMATION    :
    xxxxxxxx
    xxxxxxxx
    xxx*xxxx
    xxxxxx*x
    xxxx*xxx
    xxxxxxx*
    *xxxxxxx
    xxxxxxxx
TOTAL POSSIBLE SOLUTION EVALUATED : 57159
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
```python
ge = GE_Function_Prediction(
    bnf={
        '<expr>'    : ['<expr> <op> <expr>', 'x', '<number>'],
        '<op>'      : ['+', '-', '*'],
        '<number>'  : ['<int>', '<int>', '<float>'],
        '<digit>'   : ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
        '<int>'     : ['<digit>', '<digit>', '<digit><int>'],
        '<float>'   : ['<int>.<int>']
    },
    gene_size = 20,
    population_size = 1000, max_epoch = 1000, 
    operation_rate={'mutation':40, 'crossover':40},
    elitism_rate = 10,
    new_rate = 10,
    verbose=True)
ge.execute()
```

And here is the result:
```
GENERATION 1
VARIATION : 482

  BENCHMARK    : fitness
  BEST GENE    : 11011011011001
  BEST FITNESS : 3.000000
  PHENOTYPE    : x * x * x
TOTAL POSSIBLE SOLUTION EVALUATED : 1618
```

It is pretty quick to find that `x^3` is equal to `x*x*x`.
But I am not really happy with this, because convergance was appeared too quick.
May be I should do some optimization, or may be you should :)


Todo
----
* optimize the code