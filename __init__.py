import cv2
import numpy
from random import uniform
import time
import os
import subprocess
import command

class Region:
	x, y, w, h = 0, 0, 0, 0
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

class Arknights:
	def __init__(self, ip = None):
		self.ip = ip
	#	command.connect(ip)
	# 	print(command.exec('screencap -p', self.ip))
	@staticmethod
	def get_screen(mode = "GRAYSCALE", write = False):
		img = None
		color = 0
		if(mode == "RGB"):
			color = 1

		while img is None:
			img = cv2.imdecode(
				numpy.frombuffer(
					command.exec('screencap -p'), dtype=numpy.uint8), color)
		if(write):
			cv2.imwrite("pepe.png", img)
		return img

	@staticmethod
	def sleep(t = 0.3):
		time.sleep(t)

	@classmethod
	def find(cls, img, threshold = 0.95):
		screen = cls.get_screen()
		template = cv2.imread('sample/{}.png'.format(img), 0)
		w, h = template.shape[::-1]
		match = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
		if(max_val >= threshold):
			return Region(max_loc[0], max_loc[1], w, h)
		return None

	@classmethod
	def find_touch(cls, img, threshold = 0.95):
		region = cls.find(img)
		if region != None:
			cls.touch(region)
			return True
		return False

	@classmethod
	def wait_find(cls, img, limit = 10,threshold = 0.95):
		start = time.time()
		while(time.time() - start < limit):
			region = cls.find(img, threshold)
			if region != None:
				return region
			if(limit > 60):
				time.sleep(3)
		return None

	@classmethod
	def wait_touch(cls, img, limit = 10, threshold = 0.95):
		region = cls.wait_find(img, limit)
		if region != None:
			cls.touch(region)
			print(int(region.x + region.w/2), int(region.y + region.h/2))
			return True
		return False

	@staticmethod
	def touch(region):
		command.tap(int(region.x + region.w/2), int(region.y + region.h/2))
