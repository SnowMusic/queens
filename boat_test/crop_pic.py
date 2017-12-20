 #-*- coding: UTF-8 -*- 
 
import os
from PIL import Image

totalSize = 201
picpath = 'xxx%s.jpg'
newname ='xxx_%s.jpg'

for x in xrange(2,totalSize):
	name = picpath%x
	im = Image.open(name)

	# question position
	question = (80, 298, 545, 440)
	region = im.crop(question)

	# title order position
	title = (325,120,390,140)
	re = im.crop(title)
	region.paste(re,title)
	region.save(newname%x,'jpeg')
	print x