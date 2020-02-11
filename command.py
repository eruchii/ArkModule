import os
import subprocess

def connect(ip = ""):
	cmd = ['adb','connect', ip]
	subprocess.Popen(cmd)

def execIp(args, ip = ""):
	cmd = ['adb', '-s', ip, 'exec-out'] + args.split(' ')
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	return process.communicate()[0]
def exec(args):
	cmd = ['adb','exec-out'] + args.split(' ')
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	return process.communicate()[0]

def tapIp(x,y, ip = ""):
	cmd = ['adb','-s', ip, 'shell', 'input', 'tap', str(x), str(y)]
	subprocess.Popen(cmd)
def tap(x,y):
	cmd = ['adb','shell', 'input', 'tap', str(x), str(y)]
	subprocess.Popen(cmd)