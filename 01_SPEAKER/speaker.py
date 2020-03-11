import os
import sys

#A~G
tuning=('C','D','E','F','G','A','B')

while 1: #user input only A to G
    tuning_sound=input("what did you want?(A ~ G): ")

#a~g --> A~G change
    tuning_sound=tuning_sound.upper()

    ex=0
#exception
    for i in tuning: #i=='C'~'B'
        #print(i)
        ex +=1
        #'C' to 'B'까지 순차적으로 접근해서 조건 만족 시 출력 
        if tuning_sound==i: #tuning_sound=='C'
            print("Start "+tuning_sound+" play")
            os.system(f"start C:/{tuning_sound}.mp3") #file name: only english
            sys.exit(1) #출력 후 종료

    if ex==7: #if input data is not A to G
        print("please input A to G !!")

