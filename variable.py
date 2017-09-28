
class Variable:
    """Class representing a CSP variable with utility functions. Contains:
       1. name - an identifier for the variable (represented as a string)
       2. domain - the domain of the variable
       3. value - the current value of the variable. Value '0' means unassigned variable 
       4. isAssigned - true if the variable is currently assigned. False otherwises
    """

    def __init__(self, name, domain, value='0'):
        self.name = name
        self.value = value
        self.domain = set(domain)
        self.domain.discard(value)
        self.isAssigned = False
        if self.value != '0':
            self.isAssigned = True

    def getName(self):
        return self.name
    
    def getValue(self):
        if not self.isAssigned:
            return '0'
        return self.value

    def getDomain(self):
        return list(self.domain)
       
    def assign(self, value):
        """Assigns value to the variable and returns success/failure"""
        if value not in self.domain:
            print('ERROR! value of the variable not in its domain')
            return False

        self.value = value
        self.domain.discard(value)
        self.isAssigned = True
        return True

    def unAssign(self, value):
        self.value = '0'
        self.isAssigned = False
        self.domain.add(value)
        
    def removeFromDomain(self, value):
        self.domain.discard(value)

    def removeValuesFromDomain(self, valuesList):
        """Remove a set of values from the domain"""
        for value in valuesList:
            self.domain.discard(value)

    def addToDomain(self, value):
        self.domain.add(value)

    def updateDomain(self, domainValuesList):
        """Update the domain of the variable with a new list"""
        self.domain = set(domainValuesList)
        self.value = '0'
        self.isAssigned = False

    def print(self):
        print('variable name = ' + self.name)
        print('domain =', end=' ')
        print(self.domain)
        if self.isAssigned:
            print('assignment = %s' % self.value)
        else:
            print("unassigned")

if __name__ == '__main__':
    var1 = Variable('1', ['1', '2', '3', '4', '5', '6', '7'], '5')
    var1.print()

    print(var1.getValue())

        
