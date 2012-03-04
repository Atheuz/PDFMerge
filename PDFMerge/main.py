# -*- coding: utf-8 -*-

# Filename      main.py
# Author        Lasse Vang Gravesen <gravesenlasse@gmail.com>
# First edited  02-03-2012 19:55
# Last edited   02-03-2012 21:34

import os
import argparse
import subprocess
import glob

f = open("template.tex", "r")
TEMPLATE = f.read()
f.close()
TSTART, TEND, JUNK = TEMPLATE.partition("\end{document}")
JUNK = ["*.log","*.aux","*.dvi","*.lof","*.lot","*.bit","*.idx","*.glo","*.bbl","*.ilg","*.toc","*.ind","*.out","*.synctex.gz","*.blg"]

def run(path):
    path = os.path.abspath(path)
    pdf_name = os.path.join(path, "out.pdf")

    # PDF generation does not work with pdflatex if there's a file that's inaccessible, however xelatex still works. 
    # The problem is however solved by removing the out.pdf file before anything else is done.
    if os.path.isfile(pdf_name):
        try:
            os.remove(pdf_name)
        except WindowsError:
            pass

    pdfs = ["    \includepdf[pages=-]{%s}" % os.path.join(path, x).replace('\\','/') for x in os.listdir(path) if '.pdf' in x.lower()]
    pdfs = '\n'.join(pdfs)
     
    output_fn = os.path.join(path, "out.tex")
    output_str = TSTART + pdfs + '\n\n' + TEND
    
    with open(output_fn, "wb") as output:
        output.write(output_str)
        output.close()
        
    cur_dir = os.getcwd()
    os.chdir(path)
    commandline_info = ['pdflatex', '-interaction=nonstopmode', output_fn]
    # commandline_info = ['xelatex', output_fn, '-interaction=nonstopmode']
    subprocess.Popen(commandline_info, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    
    os.remove(output_fn)
    
    for i in JUNK:
        for j in glob.glob("%s/%s" % (path, i)):
            os.remove(j)
    
    os.chdir(cur_dir)
    print "Done."

def main():
    parser = argparse.ArgumentParser(description="Requires a fairly complete MikTex install, meaning it requires at least xelatex to be installed and in the path.")
    parser.add_argument('path', metavar='P', type=str, default=None, help='Set path of PDFs to merge.')
    args = parser.parse_args()
    
    run(args.path)

if __name__ == '__main__':
    main()

