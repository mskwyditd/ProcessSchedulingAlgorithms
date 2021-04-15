
def whichPosition(elem, lst):
    for j in range(len(lst)):
        if elem == lst[j]:
            return j
    print("Error: whichPosition()")


def readPagesFromFile(inputDir = 'lfu.txt'):
    frames = 0
    inputFile = open(inputDir, 'rt')
    frames = int(inputFile.readline().rstrip('\n'))
    inputPages = inputFile.readline().split()
    inputFile.close()
    return (inputPages, frames)


def writeToFile(content = '', outputDir = 'lfuResults.txt'):
    outputFile = open(outputDir, 'wt')
    outputFile.write(content)
    outputFile.close()


def findLeastUsedPageIndex(currentPages, pagesCounter):
    tmpKey = ""
    tmpVal = -1
    for key in currentPages:
        if tmpVal == -1:
            tmpKey = key
            tmpVal = pagesCounter[key]
        elif pagesCounter[key] < tmpVal:
            tmpKey = key
            tmpVal = pagesCounter[key]
    return tmpKey


def lfu(pages, frames):
    hits = 0
    faults = 0 # zamiany stron
    pagesCounter = {}
    currentPages = []

    for i in range(len(pages)):
        # if no pages
        if len(currentPages) == 0:
            currentPages.append(pages[i])
            pagesCounter[pages[i]] = 1
            faults += 1
        # if next page is already being processed, its frequency is going us
        elif pages[i] in currentPages:
            pagesCounter[pages[i]] += 1
            hits += 1
        # if frame not full
        elif len(currentPages) < frames:
            currentPages.append(pages[i])
            pagesCounter[pages[i]] = 1
            faults += 1
        # find and replace the least frequently used page
        else:
            tmpKey = findLeastUsedPageIndex(currentPages, pagesCounter)

            pos = whichPosition(tmpKey, currentPages)
            del currentPages[pos]
            currentPages.append(pages[i])
            
            # counting occurences of page numbers
            if pages[i] in pagesCounter.keys():
                pagesCounter[pages[i]] += 1
            else:
                pagesCounter[pages[i]] = 1
            faults += 1

    return ( str(faults), str(hits) )









def inPut(inDir = "lfu.txt"):
    frames = 0
    hits = 0
    faults = 0 # zamiany stron
    checkList = {}
    currentPages = []
    
    inputFile = open(inDir, 'rt')
    frames = int(inputFile.readline().rstrip('\n'))
    # przepisanie danych z pliku do listy
    inputPages = inputFile.readline().split()
    inputFile.close()

    # przechodzimy po wszystkich stronach
    for i in range(len(inputPages)):
        # jeśli nie ma ma jeszcze żadnej strony
        if len(currentPages) == 0:
            currentPages.append(inputPages[i])
            checkList[inputPages[i]] = 1
            faults += 1
        # jeśli następna strona jest juz przetwarzana
        elif inputPages[i] in currentPages:
            checkList[inputPages[i]] += 1
            hits += 1
        # jeśli lista nie jest jeszcze zapełniona
        elif len(currentPages) < frames:
            currentPages.append(inputPages[i])
            checkList[inputPages[i]] = 1
            faults += 1
        # trzeba zastapić stronę w currentPages inną
        else:
            tmpKey = ""
            tmpVal = -1
            # przechodzimy po currentPages, by znaleźć najrzadziej używaną stronę z checklist
            for key in currentPages:
                if tmpVal == -1:
                    tmpKey = key
                    tmpVal = checkList[key]
                elif checkList[key] < tmpVal:
                    tmpKey = key
                    tmpVal = checkList[key]

            # wymiana obsługiwanej strony w currentPages
            pos = whichPosition(tmpKey, currentPages)
            del currentPages[pos]
            currentPages.append(inputPages[i])
            
            # czy kolejna strona jest w checkList
            if inputPages[i] in checkList.keys():
                checkList[inputPages[i]] += 1
            else:
                checkList[inputPages[i]] = 1
            faults += 1
    del checkList
    return str(faults) + ' ' + str(hits)

def outPut(inDir = 'lfu.txt', outDir = 'lfuResults.txt'):
    
    outputFile = open(outDir, 'wt')

    outputFile.write(inPut(inDir))

    outputFile.close()

    

if __name__ == "__main__":
    fileTmp = readPagesFromFile()
    pages = fileTmp[0]
    frames = fileTmp[1]
    del fileTmp
    resTmp = lfu(pages, frames)
    results = str(resTmp[0]) + ' ' + str(resTmp[1])
    writeToFile(results)




