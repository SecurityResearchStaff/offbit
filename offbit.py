#!/usr/bin/python

import sys
import os
import getopt
import pefile
import random

version = 'Version 0.1'
finalFile = 'crypted.exe'

def cryptStringTable(file):
	strings = list()

	# Fetch resource directory entry containing strings
	#print [entry.id for entry in file.DIRECTORY_ENTRY_RESOURCE.entries]
	try:
		rt_string_index = [entry.id for entry in file.DIRECTORY_ENTRY_RESOURCE.entries].index(pefile.RESOURCE_TYPE['RT_STRING'])
	except:
		print '[-] String Table not used for this file!'
		return
	# Get directory entry
	
	rt_string_diretory = file.DIRECTORY_ENTRY_RESOURCE.entries[rt_string_index]
	

	# each entry contain a block of 16 strings
	for entry in rt_string_diretory.directory.entries:
		# Get RVA of the string data and size
		data_rva = entry.directory.entries[0].data.struct.OffsetToData
		size = entry.directory.entries[0].data.struct.Size
		#print '[*] Directory entry at RVA ', hex(data_rva), ' of size ', hex(size)

		# Retrieve the actual data and start processing the strings
		data = file.get_memory_mapped_image()[data_rva:data_rva+size]
		offset = 0
		while True:
			# Exit once there's no more data to read
			if offset >= size:
				break
			# Fetch the length of the unicode string
			ustr_length = file.get_word_from_data(data[offset:offset+2], 0)
			offset += 2
			# If the string is empty, skip it
			if ustr_length == 0:
				continue
			# Get the unicode string
			ustr = file.get_string_u_at_rva(data_rva+offset, max_length=ustr_length)
			# Randomly shuffle the string
			ustr = ''.join(random.sample(ustr, ustr_length))
			test = file.set_bytes_at_rva(data_rva+offset, ustr)
			offset += ustr_length * 2
			strings.append(ustr)
			#print '[*] String of length ', ustr_length, ' at offset ', hex(offset)
	print '[+] Successfully encrypted string table!'

def main(argv):
	useStringTable = False
	try:
		opts, args = getopt.getopt(argv, "hVi:o:t", ['help', 'version', 'infile', 'outfile', 'string-table'])
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
			print '\t-t or --string-table\tEncrypt the contents of the string table'
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
		if opt in ('-t', '--string-table'):
			useStringTable = True

	print "[*] Reading '" + inputFile + "'..."
	file = pefile.PE(inputPath)
	print '[*] Entry Point: ' + hex(file.OPTIONAL_HEADER.AddressOfEntryPoint)
	
	if useStringTable:
		cryptStringTable(file)
	
	print "[*] Writing to '" + finalFile + "'..."
	out = file.write(finalPath)
	
if __name__ == "__main__":
	main(sys.argv[1:])