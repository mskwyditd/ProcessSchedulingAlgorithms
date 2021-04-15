
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


def readProcessesFromFile(inputDir = 'sjf.txt'):
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


def sjf(arrivedAt, servicedFor, numeration):
    results = [[] for i in range(7)]
    time = 0
    arriveCurrent = []
    serviceCurrent = []
    while arrivedAt or arriveCurrent:
        # when there are new processes(time)
        while arrivedAt:
            if arrivedAt[0] <= time:
                arriveCurrent.append(arrivedAt[0])
                del arrivedAt[0]
                serviceCurrent.append(servicedFor[0])
                del servicedFor[0]
            else:
                break
        
        # waiting for proceses, when nothing to do
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


def writeToFile(content = '', outputDir = 'sjfResults.txt'):
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
    



# delete
def process(arriveAt, serviceFor, numeration, resNr, resArr, resSer, resStart,
resCompl, resTAT, resWAT):
    time = 0
    
    arriveCurrent = []
    serviceCurrent = []

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
        # pozycja najkrótszego procesu, z czekających na obsługę
        position = posOfShortestProcess(serviceCurrent)
        # gdy serviceCurrent jest pusta
        if position == -1:
            time += 1
            continue
        # Zbieranie danych o przetworzonym procesie do wyników
        resNr.append(numeration[position])
        resArr.append(arriveCurrent[position])
        resSer.append(serviceCurrent[position])
        resStart.append(time)
        resCompl.append(time + resSer[-1])
        resTAT.append(resCompl[-1] - resArr[-1])
        resWAT.append(resStart[-1] - resArr[-1])
        time += resSer[-1]
        
        # usunięcie przetworzonego procesu
        del numeration[position]
        del arriveCurrent[position]
        del serviceCurrent[position]

#delete    
def inPut(results, inputDir = 'sjf.txt'):
    
    # listy z wynikami
    resNr = []
    resArr = [] # Arrival
    resSer = [] # Service
    resStart = []
    resCompl = [] # Completion
    resTAT = [] # czas zakończenia od przybycia - Turnaround Time
    resWAT = [] # waiting time - czas oczekiwania na rozpoczęcie obsługi
    # Waiting Time

    processes = readProcessesFromFile(inputDir)
    nubmers = processes[0]
    arriveTimes = processes[1]
    serviceTimes = processes[2]
    

    process(arriveTimes, serviceTimes, nubmers, resNr, resArr, resSer, resStart, resCompl,
    resTAT, resWAT )

    results.append(resNr)
    results.append(resArr)
    results.append(resSer)
    results.append(resStart)
    results.append(resCompl)
    results.append(resTAT)
    results.append(resWAT)
    del resNr, resStart, resSer, resArr, resCompl, resWAT, resTAT

# delete
def outPut( saveData = True, inDir = 'sjf.txt', outDir = 'sjfResults.txt' ):

    results = []

    inPut(results, inDir)

    # liczenie średnich czasów obsługi
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
    if saveData:
        for i in range(len(results[0])):
            tmpOutput = ""
            for j in range(len(results)):
                tmpOutput += (str(results[j][i]) + ' ')
            tmpOutput = tmpOutput.rstrip(" ")
            tmpOutput += '\n'
            outputFile.write(tmpOutput)
        outputFile.write( '- - ' + str(round(avgSer, 2)) + ' - - - ' + str(round(avgTAT, 2))
        + ' ' + str(round(avgWAT, 2)) )

        # wersja bez zaokrąglania
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
    results = sjf(arriveTimes, serviceTimes, numbers)
    outputText = transform(results, 1)
    writeToFile(outputText)

