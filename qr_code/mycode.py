from PIL import Image
import qrcode
import os


channel_file ='site.txt'
f = open(channel_file)
lines = f.readlines()
f.close()

output_dir = 'output/'
if not os.path.exists(output_dir):
   os.mkdir(output_dir)

start = len('http://www.xx.xx?a=app-release-')

for sitename in lines:
	qr = qrcode.QRCode(
		version=2,
		error_correction=qrcode.constants.ERROR_CORRECT_H,
		box_size=6,
		border=2
	)

	qr.add_data(sitename)
	qr.make(fit=True)

	img = qr.make_image()
	img = img.convert("RGBA")

	icon = Image.open("logo.png")

	img_w, img_h = img.size
	factor = 4
	size_w = int(img_w / factor)
	size_h = int(img_h / factor)

	icon_w, icon_h = icon.size
	if icon_w > size_w:
		icon_w = size_w
	if icon_h > size_h:
		icon_h = size_h
	icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

	w = int((img_w - icon_w) / 2)
	h = int((img_h - icon_h) / 2)
	img.paste(icon, (w, h), icon)
	picname = sitename[start:][:-1]
	picname = picname+'.png'
	img.save(output_dir+picname)