from gogenpy import GE, random
import numpy as np, math
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

    def normalize_infinite_range(self,value):
        # the return value will vary from -1 (for value=-infinite) to 1 (for value=infinite)
        return 2 * math.atan(value) / (22/7.0)

    def calculate_fitness(self, gene, benchmark):
        try:
            gene, phenotype = self.translate(gene)
            # translation was failed
            if phenotype == self._failure_expression or phenotype == '':
                return(gene, self._broken_fitness)
            # generate program
            global_sandbox = {'x_list' : self._x}
            local_sandbox = {}
            exec('import numpy as np\n' +\
                 'y=[]\n'+\
                 'for x in x_list:\n' +\
                 '    y.append('+phenotype+')', global_sandbox, local_sandbox)
            y = np.array(local_sandbox['y'])
            correlation = pearsonr(y, self._y)[0]
            if math.isnan(correlation):
                correlation = 0
            mse = ((y - self._y) ** 2).mean()
            # calculate fitness of the program
            fitness = correlation + (2 if mse==0 else 2 * self.normalize_infinite_range(mse))
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception, e:
            print (e.message)
            return (gene, self._broken_fitness)
        return(gene, fitness)

ge = GE_Function_Prediction(
    bnf={
        '<expr>'    : ['<expr> <op> <expr>', 'x', '<number>'],
        '<op>'      : ['+', '-', '*'],
        '<number>'  : ['<int>', '<int>', '<float>'],
        '<digit>'   : ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
        '<int>'     : ['<digit>', '<digit>', '<digit><int>'],
        '<float>'   : ['<int>.<int>']
    },
    #procreation_individuals = ['00011000011001'],
    gene_size = 20,
    population_size = 1000, max_epoch = 1000, 
    operation_rate={'mutation':40, 'crossover':40},
    elitism_rate = 10,
    new_rate = 10,
    verbose=True)
ge.execute()
