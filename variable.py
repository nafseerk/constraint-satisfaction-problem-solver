
class Variable:

    def __init__(self, name, domain, value='0'):
        self.name = name
        self.domain = set(domain)
        self.isAssigned = False
        if value != '0':
            if value not in domain:
                #print('Variable can only be assigned a value from its domain')
                return
            self.isAssigned = True
        self.value = value
        self.domain.discard(value)
        
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

    #Assigns value to the variable and returns success/failure        
    def assign(self, value):
        if value not in self.domain:
            print('Variable can only be assigned a value from its domain')
            return False

        self.value = value
        self.isAssigned = True
        self.domain.discard(value)
        return True

    def removeFromDomain(self, value):
        self.domain.discard(value)

    def removeValuesFromDomain(self, valuesList):
        for value in valuesList:
            self.domain.discard(value)

    def updateDomain(self, domainValuesList):
        self.domain = set(domainValuesList)
        self.value = None
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

        
