
def whichPosition(elem, lst):
    for j in range(len(lst)):
        if elem == lst[j]:
            return j
    print("Error: whichPosition()")


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


def readPagesFromFile(inputDir = 'lru.txt'):
    frames = 0
    inputFile = open(inputDir, 'rt')
    frames = int(inputFile.readline().rstrip('\n'))
    inputPages = inputFile.readline().split()
    inputFile.close()
    return (inputPages, frames)


def writeToFile(content = '', outputDir = 'lruResults.txt'):
    outputFile = open(outputDir, 'wt')
    outputFile.write(content)
    outputFile.close()














def inPut(inDir = "lru.txt"): 
    frames = 0

    inputFile = open(inDir, 'rt')
    frames = int(inputFile.readline().rstrip('\n'))
    inputPages = inputFile.readline().split()
    inputFile.close()

    results = lru(inputPages, frames)    
    
    return str(results[0] + ' ' + results[1])

def outPut(inDir = 'lru.txt', outDir = 'lruResults.txt'):
    
    outputFile = open(outDir, 'wt')
    
    outputFile.write(inPut(inDir))

    outputFile.close()
    

if __name__ == "__main__":
    fileTmp = readPagesFromFile()
    pages = fileTmp[0]
    frames = fileTmp[1]
    del fileTmp
    resTmp = lru(pages, frames)
    results = str(resTmp[0]) + ' ' + str(resTmp[1])
    writeToFile(results)




