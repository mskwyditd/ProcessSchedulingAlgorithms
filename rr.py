
def readProcessesFromFile(inputDir = 'rr.txt'):
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


def writeToFile(content = '', outputDir = 'rrResults.txt'):
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




# delete
def process(arriveAt, serviceFor, numeration, quantum, resStart, processingList):
    time = 0

    arriveCurrent = []
    serviceCurrent = []
    
    # aktualna pozycja na przetwarzanej liście(arriveCurrent itd...)
    currentPos = 0
    
    # Zakładam, że wiem kiedy skończą przychodzić procesy do obsługi
    while arriveAt or arriveCurrent:
        # gdy zwiększa się czas(time), przychodzą kolejne procesy(serviceFor -> serviceCurrent i arriveAt -> arriveCurrent)
        while arriveAt:
            if arriveAt[0] <= time:
                arriveCurrent.append(arriveAt[0])
                del arriveAt[0]
                serviceCurrent.append(serviceFor[0])
                del serviceFor[0]
            else:
                break
        
        # w oczekiwaniu na kolejny proces
        if len(serviceCurrent) == 0:
            continue

        temporaryNumeration = []
        # wpisywanie danych do list
        # proces krótszy lub równy od kwantu (proces usuwany z listy do obsługi)
        if serviceCurrent[currentPos] <= quantum:
            tmp = serviceCurrent[currentPos]
            tmpNr = numeration[currentPos]
            # jeśli nie rozpoczęto jeszcze przetwarzania procesu
            if tmpNr not in temporaryNumeration:
                resStart.append(time)
                temporaryNumeration.append(tmpNr)
            # wpisanie procesu do processingList
            for i in range(tmp):
                processingList.append(tmpNr)
            time += tmp
            #usunięcie przetworzonego procesu
            del serviceCurrent[currentPos]
            del numeration[currentPos]
            del arriveCurrent[currentPos]
        # proces dłuższy od kwantu czasu
        else:
            tmpNr = numeration[currentPos]
            # jeśli nie rozpoczęto jeszcze przetwarzania procesu
            if tmpNr not in temporaryNumeration:
                resStart.append(time)
                temporaryNumeration.append(tmpNr)
            # wpisanie procesu do processingList
            for i in range(quantum):
                processingList.append(tmpNr)
            # zmniejszenie czasu obsługi procesu
            serviceCurrent[currentPos] -= quantum
            time += quantum
            # zwiększenie pozycji o 1, bo musimy przejść do następnego procesu
            currentPos += 1

        #jeśli wyjdziemy poza listę procesów
        if currentPos + 1 > len(serviceCurrent):
            currentPos = 0

# delete
def calculate(processingList, resCompl, resNr):
    checkCompleted = []
    # wpisywanie wyników do odpowiednich list
    for i in reversed(range( len(processingList) )):
        tmp = processingList[i]
        # Wpisujemy tak, by było posortowane rosnąco po czasie zakończenia(resCompl)
        if tmp not in checkCompleted:
            checkCompleted.append(tmp)
            resCompl.insert(0, i + 1)
            resNr.insert(0, tmp)

# delete
def inPut(results, inDir = 'rr.txt'):
    
    processingList = [] # tutaj wpisane będą procesy, przetwarzane w danym czasie

    resNr = []
    resArr = [] # Arrival
    resSer = [] # Service
    resStart = []
    resCompl = [] # Completion
    resTAT = [] # czas zakończenia od przybycia - Turnaround Time
    resWAT = [] # Waiting Time - czas oczekiwania na rozpoczęcie obsługi

    inputFile = open(inDir, "rt")
    
    nrs = [] # numery procesów
    quantum = int(inputFile.readline().rstrip())
    size = 1
    # oczytanie danych z pliku do list
    for li in inputFile:
        line = li.split()
        resArr.append(int(line[0]))
        resSer.append(int(line[1]))
        nrs.append(size)
        size += 1

    inputFile.close()

    # kopie, bo potrzebuję później danych z pliku do obliczenia wyników
    process(resArr[:], resSer[:], nrs[:], quantum, resStart, processingList)
    
    calculate(processingList, resCompl, resNr)

    tmpArr = resArr
    tmpSer = resSer
    tmpStart = resStart
    resArr = []
    resSer = []
    resStart = []

    # wpisywanie danych do pozostałych list
    for i in range(len(resNr)):
        tmp = resNr[i] - 1
        resArr.append( tmpArr[tmp] )
        resSer.append( tmpSer[tmp] )
        resStart.append( tmpStart[tmp] )
        resTAT.append( resCompl[i] - resArr[-1] )
        resWAT.append( resCompl[i] - resArr[-1] - resSer[-1] )
    
    results.append(resNr)
    results.append(resArr)
    results.append(resSer)
    results.append(resStart)
    results.append(resCompl)
    results.append(resTAT)
    results.append(resWAT)
    del resNr, resStart, resSer, resArr, resCompl, resWAT, resTAT, tmpArr, tmpStart, tmpSer

# delete
def outPut( saveRData = True, inDir = 'rr.txt', outDir = 'rrResults.txt' ):
    results = []

    inPut(results, inDir)

    # liczenie średnich
    avgSer = 0.
    avgTAT = 0.
    avgWAT = 0.
    for i in range(len(results[0])):
        avgSer += results[2][i]
        avgTAT += results[5][i]
        avgWAT += results[6][i]
    avgSer /= len(results[0])
    avgTAT /= len(results[0])
    avgWAT /= len(results[0])

    outputFile = open(outDir, 'wt')

    # zapisanie w pliku danych: Nr Arr Ser Start Compl TAT WAT i średnich
    if saveRData:
        for i in range(len(results[0])):
            tmpOutput = ""
            for j in range( len(results) ):
                tmpOutput += (str(results[j][i]) + ' ')
            tmpOutput = tmpOutput.rstrip(" ")
            tmpOutput += '\n'
            outputFile.write(tmpOutput)
        outputFile.write( '- - ' + str(round(avgSer, 2)) + ' - - - ' + str(round(avgTAT, 2))
        + ' ' + str(round(avgWAT, 2)) )

        # wersja bez zaokrąglania, gdyby prowadzący chciał bez round'a
        # outputFile.write( '- - ' + str(avgSer) + ' - - - ' + str(avgTAT)
        # + ' ' + str(avgWAT) )
    else:
        outputFile.write(str(max(results[0])) + " " + str(avgWAT))

    del results
    

    outputFile.close()
    

if __name__ == "__main__":
    fileTmp = readProcessesFromFile()
    numbers = fileTmp[0]
    arriveTimes = fileTmp[1]
    serviceTimes = fileTmp[2]
    del fileTmp
    results = rr(numbers, arriveTimes, serviceTimes)
    outputText = transform(results, 1)
    writeToFile(outputText)

