import pytesseract
from wand.image import Image
from wand.display import display
import subprocess
import os

def getPath():
    print("Please enter the source folder path: ")
    print("e.g. ", os.getcwd())
    path = input()
    print("\n")
    return path

def getInputFile():
    print("Please enter input file name in the directory. One can use an asterisk(*) to select all files with similar file name.")
    print("for example, *.tiff means select all file with .tiff suffix.")
    print("InputFile: ", end = "")
    fileIn = input()

    return fileIn

def getOutputFile():
    print("\nPlease enter output file name: ", end = "")
    fileOut = input()

    return fileOut

def mergeTiff(filePath, fileIn, fileOut):
    cmd = [fileIn, fileOut]
    #TODO folloow the process to try merging files
    
def process():
    path = getPath()
    inFile = getInputFile()
    outFile = getOutputFile()
    os.chdir(path)
    mergeTiff(path, inFile, outFile)
    cmd = ["convert", "-monochrome", "-compress", "lzw", path, "tif:-"]
    fconvert = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = fconvert.communicate()
    assert fconvert.returncode == 0, stderr

    # now stdout is TIF image. let's load it with OpenCV
    filebytes = numpy.asarray(bytearray(stdout), dtype=numpy.uint8)
    image = cv2.imdecode(filebytes, cv2.IMREAD_GRAYSCALE)
