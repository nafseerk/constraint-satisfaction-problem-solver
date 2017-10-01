from sudoku_csp import SudokuCSP
from variable import Variable
from sudoku_grid import SudokuGrid

def backtrackSearch(csp, forwardCheck=False, mrvHeuristic=False, maxDegreeHeuristic=False, lcvHeuristic=False):
    initialAssignment = csp.getCurrentAssignment()
    assignmentForVariables = []
    backtrack(csp, forwardCheck=forwardCheck, mrvHeuristic=mrvHeuristic, maxDegreeHeuristic=maxDegreeHeuristic, lcvHeuristic=lcvHeuristic)
    assignmentForVariables = csp.getCurrentAssignment().split(',')
    return assignmentForVariables
    

def backtrack(csp, forwardCheck=False, mrvHeuristic=False, maxDegreeHeuristic=False, lcvHeuristic=False):
    #Check if CSP is solved
    if csp.isAssignmentComplete() == True:
        return True

    #For reporting the progress of the algorithm
    if csp.getAssignmentCount() > 10000:
        print('took %d steps with %d remaining variables...terminating' % (csp.getAssignmentCount(), csp.getUnassignedCount()))
        return True

    currentAssingment = csp.getCurrentAssignment()
    nextVariable = csp.selectUnassignedVariable(mrvHeuristic=mrvHeuristic, maxDegreeHeuristic=maxDegreeHeuristic)
    domainValues = csp.orderDomainValues(nextVariable, lcvHeuristic=lcvHeuristic)
    for value in domainValues:
        csp.assign(nextVariable, value)
        if csp.isConstraintsSatisfied(nextVariable, value) == True and csp.applyInferences(nextVariable, value, forwardCheck=forwardCheck) == True:
            result = backtrack(csp, forwardCheck=forwardCheck, mrvHeuristic=mrvHeuristic, maxDegreeHeuristic=maxDegreeHeuristic, lcvHeuristic=lcvHeuristic)
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
    inputFilePath = '/Users/apple/Documents/git-repos/sudoku/version3/constraint-satisfaction-problem-solver/input-data/65/1.sd'
    sudokuGrid = SudokuGrid(inputFilePath)
    csp = SudokuCSP()
    csp.reset(sudokuGrid.convert())
    print(5*'=' + 'Question Sudoku' + 5*'=')
    csp.print()
    
    finalAssignment = backtrackSearch(csp, forwardCheck=True, mrvHeuristic=True, maxDegreeHeuristic=True, lcvHeuristic=True)
    if csp.getAssignmentCount() > 10000:
        print("\nTook > 10000 steps. No solution found")
    else:
        print("\nFound a solution in %d assignments" % csp.getAssignmentCount())
        print('\n\n' +5*'=' + 'Solved Sudoku' + 5*'=')
        csp.print()
    
