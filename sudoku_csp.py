from variable import Variable
from sudoku_grid import SudokuGrid
import math

class SudokuCSP():
    """Class representing Sudoku as a Constraint Satisfaction Problem. Includes utility functions for CSP operations. Contains:
       1. variables - a list of 81 variables (type Variable) of the Sudoku CSP
       2. currentAssignment - comma-seperated current values of all the variable
       3. assignmentCounter - keeps track of the number of assigments to each variable(or a sudoku cell)
    """

    def __init__(self):
        self.variables = []
        self.currentAssignment = None
        self.assignmentCounter = 0

    def reset(self, assignmentList):
        """Performs a reloading of the variable values and its domain from an assignment list of 81 values"""
        if len(assignmentList) != 81:
            print('Not enough values to initialise')
            return

        self.variables = []
        #Initialise all the 81 variables
        for i in range(81):
            varName = str(i+1) #variables are named 1 to 81 for convenience
            varDomain = []
            varValue = assignmentList[i]
            if varValue == '0':
                varDomain = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
            var = Variable(varName, varDomain, varValue)
            self.variables.append(var)

        #Current assignment is stored as a string of comma seperated values
        self.currentAssignment = ','.join(assignmentList)
        self.setDomains()

    def setDomains(self):        
        for i in range(81):
            if self.variables[i].isAssigned == False:
                allNeighbours = self.getRowNeighbours(self.variables[i]) + \
                                self.getColumnNeighbours(self.variables[i]) + \
                                self.getBoxNeighbours(self.variables[i])
                for neighbour in allNeighbours:
                    if neighbour.isAssigned == True:
                        self.variables[i].removeFromDomain(neighbour.getValue())

    def getCurrentAssignment(self):
        return self.currentAssignment

    def getAssignmentCount(self):
       return self.assignmentCounter
    
    def getVariable(self, variableName):
        """return the Variable object given the variable name"""
        for i in range(len(self.variables)):
            if self.variables[i].getName() == variableName:
                return self.variables[i]
        return None

    def selectUnassignedVariable(self, mrvHeuristic=False, maxDegreeHeuristic=False):
        """Returns the next variable to be assigned based on the policy"""
        if mrvHeuristic == False:
            #'standard-backtrack' returns the variables in order
            for variable in self.variables:
                if not variable.isAssigned:
                    return variable
            return None
        elif mrvHeuristic == True:
            minDomainValues = 10
            minVariablesList = []
            for variable in self.variables:
                if not variable.isAssigned:
                   if len(variable.getDomain()) < minDomainValues:
                        minDomainValues = len(variable.getDomain())
                        minVariablesList.clear()
                        minVariablesList.append(variable)
                   elif len(variable.getDomain()) == minDomainValues:
                        minVariablesList.append(variable)
            if len(minVariablesList) > 1 and maxDegreeHeuristic == True:
                maxDegree = -1
                maxDegreeVariablesList = []
                for v in minVariablesList:
                    if self.getUnassignedNeighboursCount(v) > maxDegree:
                        maxDegree = self.getUnassignedNeighboursCount(v)
                        maxDegreeVariablesList.clear()
                        maxDegreeVariablesList.append(v)
                    elif self.getUnassignedNeighboursCount(v) == maxDegree:
                        maxDegreeVariablesList.append(v)
                return maxDegreeVariablesList[0]
            else:     
                if minVariablesList: return minVariablesList[0]
            return None

    def orderDomainValues(self, variable, lcvHeuristic=False):
        """Returns the domain values of the variable. Order of the variables depends on the policy"""
        domainValues = []
        if lcvHeuristic == True and len(variable.getDomain()) > 1:
            #Get All unassigned neighbors of the current variable
            allNeighbours = self.getRowNeighbours(variable) + \
                            self.getColumnNeighbours(variable) + \
                            self.getBoxNeighbours(variable)
            allNeighbours = [v for v in allNeighbours if v.isAssigned == False]

            #For each value, get the number of times it occurs (which is the same as number of times it rules out
            #that value of the neighbour) in the neighbours.
            #And Order them in ascending order
            valueWithReductionsCount = []
            for value in variable.getDomain():
                reductions = 0
                for neighbour in allNeighbours:
                    if value in neighbour.getDomain():
                        reductions += 1
                valueWithReductionsCount.append((value, reductions))
                
                #The value 'value' can be ruled out 'reductions' times from its neighbors 
                valueWithReductionsCount = sorted(valueWithReductionsCount, key=lambda tup: tup[1])
                domainValues = [value for (value,reductions) in valueWithReductionsCount]
        else: 
            #'standard-backtrack' returns the values in sorted order
            domainValues = sorted(variable.getDomain())
        return domainValues

    def applyInferences(self, variable, value, forwardCheck=False):
        if forwardCheck == True:
            #Get the names of all unassigned neighbours
            allNeighbours = self.getRowNeighbours(variable) + \
                            self.getColumnNeighbours(variable) + \
                            self.getBoxNeighbours(variable)
            neighbourNames = []
            for neighbour in allNeighbours:
                if not neighbour.isAssigned:
                    neighbourNames.append(neighbour.getName())

            #Remove the value from the domains of the neighbours
            for i in range(81):
                if self.variables[i].getName() in neighbourNames:
                    self.variables[i].removeFromDomain(value)
                    if len(self.variables[i].getDomain()) == 0:
                        return False
        return True

    def reverseInferences(self, variable, value, forwardCheck=False):
        if forwardCheck == True:
            #Get the names of all unassigned neighbours
            allNeighbours = self.getRowNeighbours(variable) + \
                            self.getColumnNeighbours(variable) + \
                            self.getBoxNeighbours(variable)
            neighbourNames = []
            for neighbour in allNeighbours:
                if not neighbour.isAssigned:
                    neighbourNames.append(neighbour.getName)

            #Add the value back to the domains of unassigned neighbours
            for i in range(81):
                if self.variables[i].getName() in neighbourNames:
                    self.variables[i].addToDomain(value)
    
    def getUnassignedCount(self):
        """Returns the count of remaining unassigned variables"""
        count = 0
        for variable in self.variables:
            if not variable.isAssigned: count += 1
        return count
            
    def isAssignmentComplete(self):
        #Assignment is complete when there are no more variables to assign
        return self.selectUnassignedVariable() == None
    
    def isAllDiff(self, valuesList):
        """Utility function for evaluating the AllDiff constraint. Returns true if all the values in valuesList are different"""
        valuesList = list(filter(lambda value: value != '0', valuesList))
        return len(valuesList) == len(set(valuesList))

    def assign(self, variable, value):
        """Assign value to the variable """
        success = variable.assign(value)
        for i in range(81):
            if self.variables[i].getName() == variable.getName():
                self.variables[i] = variable
        if success:
            self.assignmentCounter += 1

        #update the current assignment
        self.currentAssignment = ','.join([v.getValue() for v in self.variables])

    def unAssign(self, variable, value):
        """For undoing the assignment of value to variable"""
        for i in range(81):
            if self.variables[i].getName() == variable.getName():
                self.variables[i].unAssign(value)
        
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
        """Returns true if 2 variables given their position (from 1 to 81) belongs to same 3X3 box"""
        return math.ceil(position1 / 27) == math.ceil(position2 / 27) and \
           math.ceil((position1 % 9) / 3) == math.ceil((position2 % 9) / 3)
    
    def getBoxNeighbours(self, variable):
        varNumber = int(variable.getName())
        boxNeighbours = []

        for v in self.variables:
            if self.isInSameBox(varNumber, int(v.getName())) and v.getName() != variable.getName():
                boxNeighbours.append(v)

        return boxNeighbours

    def getUnassignedNeighboursCount(self, variable):
        count = 0
        allNeighbours = self.getRowNeighbours(variable) + \
                        self.getColumnNeighbours(variable) + \
                        self.getBoxNeighbours(variable)

        for neighbour in allNeighbours:
            if neighbour.isAssigned == False:
                count += 1
        return count
        
    def isConstraintsSatisfied(self, variable, value):
        """Evaluates the 3 AllDiff constraints after the assignment of value to variable"""
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

    def print(self, file=None):
        """Print the assignment list as a sudoku grid"""
        listOfValues = self.currentAssignment.split(',')
        for i in range(81):
            print(listOfValues[i], end='  ', file=file)
            if(i % 9 == 8):print(file=file)

if __name__ == '__main__':
    sudokuGrid = SudokuGrid('/Users/apple/Documents/git-repos/sudoku/sudoku-as-csp/input-data/18/4.sd')
    sudokuGrid.print()
    print(sudokuGrid.convert())
    csp = SudokuCSP()
    csp.reset(sudokuGrid.convert())
    print('Current Assignment:', end=' ')
    print(csp.getCurrentAssignment())
    print('The Row Neighbours of var:')
    testVar = csp.getVariable('4')
    testVar.print()
    print('variable value ' + testVar.getValue())
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
    print('The domain of %s is:' % testVar.getName(), end=' ')
    print(testVar.getDomain())
