'''
Altitude Filter
By: Matthew D'Alessandro
This is a fork
'''

import csv
import random
import matplotlib.pyplot as plt
import statistics as st

def readCSV(filename):
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

def plot1(x,y1):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.scatter(x, y1, s=10, c='b', marker="s", label='Altitude with error')
    ax1.set_xlabel("Omega")
    ax1.set_ylabel("Error Reduction (%)")
    ax1.set_title("Error Reduction from Filter")
    plt.show()

def plot2(time,y2,y1):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.scatter(time, y1, s=10, c='b', marker="s", label='Altitude with error')
    ax1.scatter(time, y2, s=10, c='r', marker="o", label='Filtered')

    plt.legend(loc='upper right');
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Altitude (m)")
    ax1.set_title("Altitude over Time")
    plt.show()

def altFilter(alt, time, omega):
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
    l3 = []
    c = 0
    for i in l1:
        l3.append(abs(l1[c]-l2[c]))
        c = c + 1
    return l3

def runTheFilter(omega):
    info = createError(data, timeData)
    altTrue = info[0]
    alt = info[1]
    time = info[2]
    filtered = altFilter(alt, time, omega)
    error = st.mean(avgError(alt, altTrue))
    filterError = st.mean(avgError(filtered, altTrue))
    errorReduction = (error-filterError)/error
    #plot2(time, alt, filtered)
    return errorReduction

def plotTheFilter(omega):
    info = createError(data, timeData)
    altTrue = info[0]
    alt = info[1]
    time = info[2]
    filtered = altFilter(alt, time, omega)
    error = st.mean(avgError(alt, altTrue))
    filterError = st.mean(avgError(filtered, altTrue))
    errorReduction = (error-filterError)/error
    plot2(time, altTrue, filtered)
    return errorReduction

def optimize(points):
    omegaValue = []
    errorReduction = []
    for i in range(points):
        omega = i/points
        #print(omega)
        error = runTheFilter(omega)
        omegaValue.append(omega)
        errorReduction.append(error)
    plot1(omegaValue,errorReduction)
    return(omegaValue, errorReduction)

def maximize(info):
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
































