from sys import argv
script, folder = argv

import os
import subprocess
import shlex

###

# cmd = r"'C:\Program Files\PDFCreator\PDFCreator.exe' \/PrintFile= \/PrinterName='PDFCreator' \/OutputFile="

###

def pdf_to_jpg(folder):
    fajlovi_print = []
    fajlovi_out = []
    for subdir, dirs, files in os.walk(folder):
        for filename in files:
            filepath = subdir + os.sep + filename
            ##
            if filepath.endswith(".pdf"):
                # print (filepath)
                fajlovi_print.append(str("\'" + filepath + "\'"))
                output_file = filepath.removesuffix('.pdf')
                fajlovi_out.append(str("\'" + output_file + "\'"))
    #print(str(fajlovi_print))
    print_str = ' '.join([str(i) for i in fajlovi_print])
    # out_str = ' '.join([str(j) for j in fajlovi_out])
    # try:
    print_str = print_str.split()
    argumenti = [r"C:\Program Files\PDFCreator\PDFCreator.exe", r"/Merge ", print_str, r"/PrinterName='PDFCreator'", r"/OutputFile=" + str(fajlovi_out[0])]
    ##
    print(argumenti)
    ##
    # subprocess.run(argumenti)
    # except ValueError:
    #     continue
###

def main():
    pdf_to_jpg(folder)


if __name__ == "__main__":
    main()
