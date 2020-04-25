from pdf2image import convert_from_path

pages = convert_from_path('/Users/zjisuoo/Documents/zjisuoo_git/OurChord/01_OPENCV/pdf/', 500)

for page in pages :
    page.save('/Users/zjisuoo/Documents/zjisuoo_git/OurChord/01_OPENCV/pdf/out{page}.png', 'PNG')