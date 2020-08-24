from PIL import Image

image = Image.open('/Users/zjisuoo/Desktop/Pre/test04/score/test/2/2_003.png')
resize_image = image.resize((28, 28))
resize_image.save('/Users/zjisuoo/Desktop/Pre/test04/resize_score/test/2/2_003.png')