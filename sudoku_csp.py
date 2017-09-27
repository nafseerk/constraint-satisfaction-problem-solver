from csp import CSP
from variable import Variable
from sudoku_grid import SudokuGrid
import math

class SudokuCSP(CSP):

    def __init__(self):

        #List of Variable object - the variable object has all details relevant to a variable
        self.variables = []

        #Initialise with domain (1, 2,.....,9) for all variables
        self.domains = []
        domain = set(range(1, 10))
        for i in range(81):
            self.domains.append(domain)

        self.currentAssignment = None

        self.assignmentCounter = 0

    def initialise(self, startingAssignmentList):
        if len(startingAssignmentList) != 81:
            print('Not enough values to initialise')
            return

        self.variables = []
        #Initialise all the 81 variables
        for i in range(81):
            varName = str(i+1) #variables are named 1 to 81 for convenience
            varDomain = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
            varValue = startingAssignmentList[i]
            var = Variable(varName, varDomain, varValue)
            self.variables.append(var)

        #Current assignment is stored as a string of comma seperated values
        self.currentAssignment = ','.join(startingAssignmentList)

    def getVariable(self, variableName):
        for i in range(len(self.variables)):
            if self.variables[i].getName() == variableName:
                return self.variables[i]
        return None

    def selectUnassignedVariable(self, policy='inorder'):
        if policy == 'inorder':
            for variable in self.variables:
                if not variable.isAssigned:
                    return variable
            return None

    def getUnassignedCount(self):
        count = 0
        for variable in self.variables:
            if not variable.isAssigned: count += 1
        return count
            
        
    def isAssignmentComplete(self):
        #Assignment is complete when there are no more variables to assign
        return self.selectUnassignedVariable() == None

    def orderDomainValues(self, variable, policy='inorder'):
        domainValues = []
        if policy == 'inorder':
            domainValues = sorted(variable.getDomain())
        return domainValues
    
    def isAllDiff(self, valuesList):
        valuesList = list(filter(lambda value: value != '0', valuesList))
        return len(valuesList) == len(set(valuesList))

    def assign(self, variable, value):
        #print('Calling assign on variable %s with value %s' % (variable.getName(), value))
        success = variable.assign(value)
        for i in range(81):
            if self.variables[i].getName() == variable.getName():
                self.variables[i] = variable
        if success:
            self.assignmentCounter += 1

        self.currentAssignment = ','.join([v.getValue() for v in self.variables])
        #print('Inside assign with new assignment becomes %s' % self.currentAssignment)

    def getAssignmentCount(self):
       return self.assignmentCounter

    def getColumnNeighbours(self, variable):
        varNumber = int(variable.getName())
        colNeighbours = []
       
        for v in self.variables:
            if (abs(varNumber - int(v.getName())) % 9 == 0) and v.getName() != variable.getName():
                colNeighbours.append(v)

        return colNeighbours

    def getRowNeighbours(self, variable):
        varNumber = int(variable.getName())
        rowNeighbors = []

        #Calculate the starting and ending positions of that row
        rowStart = rowEnd = varNumber
        if varNumber % 9 == 0:
            rowStart = ((int(varNumber/9)) - 1) * 9 + 1
        else:
            rowStart = math.floor(varNumber/9) * 9 + 1
            rowEnd = math.ceil(varNumber/9) * 9
            
        for v in self.variables:
            if int(v.getName()) in range(rowStart, rowEnd + 1) and v.getName() != variable.getName():
                rowNeighbors.append(v)

        return rowNeighbors

    def isInSameBox(self, position1, position2):
        return math.ceil(position1 / 27) == math.ceil(position2 / 27) and \
           math.ceil((position1 % 9) / 3) == math.ceil((position2 % 9) / 3)
        
    
    def getBoxNeighbours(self, variable):
        varNumber = int(variable.getName())
        boxNeighbours = []

        for v in self.variables:
            if self.isInSameBox(varNumber, int(v.getName())) and v.getName() != variable.getName():
                boxNeighbours.append(v)

        return boxNeighbours

    def isConstraintsSatisfied(self, variable, value):

        rowNeighbours = self.getRowNeighbours(variable)
        rowValues = [neighbour.getValue() for neighbour in rowNeighbours]
        rowValues.append(value)
        rowConstraintSatisfied = self.isAllDiff(rowValues)                       
        
        colNeighbours = self.getColumnNeighbours(variable)
        colValues = [neighbour.getValue() for neighbour in colNeighbours]
        colValues.append(value)
        colConstraintSatisfied = self.isAllDiff(colValues)
        
        boxNeighbours = self.getBoxNeighbours(variable)
        boxValues = [neighbour.getValue() for neighbour in boxNeighbours]
        boxValues.append(value)
        boxConstraintSatisfied = self.isAllDiff(boxValues)

        return rowConstraintSatisfied and colConstraintSatisfied and boxConstraintSatisfied

    def getCurrentAssignment(self):
        return self.currentAssignment

    def print(self):
        listOfValues = self.currentAssignment.split(',')
        for i in range(81):
            print(listOfValues[i], end='  ')
            if(i % 9 == 8):print()

if __name__ == '__main__':
    sudokuGrid = SudokuGrid('/Users/apple/Documents/git-repos/sudoku/sudoku-as-csp/input-data/18/4.sd')
    sudokuGrid.print()
    print(sudokuGrid.convert())
    csp = SudokuCSP()
    csp.initialise(sudokuGrid.convert())
    print('Current Assignment:', end=' ')
    print(csp.getCurrentAssignment())
    print('The Row Neighbours of var:')
    testVar = csp.getVariable('4')
    print(testVar.getValue())
    for var in csp.getRowNeighbours(testVar):
        print(var.getName(), end=' ')
    print()
    print('The Column Neighbours of var:')
    for var in csp.getColumnNeighbours(testVar):
        print(var.getName(), end=' ')
    print()
    print('The Box Neighbours of var :')
    for var in csp.getBoxNeighbours(testVar):
        print(var.getName(), end=' ')
    print()    
    print(csp.isConstraintsSatisfied(testVar, '9'))
    print(csp.orderDomainValues(testVar))
    csp.print()
