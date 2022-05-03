#!/usr/bin/env python3
import os
import argparse


class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

header = bcolors.BLUE + """
===================================================================================================
████████╗███████╗██╗  ██╗████████╗    ████████╗ ██████╗     ██╗███╗   ███╗ █████╗  ██████╗ ███████╗    
╚══██╔══╝██╔════╝╚██╗██╔╝╚══██╔══╝    ╚══██╔══╝██╔═══██╗    ██║████╗ ████║██╔══██╗██╔════╝ ██╔════╝    
   ██║   █████╗   ╚███╔╝    ██║          ██║   ██║   ██║    ██║██╔████╔██║███████║██║  ███╗█████╗      
   ██║   ██╔══╝   ██╔██╗    ██║          ██║   ██║   ██║    ██║██║╚██╔╝██║██╔══██║██║   ██║██╔══╝      
   ██║   ███████╗██╔╝ ██╗   ██║          ██║   ╚██████╔╝    ██║██║ ╚═╝ ██║██║  ██║╚██████╔╝███████╗    
   ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═╝          ╚═╝    ╚═════╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝ 
                                                                                          by Trefle
====================================================================================================
""" + bcolors.ENDC

def print_with_colors(Text_str, color):
    print(color + Text_str + bcolors.ENDC)

# Parser init
parser = argparse.ArgumentParser(description=bcolors.GREEN + "A simple python script to generate image from text and get reverse shells (exploiting text recognition for example)" + bcolors.ENDC)

# first argument, required: the IP of the listener
parser.add_argument('-iP','--adress', help=bcolors.GREEN +'IP'+ bcolors.ENDC+' adress of the listener', required=True)

# listener choice
help_str = "listener (default: nc), available listeners: \n"
help_str += bcolors.GREEN + "  [-] nc\n"
help_str += "  [-] ncat\n"
help_str += "  [-] ncat_TLS\n"
help_str += "  [-] socat_TTY\n" + bcolors.ENDC
parser.add_argument('-l','--listener', help=help_str)

# name of the image file to be supplied for modification
parser.add_argument('-f','--file', help=bcolors.GREEN +'Name'+bcolors.ENDC+' of the image file to modify', required=True)

# Port argument, I usually use 4444 so this is why this is the default
parser.add_argument('-p','--port', help=bcolors.GREEN +'Port'+bcolors.ENDC+' that you wish to use for the listener (default: 4444)')

# text file to be converted
parser.add_argument('-pf','--payload-file', help=bcolors.GREEN +'text file'+bcolors.ENDC+'to convert, use '+bcolors.WARNING +'^IP^'+bcolors.ENDC+' and '+bcolors.WARNING +'^PORT^'+bcolors.ENDC+' to define the IP and Port positions', required=True)

# font choice
parser.add_argument("-fo", "--font", help=bcolors.GREEN +'Font'+bcolors.ENDC+" to be used for the text in the image (default: helvetica)")

def Parse_args():
    # let's get all the arguments
    args = vars(parser.parse_args())
    IP = args["adress"]

    if args["listener"]:
        listener = args["listener"]
    else:
        listener = "nc"

    OutputFileName = args["file"]

    if args["port"]:
        Port = args["port"]
    else:
        Port = "4444"

    if args["font"]:
        font_choice = args["font"]
    else:
        font_choice = "helvetica"

    return IP, Port, OutputFileName, payload_file, listener, font

if __name__ =="__main__":
    print(header)
    IP, Port, OutputFileName, payload_file, Listener, font = Parse_args()