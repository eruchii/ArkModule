import cv2
import numpy
import random
import time
import json
import command

class Region:
	x, y, w, h = 0, 0, 0, 0
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
	
	def __repr__(self) -> str:
		return "Region(x={},y={},w={},h={})".format(self.x, self.y, self.w, self.h)

class Image:
	region = None
	uri = None
	type = None
	def __init__(self, js: dict):
		self.uri = js.get("uri")
		if(js.get("region") != None):
			self.region = Region(js["region"][0], js["region"][1], js["region"][2], js["region"][3])
		self.type = js.get("type")

class Arknights:
	def __init__(self, ip = "127.0.0.1:62001"):
		self.ip = ip
		command.connect(ip)
		# print(command.exec('screencap -p', self.ip))
	@staticmethod
	def get_screen(mode = "GRAYSCALE", write = False):
		try:
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
		except Exception:
			return None

	@staticmethod
	def sleep(t = 0.3):
		time.sleep(t)

	@classmethod
	def find(cls, img, threshold = 0.95):
		screen = cls.get_screen()
		if(screen is None):
			return None
		template = cv2.imread('assets/{}.png'.format(img), 0)
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
			time.sleep(0.1)
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
	def touch(region: Region):
		w = random.randint(int(region.w/4)-1, int(region.w*3/4)-1)
		h = random.randint(int(region.h/4)-1, int(region.h*3/4)-1)
		# print("Random location:",int(region.x + w), int(region.y + h))
		command.tap(int(region.x + w), int(region.y + h))

	@classmethod		
	def detect_screen(cls, module = "farming", threshold = 0.95):
		start = time.time()
		screen = cls.get_screen()
		if(screen is None):
			return None
		config = json.load(open("modules/{}.json".format(module), "r"))
		imgs = [Image(x) for x in config]
		
		for img in imgs:
			if(img.region is not None):
				search_img = screen[img.region.y : img.region.y+ img.region.h, img.region.x : img.region.x+ img.region.w]
				new_x = img.region.x
				new_y = img.region.y
			else:
				search_img = screen	
				new_x = 0
				new_y = 0
			template = cv2.imread('assets/{}'.format(img.uri), 0)
			w, h = template.shape[::-1]
			match = cv2.matchTemplate(search_img, template, cv2.TM_CCOEFF_NORMED)
			min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
			if(max_val >= threshold):
				return (img.type, Region(max_loc[0] + new_x, max_loc[1] + new_y, w, h))
		return (None, None)

