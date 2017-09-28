from sudoku_csp import SudokuCSP
from variable import Variable
from sudoku_grid import SudokuGrid

def backtrackSearch(csp, forwardCheck=False, mrvHeuristic=False, maxDegreeHeuristic=False):
    initialAssignment = csp.getCurrentAssignment()
    assignmentForVariables = []
    backtrack(csp, forwardCheck=forwardCheck, mrvHeuristic=mrvHeuristic, maxDegreeHeuristic=maxDegreeHeuristic)
    assignmentForVariables = csp.getCurrentAssignment().split(',')
    return assignmentForVariables
    

def backtrack(csp, forwardCheck=False, mrvHeuristic=False, maxDegreeHeuristic=False):
    #Check if CSP is solved
    if csp.isAssignmentComplete() == True:
        return True

    #For reporting the progress of the algorithm
    if csp.getAssignmentCount() % 10000 <= 10:
        print('took %d steps with %d remaining variables' % (csp.getAssignmentCount(), csp.getUnassignedCount()))

    currentAssingment = csp.getCurrentAssignment()
    nextVariable = csp.selectUnassignedVariable(mrvHeuristic=mrvHeuristic, maxDegreeHeuristic=maxDegreeHeuristic)
    domainValues = csp.orderDomainValues(nextVariable)
    for value in domainValues:
        csp.assign(nextVariable, value)
        if csp.isConstraintsSatisfied(nextVariable, value) == True and csp.applyInferences(nextVariable, value, forwardCheck=forwardCheck) == True:
            result = backtrack(csp, forwardCheck=forwardCheck, mrvHeuristic=mrvHeuristic, maxDegreeHeuristic=maxDegreeHeuristic)
            if result != False:
                return result
            else:
                csp.reverseInferences(nextVariable, value, forwardCheck=forwardCheck)
                csp.unAssign(nextVariable, value)
                csp.reset(currentAssingment.split(','))               
        else:
            csp.reverseInferences(nextVariable, value, forwardCheck=forwardCheck)
            csp.unAssign(nextVariable, value)
            csp.reset(currentAssingment.split(','))
    return False


if __name__ == '__main__':
    sudokuGrid = SudokuGrid('/Users/apple/Documents/git-repos/sudoku/sudoku-as-csp/input-data/30/8.sd')
    csp = SudokuCSP()
    csp.reset(sudokuGrid.convert())
    print(5*'=' + 'Question Sudoku' + 5*'=')
    csp.print()
    
    finalAssignment = backtrackSearch(csp, forwardCheck=True, mrvHeuristic=True, maxDegreeHeuristic=True)
    print("\nFound a solution in %d assignments" % csp.getAssignmentCount())
    print('\n\n' +5*'=' + 'Solved Sudoku' + 5*'=')
    csp.print()
    
