from gogenpy import GE, random
import numpy as np
from scipy.stats.stats import pearsonr

'''
Function Prediction, given x & y (noised), try to guess the function!
'''
x = np.linspace(0,99,100)
y = pow(x,3)

class GE_Function_Prediction(GE):
    def __init__(self, *args, **kwargs):
        GE.__init__(self, *args, **kwargs)
        self._x = np.array(kwargs.pop('x', x))
        self._y = np.array(kwargs.pop('y', y))



    def mse(self, prediction_list):
        prediction_list = np.array(prediction_list)
        return ((prediction_list - self._y) ** 2).mean()

    def calculate_fitness(self, gene, benchmark):
        try:
            gene, phenotype = self.translate(gene)
            # translation was failed
            if phenotype == self._failure_expression:
                return(gene, self._broken_fitness)
            # generate program
            global_sandbox = {'x_list' : self._x}
            local_sandbox = {}
            exec('import numpy as np\n' +\
                 'y=[]\n'+\
                 'for x in x_list:\n' +\
                 '    y.append('+phenotype+')', global_sandbox, local_sandbox)
            y = np.array(local_sandbox['y'])
            #pearsonr = pearsonr(self._y, y)
            mse = ((y - self._y) ** 2).mean()
            # calculate fitness of the program
            fitness = 1/(mse + self._minimum_fitness)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            return (gene, self._broken_fitness)
        return(gene, fitness)

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
    #procreation_individuals = ['00001110011','0000111000001110011'],
    gene_size = 20,
    population_size = 100, max_epoch = 1000, 
    operation_rate={'mutation':40, 'crossover':40},
    elitism_rate = 10,
    new_rate = 10,
    verbose=True)
ge.execute()
