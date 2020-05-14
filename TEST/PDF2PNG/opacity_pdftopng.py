#opacity 악보

import fitz
    
pdffile = "12.pdf"
doc = fitz.open(pdffile)
page = doc.loadPage(0) #number of page
pix = page.getPixmap()
output = "outfile12.png"
pix.writePNG(output)
