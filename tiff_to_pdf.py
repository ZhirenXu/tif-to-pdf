import pytesseract
import subprocess
from wand.image import Image
from wand.display import display

def convertPdfSerial(inputFile, outputFile):
    pdf = pytesseract.image_to_pdf_or_hocr(inputFile, extension='pdf')
    with open(outputFile, 'w+b') as f:
        f.write(pdf)

def main():
    print(pytesseract.get_tesseract_version())
    #subprocess.run(["magick", "test*", "combine.tif"],capture_output=True)
    #convertPdfSerial("combine.tif", "test.pdf")
    subprocess.run(["tesseract", "combine.tif", "test", "pdf"],capture_output=True)
if __name__ == "__main__":
    main()
