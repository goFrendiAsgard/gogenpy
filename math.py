from gogenpy import GE, random
import numpy as np

'''
Function Prediction, given x & y (noised), try to guess the function!
'''
x = np.linspace(0,99,100)
y = np.sin(x)

class GE_Function_Prediction(GE):
    def __init__(self, *args, **kwargs):
        GE.__init__(self, *args, **kwargs)
        self._x = np.array(kwargs.pop('x', x))
        self._y = np.array(kwargs.pop('y', y))

    def mse(self, prediction_list):
        prediction_list = np.array(prediction_list)
        return ((prediction_list - self._y) ** 2).mean(axis=None)

    def calculate_fitness(self, gene, benchmark):
        try:
            gene, phenotype = self.translate(gene)
        except:
            return (gene, 0)
        # eval
        try:
            global_sandbox = {'x_list' : self._x}
            local_sandbox = {}
            exec('import numpy as np\n' +\
                 'y=[]\n'+\
                 'for x in x_list:\n' +\
                 '    y.append('+phenotype+')', global_sandbox, local_sandbox)
            y = local_sandbox['y']
            fitness = 1/(self.mse(y) + 0.000001)
        except:
            fitness = 0
        return(gene, fitness)

    def show_result(self, *args, **kwargs):
        print('\nGENERATION %d' %(self._epoch+1))
        variation = self.individu_variation()
        print('VARIATION : %d\n' %(variation))
        for benchmark in self._benchmark_list:
            individu = self._population_sorted[benchmark][0]
            gene = individu['gene']
            print('  BENCHMARK    : %s' %(benchmark))
            print('  BEST GENE    : %s' %(str(gene)))
            print('  BEST FITNESS : %f' %(individu['fitness'][benchmark]))
            try:
                print('  PHENOTYPE    : %s' %(self.translate(gene)[1]))
            except:
                print('  PHENOTYPE UNTRANSTATABLE')

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
