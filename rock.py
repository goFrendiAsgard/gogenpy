from gogenpy import Gogenpy
class GA(Gogenpy):
    '''Demo to solve chess rock problem
    '''
    def __init__(self, *args, **kwargs):
        Gogenpy.__init__(self, *args, **kwargs)
        self._board_size = 5
        self._gene_size = self._board_size ** 2

    # we have different fitness measurement
    def calculate_fitness(self,gene,benchmark):
        uncovered_count, overlapped_count, one_count = self.measurement(gene)
        fitness = ((self._gene_size ** 3) - (uncovered_count * self._gene_size ** 2)) +\
            ((self._gene_size ** 2) - (overlapped_count * self._gene_size)) +\
            ((self._gene_size - one_count))
        return fitness

    def measurement(self, gene):
        # calculate how many ones (it must be as few as possible)
        one_count = 0
        for i in range(self._gene_size):
            if gene[i] == '1':
                one_count += 1
        overlapped_count = 0
        uncovered_count = 0
        # calculate how many cell doesn't covered (it must be as few as possible)
        # calculate how many overlapped queen (it must be as few as possible)
        for i in range(self._gene_size):
            row = i / self._board_size
            col = i % self._board_size
            covered = False
            if gene[i] == '1': # is rock
                # horizontal
                for other_col in range(self._board_size):
                    if other_col != col and gene[row * self._board_size + other_col] == '1':
                        overlapped_count += 1
                # vertical
                for other_row in range(self._board_size):
                    if other_row != row and gene[other_row * self._board_size + col] == '1':
                        overlapped_count += 1
            # horizontal
            for other_col in range(self._board_size):
                if gene[row * self._board_size + other_col] == '1':
                    covered = True
                    break
            if not covered:
                # vertical
                for other_row in range(self._board_size):
                    if gene[other_row * self._board_size + col] == '1':
                        covered = True
                        break
            if not covered:
                uncovered_count += 1
        return (uncovered_count, overlapped_count, one_count)


    def show_result(self, *args, **kwargs):
        print('\nGENERATION %d' %(self._epoch+1))
        variation = self.individu_variation()
        print('VARIATION : %d\n' %(variation))
        for benchmark in self._benchmark_list:
            individu = self._population_sorted[benchmark][0]
            uncovered_count, overlapped_count, one_count = self.measurement(individu['gene'])
            print('  BENCHMARK    : %s' %(benchmark))
            print('  BEST GENE    : %s' %(str(individu['gene'])))
            print('  BEST FITNESS : %f' %(individu['fitness'][benchmark]))
            print('  ROCK COUNT   : %d' %(one_count))
            print('  UNCOVERED    : %d' %(uncovered_count))
            print('  OVERLAPPED   : %d' %(overlapped_count))
            print('  FORMATION    :')
            for i in range(self._board_size):
                chunk = individu['gene'][i*self._board_size:(i+1)*self._board_size]
                chunk = chunk.replace('0','x').replace('1','*')
                print('    %s' %(chunk))

        
ga = GA(population_size=100, max_epoch=1000)
ga.execute()
ga.show_result()