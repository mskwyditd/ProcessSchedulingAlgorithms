
def whichPosition(elem, lst):
    for j in range(len(lst)):
        if elem == lst[j]:
            return j
    print("Error: whichPosition()")


def readPagesFromFile(inputDir = 'pages.txt'):
    frames = 0
    inputFile = open(inputDir, 'rt')
    frames = int(inputFile.readline().rstrip('\n'))
    inputPages = inputFile.readline().split()
    inputFile.close()
    return (inputPages, frames)


def writeToFile(content = '', outputDir = 'pagesResults.txt'):
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


def lru(pages, frames):
    hits = 0
    faults = 0 # zamiany stron
    currentPages = []
    # least recently used page is always at i=0 in currently processed pages
    for i in range(len(pages)): 
        # if no pages
        if len(currentPages) == 0:
            currentPages.append(pages[i])
            faults += 1
        # if next page is already in the frame, its position is changed to i=0
        elif pages[i] in currentPages:
            pos = whichPosition(pages[i], currentPages)
            del currentPages[pos]
            hits += 1
            currentPages.append(pages[i])
        # if frame not full
        elif len(currentPages) < frames:
            currentPages.append(pages[i])
            faults += 1
        else:
            del currentPages[0]
            currentPages.append(pages[i])
            faults += 1
    return ( str(faults), str(hits) )







    

if __name__ == "__main__":
    # lfu
    fileTmp = readPagesFromFile('lfu.txt')
    pages = fileTmp[0]
    frames = fileTmp[1]
    del fileTmp
    resTmp = lfu(pages, frames)
    results = str(resTmp[0]) + ' ' + str(resTmp[1])
    writeToFile(results, 'lfuResults.txt')
    # lru
    fileTmp = readPagesFromFile('lru.txt')
    pages = fileTmp[0]
    frames = fileTmp[1]
    del fileTmp
    resTmp = lru(pages, frames)
    results = str(resTmp[0]) + ' ' + str(resTmp[1])
    writeToFile(results, 'lruResults.txt')



