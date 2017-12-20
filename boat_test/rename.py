 #-*- coding: UTF-8 -*- 
 
import os


filepath = 'xxx/newtest3'
pathDir =  os.listdir(filepath)
count = 0
for singleDir in pathDir:
    # child = os.path.join('%s%s' % ('', singleDir))
    print singleDir
    os.rename(os.path.join(filepath,singleDir),os.path.join(filepath,str(count)+".jpg"))
    count +=1
    # print child