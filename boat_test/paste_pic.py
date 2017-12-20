 #-*- coding: UTF-8 -*- 
 
import os
from PIL import Image

UNIT_WIDTH = 465 # img width 
UNIT_HEIGHT = 142 # img height

filepath = 'xxx%s.jpg'
resPath = 'xxx%snd.jpg'

def gridview(images,name):
    target = Image.new('RGB', (UNIT_WIDTH*3, UNIT_HEIGHT*13))   # result is 3*13
    for x in xrange(0,39):
        if x < 13:
            area = (0,UNIT_HEIGHT * x,UNIT_WIDTH,(x + 1) * UNIT_HEIGHT)
        elif x < 26:
            area = (UNIT_WIDTH,UNIT_HEIGHT * (x-13),2 * UNIT_WIDTH,(x + 1-13)* UNIT_HEIGHT)
        elif x < 39:
            area = (2 * UNIT_WIDTH,UNIT_HEIGHT * (x-26),3 * UNIT_WIDTH,(x + 1 - 26)* UNIT_HEIGHT)
        
        try:
            my = Image.open(images[x])
        except Exception as e:
            break
            print e
        finally:
           target.paste(my,area)

    target.save(name,'jpeg')

for t in range(1,7):
    L = [filepath % x for x in range(39 * (t-1) + 1,39 * t + 1)]
    gridview(L,resPath % t)
# print L
