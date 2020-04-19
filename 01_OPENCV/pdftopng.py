from wand.image import Image
with Image(filename='endtest.pdf',resolution=200) as img: #image resolution(200/500)
    img.format="png"
    img.save(filename='endtest.png')
