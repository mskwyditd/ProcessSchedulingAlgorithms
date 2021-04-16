

# -1 when list empty
def posOfShortestProcess(lst):
    t = len(lst)
    pos = -1
    tmp = -1
    for i in range(t):
        if tmp > lst[i] or tmp == -1:
            pos = i
            tmp = lst[i]
    return pos


def readProcessesFromFile(inputDir = 'processes.txt'):
    inputFile = open(inputDir, 'rt')
    numbers = []
    arriveTimes = []
    serviceTimes = []
    size = 1
    for li in inputFile:
        line = li.split()
        # if it's rr
        if len(line) == 1:
            line.append(-1)
        arriveTimes.append(int(line[0]))
        serviceTimes.append(int(line[1]))
        numbers.append(size)
        size += 1
    inputFile.close()
    return (numbers, arriveTimes, serviceTimes)


def writeToFile(content = '', outputDir = 'processingResults.txt'):
    outputFile = open(outputDir, 'wt')
    outputFile.write(content)
    outputFile.close()


def transform(lst, countingAverages = False):
    result = ''
    avgService = 0.
    avgTAT = 0.
    avgWAT = 0.

    for i in range(len(lst[0])):
        tmpOutput = ""
        for j in range(len(lst)):
            tmpOutput += (str(lst[j][i]) + ' ')
        tmpOutput = tmpOutput.rstrip(' ') + '\n'
        result += tmpOutput

    if countingAverages:
        for i in range(len(lst[0])):
            avgService += lst[2][i]
            avgTAT += lst[5][i]
            avgWAT += lst[6][i]
        avgService /= len(lst[0])
        avgTAT /= len(lst[0])
        avgWAT /= len(lst[0])
        # num, arrival, serviceTimes, start, completion, TurnAroundT, WaitingT
        result += '- - ' + str(round(avgService, 2)) + ' - ' + str(round(avgTAT, 2))
        result += ' ' + str(round(avgWAT, 2))
    else:
        result.rstrip(' ')

    return result

# when there are new pocesses, writes processes into current lists
def getNewProcesses(arrivedAt, arriveCurrent, servicedFor, serviceCurrent, time):
    while arrivedAt:
        if arrivedAt[0] <= time:
            arriveCurrent.append(arrivedAt[0])
            del arrivedAt[0]
            serviceCurrent.append(servicedFor[0])
            del servicedFor[0]
        else:
            break

# give copies in arguments
def getProcessingListAndStartingTimesRR(arrivedAt, servicedFor, numeration):
    time = 0
    arriveCurrent = []
    serviceCurrent = []
    currentPosition = 0
    processingList = [] # list of processes - every element 'is equal' to 1 unit of time
    startingTimes = []

    # getting quantum
    quantum = arrivedAt[0]
    del arrivedAt[0]
    del servicedFor[0]

    startedProcesses = []
    while arrivedAt or arriveCurrent:

        getNewProcesses(arrivedAt, arriveCurrent,
        servicedFor, serviceCurrent, time)

        # waiting for processes, when nothing to do
        if len(serviceCurrent) == 0:
            time += 1
            continue
        
        
        # process shorter than or equal quantum is deleted
        if serviceCurrent[currentPosition] <= quantum:
            timeOfCurrentProcess = serviceCurrent[currentPosition]
            nrOfCurrentProcess = numeration[currentPosition]
            # if the process hasn't started yet
            if nrOfCurrentProcess not in startedProcesses:
                startingTimes.append(time)
                startedProcesses.append(nrOfCurrentProcess)
            # writing to processingList
            for i in range(timeOfCurrentProcess):
                processingList.append(nrOfCurrentProcess)   
            time += timeOfCurrentProcess    
            # process is done
            del serviceCurrent[currentPosition]
            del numeration[currentPosition]
            del arriveCurrent[currentPosition]

        # process longer than quantum
        else:
            nrOfCurrentProcess = numeration[currentPosition]
            # if the process hasn't started yet
            if nrOfCurrentProcess not in startedProcesses:
                startingTimes.append(time)
                startedProcesses.append(nrOfCurrentProcess)
            # writing to processingList
            for i in range(quantum):
                processingList.append(nrOfCurrentProcess)
            serviceCurrent[currentPosition] -= quantum
            time += quantum 
            # going to next process on the list
            currentPosition += 1

        # not getting index out of list
        if currentPosition + 1 > len(serviceCurrent):
            currentPosition = 0
    return (processingList, startingTimes)


