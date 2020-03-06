from PIL import Image

#i=1
#img=Image.open('3test-'+i+'.png')
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
#for i in range(0,6):
#    img=Image.open(f'3-{i}.PNG')

for i in range(1,31):
    #img = Image.open(f'3-{i}.PNG')
    #img = Image.open(f'C://cnntrain//Note//Template Match//hote2//rest2_0{i}.PNG')
    #img = Image.open(f'C://rest8//rest8_{i}.PNG') #Cutoff200
    img = Image.open(f'C://100test//rest8//rest8_{i}.PNG')  # Cutoff170

#img=img.convert("RGBA")
    datas=img.getdata()

    newData = []
    Cutoff=170 #10이하는 비슷한걸로 보임 10이랑 100은 차이남

    for item in datas:
        if item[0] >= Cutoff and item[1] >=Cutoff and item[2] >=Cutoff:
            newData.append((255,255,255,0))

        else:
            newData.append(item)

    img.putdata(newData)
    # 3.pdf test
    #img.save(f'new3-{i}.PNG')
    #img.save(f'C://cnntrain//Note//Template Match//hote2//rest2_0{i}.PNG')
    #img.save(f'C://rest8//rest8_{i}.PNG') #Cutoff50 #Cutoff200
    img.save(f'C://100test//rest8//rest8_{i}.PNG')  # Cutoff170
    #img.save(f'3-{i}.PNG', "PNG")
'''
for i in range(76, 99):
    img.save(f'new10_0{i}.PNG',"PNG")
''' #rest success
'''
for i in range(0,5):
    img.save(f'endtest-{i}.PNG')
''' #endtest score success(wartermark x)
