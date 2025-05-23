from data.globals import *

def makeToFile(path): #takes either a filename or ID, if filename it returns it, otherwise it adds .md 
    if not path.endswith(".md"):
        path = path + ".md"
    return path

def makeToID(path):
    if path.endswith(".md"):
        return path[:-3]

def shortPath(path):
    for startOfPath in [filesPath + "/",trashPath + "/"]:
        if path.startswith(startOfPath):
            return(path.replace(startOfPath,""))
        else:
            return path


def dataPath(pathEnd):
    if pathEnd.startswith(pathStart):
        return pathEnd
    return pathJoin(pathStart,pathEnd)

def pathJoin(pathA,pathB):
    path0, path1 = pathA, pathB
    if path0.endswith("/"):
        path0 = path0[:len(path0)-1]
    if path1.startswith("/"):
        path1 = path1[1:]
    return f"{path0}/{path1}"


def dictElement(dictionary):
    key, value = next(iter(dictionary.items()))
    return key,  value

def clearDuplicates(arr):
    newArr = []
    for element in arr:
        if element not in newArr:
            newArr.append(element)
    return newArr

def rotate(arr):
    newArr = []
    maxLength = max([len(i) for i in arr])

    for i in range(maxLength):
        row = []
        for col in arr:
            row.append(col[i])
        newArr.append(row)
    return newArr


def cutText(text, maxLineWidth):
    lines = []
    line = ""
    words0 = text.split(" ")
    words = []
    for word in words0:
        if len(word) > maxLineWidth:
            tempWord = word
            while len(tempWord) > maxLineWidth:
                
                words.append(tempWord[:maxLineWidth])
                tempWord = tempWord[maxLineWidth:]
            words.append(tempWord)
        else:
            words.append(word)
        
    for word in words:
        if not line:
            newLine = word
        else:
            newLine = line + " " + word
        
        if len(newLine) > maxLineWidth:
            lines.append(line)
            line = word
        else:
            line = newLine
    lines.append(line)
    return lines


def reducedText(text, maxWidth):
    if maxWidth == 0:
        return f"{text} {maxWidth}"
    tempLines = cutText(text, maxWidth)
    if len(text) <= maxWidth:
        displayText = text +"\n"
    elif len(tempLines) > 2:
        
        tempLines = cutText(text, maxWidth)
        line0 = tempLines[0]
        line1 = tempLines[1]
        lineLen = len(line1)
        dL = maxWidth - lineLen
        if dL >= 3:
            line1 += "..."
        else:
            line1 += " "*(maxWidth-len(line1))
            line1 = line1[:maxWidth - 3]
            line1 += "..."
        displayText = line0 + " " + line1
    else:
        displayText = text
    return displayText

def displayableText(text, maxWidth):
    if len(text) <= maxWidth:
        return text + "\n"
    return text

