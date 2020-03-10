import os

tuning_sound=input("what did you want?(A ~ G): ") 

print("Start "+tuning_sound+" play")

os.system(f"start C:\{tuning_sound}.mp3") #file name: only english/korean:error occur
