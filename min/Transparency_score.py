from PIL import Image

'''
for i in range(76,100): #10_076~100
    #print(f'10_07{i}.PNG')
    img=Image.open(f'10_0{i}.PNG')
''' #rest success
'''
for i in range(0,5):
    img=Image.open(f'endtest-{i}.PNG')
'''#endtest score success(wartermark x)

#3.pdf test
for i in range(0,6):
    img=Image.open(f'3-{i}.PNG')

#img=img.convert("RGBA")
    datas=img.getdata()

    newData = []
    Cutoff=150

    for item in datas:
        if item[0] >= Cutoff and item[1] >=Cutoff and item[2] >=Cutoff:
            newData.append((255,255,255,0))

        else:
            newData.append(item)

    img.putdata(newData)
    # 3.pdf test
    img.save(f'new3-{i}.PNG')
'''
for i in range(76, 100):
    img.save(f'new10_0{i}.PNG',"PNG")
''' #rest success
'''
for i in range(0,5):
    img.save(f'endtest-{i}.PNG')
''' #endtest score success(wartermark x
