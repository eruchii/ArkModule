import time
from __init__ import *

def main():
    ark = Arknights()
    farming = False
    start = None
    while(1):
        type, reg = ark.detect_screen("seaborn")
        if(type != None):
            if(not farming):
                print(type, reg)
            if(type in ["start", "mission_start", "finish"]):
                farming = False
                ark.touch(reg)
            if(type in ["farming"]):
                farming = True
                ark.sleep(1)
        ark.sleep(1)

if __name__ == '__main__':
	main()