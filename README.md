## TIF to OCR PDF Converter
Author: Zhiren Xu  
Publish data: 12/14/20

### What does it do
   Find tif files base on input, merge them into one tif under naming rule, then convert them into OCR pdf files. Merged tif file will be deleted after the convert process finishs.
   
   
### Prerequisites
   Run in Windows10 environment. 
   
   Python ver. 3.8 or higher, other version has not been tested. 
   
   Required Software: 
   
      ImageMagick (tested version: 7.0.10-43 Q16 x64 2020-11-23) 
      
      tesseract (tested version: v5.0.0-alpha.20201127)
      
   *If you import file name from CSV file, file names must in first row and no header is allowed*
   
   *Duplicate file name is ok as the script will filter input data*
   
   *Don't type the wrong file name*  

### Instruction:  
   1. put the script in the same folder as files you want merge&convert  
   2. run 'tif_to_pdf.py'  
   3. follow instructions on display

### Tips:
   1. You can get input file name by typing or import from csv file
   2. This program need a lot of compute resources. Try avoid running other tasks together with the script
   3. For safty, making sure you have backup files before running this script
