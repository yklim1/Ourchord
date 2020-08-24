from wand.image import Image

for i in range(25):

    with Image(filename='/Users/zjisuoo/Documents/zjisuoo_git/OurChord/01_OPENCV/pdf/{i}.pdf',resolution=200) as img: #image resolution(200/500)
        img.format="PNG"
        img.save(filename='/Users/zjisuoo/Documents/zjisuoo_git/OurChord/01_OPENCV/{i}.png')
