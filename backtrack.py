from sudoku_csp import SudokuCSP
from variable import Variable
from sudoku_grid import SudokuGrid

def backtrackSearch(csp):
    initialAssignment = csp.getCurrentAssignment()
    assignmentForVariables = []
    backtrack(csp)
    assignmentForVariables = csp.getCurrentAssignment().split(',')
    if csp.getAssignmentCount() > 10000:
        print('\nFailed: bactrack search took more than 10000 steps')
    else:
        print('\nSuccess: Solution found in %d steps' % csp.getAssignmentCount())
    return assignmentForVariables
    

def backtrack(csp):
    
    #Check if CSP is solved
    currentAssingment = csp.getCurrentAssignment()
    if csp.isAssignmentComplete() == True:
        return True

    nextVariable = csp.selectUnassignedVariable()
    domainValues = csp.orderDomainValues(nextVariable)
    for value in domainValues:
        csp.assign(nextVariable, value)
        newAssignment = csp.getCurrentAssignment()
        if csp.isConstraintsSatisfied(nextVariable, value) == True:
            result = backtrack(csp)
            if result != False: return result
        else:
            csp.initialise(currentAssingment.split(','))
    return False


if __name__ == '__main__':
    sudokuGrid = SudokuGrid('/Users/apple/Documents/git-repos/sudoku/sudoku-as-csp/input-data/1/8.sd')
    csp = SudokuCSP()
    csp.initialise(sudokuGrid.convert())
    print(5*'=' + 'Question Sudoku' + 5*'=')
    csp.print()
    
    finalAssignment = backtrackSearch(csp)
    print('\n\n' +5*'=' + 'Solved Sudoku' + 5*'=')
    csp.print()
    
