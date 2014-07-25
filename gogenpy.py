import math, random
random.seed(1500)

class Gogenpy(object):
    '''
    individu structure is as follow
        {
            'gene' : '010001000100',
            'fitness' : {'intelligent' : 5, 'agility' : 6, 'strength' : 4},
            'accumulation' : {'intelligent' : 15, 'agility' : 16, 'strength' : 14}
        }
    '''

    def __init__(self, *args, **kwargs):
        self._max_epoch = kwargs.pop('max_epoch', 50)
        self._population_size = kwargs.pop('population_size', 20)
        self._benchmark_list = kwargs.pop('benchmark',['fitness'])
        self._operation_list = kwargs.pop('operation',['mutation','crossover'])
        self._operation_rate = kwargs.pop('operation_rate',{'mutation':30, 'crossover':30})
        self._elitism_rate = kwargs.pop('elitism_rate',20)
        self._new_rate = kwargs.pop('new_rate',20)
        self._gene_size = kwargs.pop('gene_size',50)
        self._verbose = kwargs.pop('verbose',True)
        self._epoch                  = 0
        self._population             = []
        self._population_sorted      = {}
        self._generation             = []
        self._generation_sorted      = []
        self._memoized_gene          = []
        self._memoized_fitness       = []
        # get total rate
        total_operation_rate = reduce(lambda x,y: x+self._operation_rate[y], self._operation_rate, 0)
        total_rate = total_operation_rate + self._elitism_rate + self._new_rate
        new_total_rate = 0
        # new operation_rate
        for operation in self._operation_rate:
            self._operation_rate[operation] = int(math.floor(self._population_size * self._operation_rate[operation]/total_rate))
            while self._operation_rate[operation] % len(self._benchmark_list) > 0:
                self._operation_rate[operation] += 1
            new_total_rate += self._operation_rate[operation]
        # new elitism_rate
        self._elitism_rate = int(math.floor(self._population_size * self._elitism_rate/total_rate))
        while self._elitism_rate % len(self._benchmark_list) > 0:
            self._elitism_rate += 1
        new_total_rate += self._elitism_rate
        # new new_rate
        self._new_rate = int(self._population_size - new_total_rate)

    def execute(self):
        # first population
        self._population = []
        for gene in self.initialize_population():
            self._population.append({'gene':gene})
        self._completing_population()
        while self._epoch < self._max_epoch and not self.convergance():
            # new population
            new_population = []
            for benchmark in self._benchmark_list:
                # elitism
                new_population += self._get_best_individu(int(self._elitism_rate/len(self._benchmark_list)), benchmark)
                # operation
                for operation in self._operation_list:
                    operation_rate = self._operation_rate[operation]
                    operation_func = getattr(self, operation)
                    for i in range(operation_rate):
                        new_population.append({'gene':operation_func(benchmark)})
            # freshly new individu
            for i in range(self._new_rate):
                new_population.append({'gene':self.new_individu()})
            
            self._population = new_population
            self._completing_population()
            if self._verbose:
                self.show_result()
            else:
                print('GENERATION %d' %(self._epoch+1))
            self._epoch += 1
        # adjust self._epoch value
        self._epoch -= 1
        if not self._verbose:
            self.show_result()
        print('TOTAL POSSIBLE SOLUTION EVALUATED : %d' %(len(self._memoized_gene)))        

    def show_result(self, *args, **kwargs):
        ''' to be overridden by user
        '''
        print('\nGENERATION %d' %(self._epoch+1))
        variation = self.individu_variation()
        print('VARIATION : %d\n' %(variation))
        for benchmark in self._benchmark_list:
            individu = self._population_sorted[benchmark][0]
            print('  BENCHMARK    : %s' %(benchmark))
            print('  BEST GENE    : %s' %(str(individu['gene'])))
            print('  BEST FITNESS : %f' %(individu['fitness'][benchmark]))

    def individu_variation(self):
        unique_gene = []
        for individu in self._population:
            if individu['gene'] not in unique_gene:
                unique_gene.append(individu['gene'])
        variation = len(unique_gene)
        return variation

    def convergance(self):
        return self.individu_variation() < 0.5 * self._population_size

    def _get_best_individu(self, count, benchmark):
        return self._population_sorted[benchmark][:count]

    def _completing_population(self):
        ''' This method should be called everytime a population created
        '''
        # calculate fitness for each individu
        for individu in self._population:
            gene = individu['gene']
            if gene in self._memoized_gene:
                index = self._memoized_gene.index(gene)
                fitness_dict = self._memoized_fitness[index]
            else:
                fitness_dict = {}
                for benchmark in self._benchmark_list:
                    calculated_fitness = self.calculate_fitness(gene, benchmark)
                    fitness_dict[benchmark] = calculated_fitness if calculated_fitness > 0 else 0.001
                self._memoized_gene.append(gene)
                self._memoized_fitness.append(fitness_dict)
            individu['fitness'] = fitness_dict
        # calculate accumulation for each individu
        for benchmark in self._benchmark_list:
            total_fitness = reduce(lambda x,y:x+y['fitness'][benchmark], self._population, 0)
            self._population = sorted(self._population, key=lambda x: x['fitness'][benchmark]*-1)
            accumulation = 0
            for individu in self._population:
                if 'accumulation' not in individu:
                    individu['accumulation'] = {}
                accumulation += individu['fitness'][benchmark] * 1000.0 / total_fitness
                individu['accumulation'][benchmark] = accumulation
        # add to sorted
        for benchmark in self._benchmark_list:
            self._population_sorted[benchmark] = sorted(self._population, key=lambda x: x['fitness'][benchmark]*-1)
        # add to generation
        self._generation.append(self._population)
        self._generation_sorted.append(self._population_sorted)

    def calculate_fitness(self, gene, benchmark):
        ''' To be overridden by user 
        '''
        if benchmark == 'fitness':
            fitness = reduce(lambda x,y:int(x)+int(y), gene, 0)
            return fitness
        return None

    def initialize_population(self):
        gene_list = []
        while len(gene_list) < self._population_size:
            gene = self.new_individu()
            attempt = 0
            while attempt < 100 and gene in gene_list:
                gene = self.new_individu()
                attempt += 1;
            gene_list.append(gene)
        return gene_list

    def new_individu(self):
        ''' To be overridden by user
        '''
        gene = ''
        for i in xrange(self._gene_size):
            gene += str(random.randrange(2))
        attempt = 0
        while attempt<20 and gene in self._memoized_gene:
            gene = ''
            for i in xrange(self._gene_size):
                gene += str(random.randrange(2))
            attempt += 1
        return gene

    def mutation(self, benchmark):
        ''' To be overridden by user
        '''
        # select gene to be mutated
        number = random.randrange(1000)
        selected_gene = ''
        for individu in self._population_sorted[benchmark]:
            if selected_gene == '' and individu['accumulation'][benchmark] > number:
                selected_gene = individu['gene']
                break
        number = random.randrange(self._gene_size)
        # mutation
        new_gene = ''
        for i in range(len(selected_gene)):
            if i == number:
                new_gene += '1' if selected_gene[number] == 0 else '0'
            else:
                new_gene += selected_gene[number]
        return new_gene

    def crossover(self, benchmark):
        ''' To be overridden by user
        '''
        # select genes to be crossovered
        number_1 = random.randrange(1000)
        number_2 = random.randrange(1000)
        selected_gene_1 = ''
        selected_gene_2 = ''
        for individu in self._population_sorted[benchmark]:
            if selected_gene_1 == '' and individu['accumulation'][benchmark] > number_1:
                selected_gene_1 = individu['gene']
            if selected_gene_2 == '' and individu['accumulation'][benchmark] > number_2:
                selected_gene_2 = individu['gene']
            if selected_gene_1 != '' and selected_gene_2 != '':
                break
        number = random.randrange(self._gene_size)
        # crossover
        new_gene = selected_gene_1[:number] + selected_gene_2[number:]
        return new_gene