def getCompletionTimesAndNrs(processingList):
    checkCompleted = []
    completionTimesAndNrs = [[] for i in range(2)]

    # getting completion times
    for i in reversed(range( len(processingList) )):
        tmp = processingList[i]
        if tmp not in checkCompleted:
            checkCompleted.append(tmp)
            completionTimesAndNrs[0].insert(0, i + 1)
            completionTimesAndNrs[1].insert(0, tmp)
    return completionTimesAndNrs


def saveRRToResults(tmpArrived, tmpServiced, completionList, tmpStarted):
    # 0    1        2             3      4           5            6
    # num, arrival, serviceTimes, start, completion, TurnAroundT, WaitingT
    results = [[] for i in range(7)]
    del tmpArrived[0]
    del tmpServiced[0]
    for i in range(len(completionList[1])):
        results[4].append( completionList[0][i] )
        results[0].append( completionList[1][i] )
        tmp = results[0][-1] - 1
        results[1].append( tmpArrived[tmp] )
        results[2].append( tmpServiced[tmp] )
        results[3].append( tmpStarted[tmp] )
        results[5].append( results[4][-1] - results[1][-1] )
        results[6].append( results[4][-1] - results[1][-1] - results[2][-1] )

    return results


def rr(numbers, arrivedAt, servicedFor):
    tmpProcessLstAndStart = getProcessingListAndStartingTimesRR(arrivedAt[:], servicedFor[:], numbers[:])
    startTimes = tmpProcessLstAndStart[1]
    completionList = getCompletionTimesAndNrs(tmpProcessLstAndStart[0])
    del tmpProcessLstAndStart
    return saveRRToResults(arrivedAt, servicedFor, completionList, startTimes)


def sjf(arrivedAt, servicedFor, numeration):
    # num, arrival, serviceTimes, start, completion, TurnAroundT, WaitingT
    results = [[] for i in range(7)]
    time = 0
    arriveCurrent = []
    serviceCurrent = []

    while arrivedAt or arriveCurrent:

        getNewProcesses(arrivedAt, arriveCurrent,
        servicedFor, serviceCurrent, time)
        
        # waiting for processes, when nothing to do
        position = posOfShortestProcess(serviceCurrent)
        if position == -1:
            time += 1
            continue

        # num, arrival, serviceTimes, start, completion, TurnAroundT, WaitingT
        results[0].append(numeration[position])
        results[1].append(arriveCurrent[position])
        results[2].append(serviceCurrent[position])
        results[3].append(time)
        results[4].append(time + results[2][-1])
        results[5].append(results[4][-1] - results[1][-1])
        results[6].append(results[3][-1] - results[1][-1])
        time += results[2][-1]
        
        del numeration[position]
        del arriveCurrent[position]
        del serviceCurrent[position]
    
    return results






if __name__ == "__main__":
    # rr
    fileTmp = readProcessesFromFile('rr.txt')
    numbers = fileTmp[0]
    arriveTimes = fileTmp[1]
    serviceTimes = fileTmp[2]
    del fileTmp
    results = rr(numbers, arriveTimes, serviceTimes)
    outputText = transform(results, 1)
    results.remove()
    writeToFile(outputText, 'rrResults.txt')
    # sjf
    fileTmp = readProcessesFromFile('sjf.txt')
    numbers = fileTmp[0]
    arriveTimes = fileTmp[1]
    serviceTimes = fileTmp[2]
    del fileTmp
    results = sjf(arriveTimes, serviceTimes, numbers)
    outputText = transform(results, 1)
    writeToFile(outputText, 'sjfResults.txt')










