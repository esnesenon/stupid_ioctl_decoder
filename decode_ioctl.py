#!/usr/bin/env python

import os, sys

usage = """"Usage: decode_ioctl.py [ioctl_code]
Example: {} 0x50505050
If ioctl_code argument is not given, will loop and prompt for ioctl codes."
""" #.format(sys.argv[0])

ACCESS_TYPE_DICT = {0x00:'FILE_ANY_ACCESS',
					0x01:'FILE_READ_ACCESS',
					0x02:'FILE_WRITE_ACCESS',
					0x03:'FILE_READ_ACCESS | FILE_WRITE_ACCESS'}

METHOD_TYPE_DICT = {0x00:'METHOD_BUFFERED',
					0x01:'METHOD_IN_DIRECT',
					0x02:'METHOD_OUT_DIRECT',
					0x03:'METHOD_NEITHER'}			
					
def format_print_ioctl(ioctl, dev, access, func, method):
	print("IOCTL code 0x{:08x}:".format(ioctl))
	print("Device code: 0x{:04x}".format(dev))
	print("Access code: 0x{:02x} [{rep}]".format(access, rep=ACCESS_TYPE_DICT[access]))
	print("Function code: 0x{:04x}".format(func))
	print("Method type: 0x{:02x} [{rep}]".format(method, rep=METHOD_TYPE_DICT[method]))
	print("\n")
					
def ioc_decode(ioctl):
	if ioctl > 0xffffffff:
		print("Invalid IOCTL code: must be 0 < ioctl < 0xffffffff")
		return
		
	device_code   = (ioctl & 0xffff0000) >> 16
	access_code   = (ioctl & 0x0000c000) >> 14
	function_code = (ioctl & 0x00003ffc) >> 2
	method_code   = (ioctl & 0x00000003)
	
	format_print_ioctl(ioctl, device_code, access_code, function_code, method_code)

ioctl_code = None
if len(sys.argv) > 2:
	print(usage)
elif len(sys.argv) == 2:
	ioctl_code = int(sys.argv[1], 16)
	ioc_decode(ioctl_code)
	exit(0)
	
while True:
	try:
		ioctl_code = input("Enter a ioctl code (ie. 0x5349e0e0): ")
	except (NameError, SyntaxError):
		print("Invalid IOCTL code: must be 0 < ioctl < 0xffffffff")
		continue
		
	ioc_decode(ioctl_code)