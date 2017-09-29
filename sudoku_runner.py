from sudoku_csp import SudokuCSP
from variable import Variable
from sudoku_grid import SudokuGrid
import backtrack
import os
import shutil


def runOnFile(inputFile, version, outputDirectory):
    #If the sudoku was already solved quit
    filePath = os.path.join(outputDirectory, os.path.splitext(os.path.basename(os.path.normpath(inputFile)))[0])
    solutionFilePath = filePath + '_solution_' + version + '.txt'
    countFilePath = filePath + '_count_' + version + '.txt'
    if os.path.exists(solutionFilePath) and os.path.exists(countFilePath): return

    ##Solve the sudoku and store the solution and assignment count in file
    sudokuGrid = SudokuGrid(inputFile)
    csp = SudokuCSP()
    csp.reset(sudokuGrid.convert())                   
    if version == 'v1':
        backtrack.backtrackSearch(csp)
    elif version == 'v2':
        backtrack.backtrackSearch(csp, forwardCheck=True)
    elif version == 'v3':
        backtrack.backtrackSearch(csp, forwardCheck=True, mrvHeuristic=True, maxDegreeHeuristic=True, lcvHeuristic=True)
    else: return
    
    with open(solutionFilePath, 'w') as f:
        csp.print(file=f)
    with open(countFilePath, 'w') as f:
        print(csp.getAssignmentCount(), file=f)

def runOnDataSet(inputRootDirectory):
    outputRootDirectory = os.path.join(os.path.abspath(os.path.join(inputRootDirectory, os.pardir)), 'output-data')
    if not os.path.exists(outputRootDirectory):
        os.makedirs(outputRootDirectory)

    for root, dirs, files in os.walk(inputRootDirectory):
        for directory in dirs:
            outputDirectory = os.path.join(outputRootDirectory, directory)
            if not os.path.exists(outputDirectory): os.makedirs(outputDirectory)
            for file in os.listdir(os.path.join(inputRootDirectory, directory)):
                if file.endswith(".sd"):
                    fullFilePath = os.path.join(os.path.join(inputRootDirectory, directory), file)
                    csp_versions = ['v1', 'v2', 'v3']
                    for version in csp_versions:
                        print('%s on %s started' % (version, directory+'/'+file))
                        runOnFile(fullFilePath, version, outputDirectory)
                        print('%s on %s complete' % (version, directory+'/'+file))
    
        

runOnDataSet('/Users/apple/Documents/git-repos/sudoku/version3/constraint-satisfaction-problem-solver/input-data')
