## ALGORITHM EXPLAIN   
* To be changed to Thread     

Note Recognition(OPENCV)   
> notesearch  
>> transgap (get the gap between base chord change chord for chord conversion)   
>> stafflist (get the staff coordinates)    
>> resize_rate (get the gap each staff coordinates rate)   
>> resize_img_path (resize sheet music to resize-rate)   
>> resize_stafflist (get the gap of resize staff coordinates)   
>> divideimglist (cut each staff image)   
>> checklinklist (find group of notes)   
>> harmolist (find chord notes)   
>> scale_note_list (list of base chord notes)
>> change_list (list of change chord notes)

Tempo Recognition(DEEP LEARNING)
> tempo_classification (get the tempo)   
>> possible to classification half, quarter, eight, sixteenth note    
>> classification according to the direction of the note's tail   

 
