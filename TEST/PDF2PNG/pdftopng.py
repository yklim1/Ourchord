'''
from pdf2image import convert_from_path, convert_from_bytes

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
'''
#images = convert_from_bytes(open('C://anaconda\envs\mushroom\.vscode//testsky.pdf', 'rb').read())
#images = convert_from_path('C://anaconda\envs\mushroom\.vscode\testsky.pdf')
#pages = convert_from_path('C://anaconda\envs\mushroom\.vscode\10.pdf')

#for page in pages:
 #   page.save('.vscode//out.png', 'PNG')

import fitz

pdffile = ".vscode//12.pdf"
doc = fitz.open(pdffile)
'''
page = doc.loadPage(0) #number of page
pix = page.getPixmap()
output = ".vscode//outfile.png"
pix.writePNG(output)
'''
for i in range(len(doc)):
    page = doc.loadPage(i)
    pix = page.getPixmap()
    output = f".vscode//outfile{i}.png"
    pix.writePNG(output)