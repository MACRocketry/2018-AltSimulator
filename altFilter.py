'''
Altitude Filter
By: Matthew D'Alessandro

matplotlib must be installed 
'''

import csv  #imports native csv library to access data
import random  #imports native ranom library to genenrate random error
import matplotlib.pyplot as plt  #library which generates plots
import statistics as st #native library to calculate stats quickly

def readCSV(filename):
    '''
    Description: Pulls the first column of data from a csv file.  The column must not have any titles
    Inputs: Only the filename is required as a string in the form "filename.csv"
    Outputs: Returns the information in a list where the first entry is in data[0][0] and the second entry is in data[0][1]
    '''
    ifile = open(filename, "rU")
    reader = csv.reader(ifile, delimiter=";")
    rownum = 0
    data=[]
    for row in reader:
        data.append(row)
        rownum += 1
    ifile.close()
    return data

def createError(data, timeData):
    '''
    Description: Adds +/- 10% error to every data point in a list as well as formatting the data into one list from the previous format from readCSV()
    Inputs: Requires the altitude data and time data from the readCSV function
    Outputs: Returns the true altitude, altitude, and time all in lists inside of a single list, these can be seperated by altTrue = info[0], alt = info[1], time = info[2]
    '''
    altTrue = []
    alt = []
    time = []
    rownum = 0
    for entry in data:
        percError = random.randint(-100,100)/1000
        current = float(data[rownum][0])
        curwe = current + percError*current
        alt.append(curwe)
        altTrue.append(current)
        time.append(float(timeData[rownum][0]))
        rownum += 1
    return altTrue, alt, time

def plot1(x,y1,title,xtit,ytit):
    '''
    Description: Generates a scatter plot from a given (x, y) dataset as a list and a title, x label, and y label as strings
    Inputs: Requires x data and y data given each in a seperate list, followed by a title, x label, and y label as individual strings
    Outputs: Does not return anything, instead generates a plot that halts the program until the plot is closed manually
    '''
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.scatter(x, y1, s=10, c='b', marker="s", label='Dataset 1')
    ax1.set_xlabel(xtit)
    ax1.set_ylabel(ytit)
    ax1.set_title(title)
    plt.show()

def plot3(time, y1, y2, y3):
    '''
    Description: Generates a scatter plot from three given (x, y1), (x, y2), (x, y3) datasets, note the first y set will be printed to screen first
    Inputs: Requires x data followed by the three y datasets all in lists
    Outputs: Does not return anything, instead generates a plot that halts the program until the plot is closed manually
    '''
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.scatter(time, y1, s=10, c='b', marker="s", label='Altitude with Error')
    ax1.scatter(time, y2, s=10, c='r', marker="o", label='Filtered')
    ax1.scatter(time, y3, s=5, c='g', marker="o", label='True Altitude from Simulation')
    plt.legend(loc='upper right');
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Altitude (m)")
    ax1.set_title("Altitude over Time")
    plt.show()

def altFilter(alt, time, omega):
    '''
    Description: Filters out error by predicting the next step and weighting that prediction by a given omega value (0 -> 1)
    Inputs: Requires altitude data and time dat given in lists as well as a value for omega in range [0,1]
    Outputs: Returns a filtered list of altitude points
    '''
    cp = 0
    cv = 0
    ca = 0
    lp = 0
    lv = 0
    la = 0
    lt = 0
    dt = 1
    entry = 0
    filtered = []
    for i in alt:
        prediction = cp + dt*cv
        cp = alt[entry]
        ct = time[entry]
        dt = ct - lt
        if dt == 0:
            dt = 0.005
        cv = ((cp - lp) / dt) * (1 - omega) + lv * omega
        ca = ((cv - lv) / dt) * (1-omega) + la * omega
        updated = ((1-omega) * cp) + (omega * prediction)
        filtered.append(updated)
        lp = cp
        lv = cv
        la = ca
        lt = ct
        entry = entry + 1
    return filtered

def avgError(l1, l2):
    '''
    Description: Returns a list of the delta between two lists on an entry to entry level
    Inputs: Two lists where len(l1) < len(l2)
    Outputs: A list of all deltas
    '''
    l3 = []
    c = 0
    for i in l1:
        l3.append(abs(l1[c]-l2[c]))
        c = c + 1
    return l3

def runTheFilter(omega):
    '''
    Description: Generates error, and then runs the filter for a given omega value and returns the error reduction percentage
    Inputs: A value of omega in range [0,1]
    Outputs: Error reduction value in percentage
    '''
    info = createError(data, timeData)
    altTrue = info[0]
    alt = info[1]
    time = info[2]
    filtered = altFilter(alt, time, omega)
    error = st.mean(avgError(alt, altTrue))
    filterError = st.mean(avgError(filtered, altTrue))
    errorReduction = (error-filterError)/error * 100
    return errorReduction

def plotTheFilter(omega):
    '''
    Description: Runs the filter a single time as well as generates a plot of the data
    Inputs: Only requires a a value for omega in range [0,1]
    Outputs: Returns a plot that halts program until manually closed and then returns the error reduction
    '''
    info = createError(data, timeData)
    altTrue = info[0]
    alt = info[1]
    time = info[2]
    filtered = altFilter(alt, time, omega)
    error = st.mean(avgError(alt, altTrue))
    filterError = st.mean(avgError(filtered, altTrue))
    errorReduction = (error-filterError)/error
    plot3(time, alt, filtered, altTrue)
    return errorReduction

def optimize(points):
    '''
    Description: Runs the filter cycling omega from 0 to 1 given x number of points
    Inputs: A positive integer value of points
    Outputs: A list with column 1 containing the omega value and column 2 containing the error reduction for the given omega
    '''
    omegaValue = []
    errorReduction = []
    for i in range(points):
        omega = i/points
        print(omega)
        error = runTheFilter(omega)
        omegaValue.append(omega)
        errorReduction.append(error)
    plot1(omegaValue, errorReduction, "Error Reduction by Omega", "Omega", "Error Reduction (%)")
    return(omegaValue, errorReduction)

def maximize(info):
    '''
    Description: Returns the maximum error reduction as well as omega value when you pass it the optimize() function
    Inputs: The optimize function
    Outputs: Maximum erro reduction with associated omega value
    '''
    maxValue = 0
    index = 0
    c = 0
    for error in info[1]:
        if error > maxValue:
            maxValue = error
            index = c
        c = c + 1
    return maxValue, info[0][index]

data = readCSV("altData.csv")
timeData = readCSV("timeData.csv")


