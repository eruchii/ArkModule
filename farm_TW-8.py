from __init__ import *

def main():
	ark = Arknights()
	script = [("TW-8", 5), ("start_normal", 5), ("mission_start", 10), ("finish_star", 600)]
	for i in range(0,20):
		print(i)
		for action, time in script:
			print("Wait {}".format(action))
			f = ark.wait_touch(action, time, 0.9)
			if(f):
				print("Found {}".format(action))
			else:
				print("Not Found {}".format(action))

if __name__ == '__main__':
	main()