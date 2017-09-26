import numpy as np

class SudokuGrid:

    def __init__(self, inputFile):
        self.grid = np.zeros([9, 9], dtype=int)
        f = open(inputFile, 'r') 
        lines = f.readlines()
        f.close()
        
        if len(lines) < 9:
            raise ValueError("The format of input data is not correct")

        for i in range(9):
            columnValues = lines[i].rstrip().split(' ')
            if len(columnValues) != 9:
                raise ValueError("The format of input data is not correct")
            self.grid[i] = columnValues
            

    def print(self):
        print('\n'.join('  '.join(str(cell) for cell in row) for row in self.grid))

    def setValue(self, value, row, col):
        self.grid[row-1][col-1] = value
    
    def valueAt(self, row, col):
        return self.grid[row-1, col-1]

    def convert(self, outputFormat='list'):
        if outputFormat == 'list':
            return list(self.grid.flatten())



if __name__ == '__main__':
    sudokuGrid = SudokuGrid('/Users/apple/Documents/git-repos/sudoku/sudoku-as-csp/input-data/18/4.sd')

    #Test print() 
    sudokuGrid.print()

    #Test valueAt() 
    print(sudokuGrid.valueAt(3, 4))

    #Test setValue() 
    sudokuGrid.setValue(99, 3, 4)
    print(sudokuGrid.valueAt(3, 4))

    #Test convert()
    print(sudokuGrid.convert())    
