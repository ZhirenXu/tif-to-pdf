import subprocess
import os
import time
import sys
from multiprocessing import Pool

def getFilePatternList():
    patternList = []
    
    isContinue = True
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

def process(filePatternList):
    outputTifList = []
    outputPdfList = []
    outputTifListCp = []
    fullFilePatternList = []

    try:
        for filePattern in filePatternList:
            fullFilePattern = filePattern + "*.tif*"
            outputTif = filePattern + ".tif"
            outputPdf = filePattern
            fullFilePatternList.append(fullFilePattern)
            outputTifList.append(outputTif)
            outputTifListCp.append(outputTif)
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
    except:
        print("ERROR: unable to convert tif. Output file may still be correct.\nPress enter to exit.")
        input()
        sys.exit()

def mergeTifParallel(fullFilePatternList, outputTifList):
    dataPairs = []

    while(len(fullFilePatternList) > 0):
        data = [fullFilePatternList.pop(0), outputTifList.pop(0)]
        dataPairs.append(data)
    try:
        with Pool(6) as p:
            p.map(mergeTif, dataPairs)
    except:
        print("ERROR: parallel merge fail.\nPress enter to exit.")
        input()
        sys.exit()
    print("Done.\n")

#paramList is list in list
def mergeTif(param):
        src = param[0]
        dest = param[1]
        print("Process source file: ", src, "   ")
        print("Finish merged file: ", dest, "...", end = '');
        subprocess.run(["magick", src, dest],capture_output=True)
        print("Done")

def convertToPdfParallel(outputTifListCp, outputPdfList):
    dataPairs = []

    while(len(outputTifListCp) > 0):
        data = [outputTifListCp.pop(0), outputPdfList.pop(0)]
        dataPairs.append(data)
    print("Convert merged tif file to OCR pdf...")
    print("DO NOT close the script until further notice. The process may take several minutes...")
    print("If you can find Tesseract processes in Task Manager and CPU usage is high, the convertor is running...")
    try:
        with Pool(6) as p:
            t_start = time.time()
            p.map(convertToPdf, dataPairs)
            t_end = time.time()
            print("Process Time: ", t_end - t_start, "s\n")
    except:
        print("ERROR: parallel convert fail.\nPress enter to exit.")
        input()
        sys.exit()
    print("Done\n")

#paramList is list in list
def convertToPdf(param):
    src = param[0]
    dest = param[1]
    subprocess.run(["tesseract", src, dest, "pdf"],capture_output=True)
    
def welcome():
    print("********************************************")
    print("*     TIF to OCR PDF Converter v1.0.0      *")
    print("*            Author: Zhiren Xu             *")
    print("*         published data: 12/1/20          *")
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
