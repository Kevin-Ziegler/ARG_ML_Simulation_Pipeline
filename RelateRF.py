import os
import subprocess
import sys

dir = sys.argv[1]
cores = sys.argv[2]
dirSimulated = sys.argv[3]
length = sys.argv[4]
dirScript = sys.argv[5]
whichPython = sys.argv[6]

for i in range(1, int(cores)+1):
	file = dir + "Core" + str(i) + "/"
	#print("cd " + file
	x = subprocess.check_output(["cd", file], shell=True)
	#x2 = subprocess.check_output(["ls | grep .trees > ListTreeFiles.txt"], shell=True)
	line2 = "ls " + file + " | grep .trees$ > " + file + "ListTreeFiles.txt"

	try:
		x2 = subprocess.check_output([line2], shell=True)
	except Exception as e:
		print(e)
	#print(x2)
	print(whichPython + " " + dirScript + "RelateConverter_RF2.py " + file + "ListTreeFiles.txt " + file + " " + file +"result_RF3 " + dirSimulated + " " + length + " " + dirScript)


