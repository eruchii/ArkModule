import os
import cv2

lst = os.listdir("./1920x1080")

for i in lst:
	img = cv2.imread("./1920x1080/"+i, cv2.IMREAD_UNCHANGED)
	scale = 1600/1920

	width = int(img.shape[1] * scale)
	height = int(img.shape[0] * scale)
	dsize = (width, height)
	img_out = cv2.resize(img, dsize)
	
	cv2.imwrite("./1600x900/"+i, img_out)
