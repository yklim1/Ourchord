def harmonysearch(notelist):

    for i in range(len(notelist)):
        num = 1

        if(notelist[i][5] == 0):
            continue
        
        for ck in range(1,5):
            
            if(i+ck >= len(notelist)-1):
                if(notelist[i+ck-1][5] != 1):
                    notelist[i+ck][5] = 0
                    break
                
                else:
                    break
            
            if(abs(notelist[i][0]-notelist[i+ck][0])<3):
                num = num + 1
                notelist[i][5]=num
                notelist[i+ck][5]=0
                
            else:
                notelist[i][5] = num
                break
    #print(notelist)
    return notelist
