import subprocess
import os
import time
import sys
import csv
from multiprocessing import Pool

os.environ['OMP_THREAD_LIMIT'] = '1'

##open csv file and read handler link, store in a list
# @param    csvName
#           the file name user typed in
# @return   fileList
#           a list contain file name that need to be processed
def readCSV(csvName):
    fileList = []

    try:
        inFile = open(csvName, 'r')
        csvReader = csv.reader(inFile, delimiter=',')
        for row in csvReader:
            if len(row) > 0:
                fileName = row[0]
                if not (fileName in fileList):
                    fileList.append(fileName)
        print ("Open input CSV success.")
    except:
        print("Fail to open input CSV. Press enter to exit.")
        key = input()
        sys.exit()
        
    return fileList

## Check if input has suffix or not
# @param    userInput
#           Input file name
# @return   fileIn
#           Sanitized input file name
def sanitizeInput(userInput):
    fileIn = ""
    if not(".csv" in userInput):
        fileIn = userInput + ".csv"
    else:
        fileIn = userInput
    return fileIn

## Get input tif file name
# @return   patternList
#           A list include all tilf file name waiting to process
def getFilePatternList():
    patternList = []
    
    isContinue = True
    print("Input file name using CSV or hand typing?")
    print("Enter csv file name with suffix for read from CSV or hit Enter for hand typing.")
    userInput = input()
    if len(userInput) != 0:
        csvFile = sanitizeInput(userInput)
        patternList = readCSV(csvFile)
    else:
        print("Please enter the common name pattern of files you want to convert: ")
        print("e.g. Lantern_1913-09-16_001.tif --> Lantern_1913-09-16\n")
        print("You can choose to convert multiple days at once. Just keep typing name pattern.", end = '')
        print(" When done, type 'finish'.")
        while(isContinue):
            print("File pattern: ", end = '');
            pattern = input()
            if pattern != "finish":
                patternList.append(pattern)
            else:
                isContinue = False
            
        print("\n")
    return patternList

## Setup input/output file name and do the work
# @param    filePatternList
#           A list include all tilf file name waiting to process
def process(filePatternList):
    outputTifList = []
    outputPdfList = []
    #two copy of outputTifList, lame design on my part but I don't want change
    #working functions
    outputTifListCp = []
    outputTifListCp1 = []
    fullFilePatternList = []

    try:
        for filePattern in filePatternList:
            fullFilePattern = filePattern + "*.tif*"
            outputTif = filePattern + ".tif"
            outputPdf = filePattern
            fullFilePatternList.append(fullFilePattern)
            outputTifList.append(outputTif)
            outputTifListCp.append(outputTif)
            outputTifListCp1.append(outputTif)
            outputPdfList.append(outputPdf)
    except:
        print("ERROR: unable to load data.\nPress enter to exit.")
        input()
        sys.exit()
    print("Merge tif files...", end = '')
    try:
        mergeTifParallel(fullFilePatternList, outputTifList)
    except:
        print("ERROR: unable to merge tif.\nPress enter to exit.")
        input()
        sys.exit()
    try:
        convertToPdfParallel(outputTifListCp, outputPdfList)
        print("Deleting merged tif file...", end = '')
        for file in outputTifListCp1:
            try:
                os.remove(file)
            except:
                print("Fail to delete ", file)
        print("Done!")
    except:
        print("ERROR: unable to convert tif or error happen when delete file. Output tif may still be correct.\nPress enter to exit.")
        input()
        sys.exit()

## merge tif files in multiprocess way
# @param    fullFilePatternList
#           A list of file name but with suffix (.tif)
# @param    outputTifList
#           A list of output pdf file name WITHOUT suffix (.pdf)
def mergeTifParallel(fullFilePatternList, outputTifList):
    dataPairs = []

    while(len(fullFilePatternList) > 0):
        data = [fullFilePatternList.pop(0), outputTifList.pop(0)]
        dataPairs.append(data)
    try:
        with Pool() as p:
            p.map(mergeTif, dataPairs)
    except:
        print("ERROR: parallel merge fail.\nPress enter to exit.")
        input()
        sys.exit()
    print("Done.\n")

## call image magick to merge tif files
# @param    param
#           A pair of file name, generate by pool object map.
#           include source file name and output file name
def mergeTif(param):
        src = param[0]
        dest = param[1]
        print("Process source file: ", src, "   ")
        print("Finish merged file: ", dest, "...", end = '');
        subprocess.run(["magick", src, dest],capture_output=True)
        print("Done")

## covert merged tif to OCR pdf in multiprocess way
# @param    outputTifListCp
#           A list contain all merged tif file name as input file
# @param    outputPdfList
#           A lsit contain all output pdf file name
def convertToPdfParallel(outputTifListCp, outputPdfList):
    dataPairs = []

    while(len(outputTifListCp) > 0):
        data = [outputTifListCp.pop(0), outputPdfList.pop(0)]
        dataPairs.append(data)
    print("Convert merged tif file to OCR pdf...")
    print("DO NOT close the script until further notice. The process may take several minutes...")
    print("If you can find Tesseract processes in Task Manager and CPU usage is high, the convertor is running...")
    try:
        with Pool() as p:
            t_start = time.time()
            p.map(convertToPdf, dataPairs)
            t_end = time.time()
            print("Process Time: ", t_end - t_start, "s\n")
    except:
        print("ERROR: parallel convert fail.\nPress enter to exit.")
        input()
        sys.exit()
    print("Done\n")

## call tesseract to convert tif file to OCR pdf file
# @param    param
#           A pair of file name, generate by pool object map.
#           include source file name and output file name
def convertToPdf(param):
    src = param[0]
    dest = param[1]
    subprocess.run(["tesseract", src, dest, "pdf"],capture_output=True)
    
def welcome():
    print("********************************************")
    print("*     TIF to OCR PDF Converter v1.0.1      *")
    print("*            Author: Zhiren Xu             *")
    print("*         published data: 12/14/20          *")
    print("********************************************")

def end():
    print("The process is finished. The pdf file is in the same directory as the script.")
    print("Press anykey to exit")
    input()
    sys.exit()


def main():
    welcome()
    inputPatternList = getFilePatternList()
    process(inputPatternList)
    end()
        
if __name__ == "__main__":
    main()
