from gogenpy import GA, random
import sys
if sys.version_info >= (3,0,0):
    xrange = range

'''
Find the minimum number of queens needed to occupy or attack all squares.
Please take a look at http://mathworld.wolfram.com/QueensProblem.html for more information.
'''

class GA_N_Queen(GA):
    '''Demo to solve chess rock problem
    '''
    def __init__(self, *args, **kwargs):
        GA.__init__(self, *args, **kwargs)
        self._board_size = kwargs.pop('board_size',5)
        self._gene_size = self._board_size ** 2
        # queen basic movement
        movement_pattern_list = (
            ( 0, 0),         # current position
            ( 1, 0),(-1, 0), # horizontal
            ( 0, 1),( 0,-1), # vertical
            (-1,-1),( 1, 1), # diagonal (left top - right bottom)
            (-1, 1),( 1,-1), # diagonal (left bottom - right top)
        )
        # queen has no limit
        movement_list = []
        for i in range(1,self._board_size):
            for  movement_pattern in movement_pattern_list:
                row, col = movement_pattern
                row *= i
                col *= i
                if [row, col] not in movement_list:
                    movement_list.append([row, col])
        self.movement_list = movement_list

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

    # we have different fitness measurement
    def calculate_fitness(self,gene,benchmark):
        uncovered_count, overlapped_count, queen_count = self.measurement(gene)
        fitness = ((self._gene_size ** 3) - (uncovered_count * self._gene_size ** 2)) +\
            ((self._gene_size ** 2) - (queen_count * self._gene_size)) +\
            ((self._gene_size - overlapped_count))
        return fitness

    def measurement(self, gene):
        queen_count = 0
        overlapped_count = 0
        uncovered_count = 0
        # calculate how many queens (it must be as few as possible)
        # calculate how many cell doesn't covered (it must be as few as possible)
        # calculate how many overlapped queen (it must be as few as possible)
        for i in range(self._gene_size):
            if gene[i] == '1':
                queen_count += 1
            row = i / self._board_size
            col = i % self._board_size
            covered = False
            for movement in self.movement_list:
                delta_row = movement[0]
                delta_col = movement[1]
                new_row = row + delta_row
                # out of board, ignore
                if new_row<0 or new_row >= self._board_size:
                    continue
                new_col = col + delta_col
                # out of board, ignore
                if new_col<0 or new_col >= self._board_size:
                    continue
                # don't include itself
                if new_row != row or new_col != col:
                    new_index = new_row * self._board_size + new_col
                    # this is queen, and other is also queen
                    if gene[new_index] == '1' and gene[i] == '1':
                        overlapped_count += 1
                    # this is not queen, but there is queen in line or diagonal
                    if not covered and (gene[i] == '1' or (gene[new_index] == '1' and gene[i] == '0')):
                        covered = True
            if not covered:
                uncovered_count += 1
        return (uncovered_count, overlapped_count, queen_count)


    def show_result(self, *args, **kwargs):
        print('\nGENERATION %d' %(self._epoch+1))
        variation = self.individu_variation()
        print('VARIATION : %d\n' %(variation))
        for benchmark in self._benchmark_list:
            individu = self._population_sorted[benchmark][0]
            uncovered_count, overlapped_count, queen_count = self.measurement(individu['gene'])
            print('  BENCHMARK    : %s' %(benchmark))
            print('  BEST GENE    : %s' %(str(individu['gene'])))
            print('  BEST FITNESS : %f' %(individu['fitness'][benchmark]))
            print('  QUEEN COUNT  : %d' %(queen_count))
            print('  UNCOVERED    : %d' %(uncovered_count))
            print('  OVERLAPPED   : %d' %(overlapped_count))
            print('  FORMATION    :')
            for i in range(self._board_size):
                chunk = individu['gene'][i*self._board_size:(i+1)*self._board_size]
                chunk = chunk.replace('0','x').replace('1','*')
                print('    %s' %(chunk))

        
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
ga.execute()