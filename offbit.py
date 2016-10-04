#!/usr/bin/python

import sys
import os
import getopt
import pefile

version = 'Version 0.1'
finalFile = 'crypted.exe'

def main(argv):
	try:
		opts, args = getopt.getopt(argv, "hVi:o:", ['help', 'version', 'infile', 'outfile'])
	except getopt.GetoptError:
		print 'Usage: ./offbit.py -i <input file> -o <output file> <args>'
		sys.exit(2)
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			print 'Usage: ./offbit.py -i <input file> -o <output file> <args>'
			print 'Command Line Arguments:'
			print '\t-V or --version\t\tShow version info'
			print '\t-h or --help\t\tShow this screen'
			print '\t-i or --infile\t\tSpecify an input file (Must be .exe!)'
			print '\t-o or --outfile\t\tSpecify an output file'
			sys.exit()
		if opt in ('-V', '--version'):
			print 'offbit.py ' + version
			sys.exit()
		if opt in ('-i', '--infile'):
			inputPath = arg
			#strip filename from path
			inputFile = os.path.basename(inputPath)
		if opt in ('-o', '--outfile'):
			finalPath = arg
			#strip filename from path
			finalFile = os.path.basename(finalPath)
	print "[*] Reading '" + inputFile + "'..."
	file = pefile.PE(inputPath)
	print '[*] Entry Point: ' + hex(file.OPTIONAL_HEADER.AddressOfEntryPoint)
	print "[*] Writing to '" + finalFile + "'..."
	out = file.write(finalPath)
	
if __name__ == "__main__":
	main(sys.argv[1:])