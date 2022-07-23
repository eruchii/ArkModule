from __init__ import *

def main():
	ark = Arknights()
	script = [("finish_star", 3), ("start_story", 10), ("mission_start", 10), ("finish_star", 600)]
	for i in range(0,11):
		print(i)
		for action, time in script:
			print("Wait {}".format(action))
			f = ark.wait_touch(action, time, 0.9)
			if(f):
				print("Found {}".format(action))
			else:
				if(action == "mission_start"):
					break
				if(action == "finish_star"):
					f = ark.wait_touch(action, time, 0.9)
					if(f):
						print("Found {}".format(action))
				print("Not Found {}".format(action))

if __name__ == '__main__':
	main()