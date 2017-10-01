import numpy as np
import matplotlib.pyplot as plt
import os

def plotResults(xValues, yValues, version):
    
    #Assignment counts < 10000
    x_normal = []
    y_normal = []

    #Assignment counts > 10000
    x_large = []
    y_large = []

    print('Plotting %d data points' % len(yValues))
    for i in range(len(yValues)):
        if yValues[i] < 10000:
            x_normal.append(xValues[i])
            y_normal.append(yValues[i])
        else:
            x_large.append(xValues[i])
            y_large.append(yValues[i]/10000)
        
    normalPlot = plt.scatter(x_normal, y_normal)
    largePlot = plt.scatter(x_large, [10000]*len(x_large) )
    print(y_large)
    plt.xlabel('# of initial values')
    plt.ylabel('Avg # of assignments')
    plt.legend((normalPlot, largePlot),
               ('< 10000 assignments', '> 10000 assignments'),)
    if version == 'v1':
        plt.title('Standard backtracking')
    elif version == 'v2':
        plt.title('Standard backtracking with forward checking')
    elif version == 'v3':
        plt.title('Standard backtracking with forward checking and heuristics')
    plt.show()


def getResults(outputRootDirectory, version):
    x = []
    y = []
    for root, dirs, files in os.walk(outputRootDirectory):
        for directory in dirs:
            x.append(int(directory))
            outputDirectory = os.path.join(outputRootDirectory, directory)
            y_sum = 0
            overshootCount = 0
            for file in os.listdir(outputDirectory):
                if file.endswith(".txt") and 'count_' + version in file:
                    fullFilePath = os.path.join(os.path.join(outputRootDirectory, directory), file)
                    with open(fullFilePath, 'r') as f:
                        yValue = int(f.readline())
                        if (yValue > 10000):
                            overshootCount += 1
                            print('Crossed 10000 steps for # initial values ' + directory)
                        else: y_sum += yValue
            if overshootCount > 5:
                y.append(overshootCount * 10000)
            else:
                y_avg = y_sum / (10 - overshootCount)
                y.append(y_avg)

    return x,y


if __name__ == '__main__':
    version = 'v3'
    xs,ys = getResults('/Users/apple/Documents/git-repos/sudoku/Run2/constraint-satisfaction-problem-solver/output-data', version)
    plotResults(xs, ys, version)
