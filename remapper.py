#!/usr/bin/env python3.8

import os, sys, signal
import subprocess 
import pyautogui
import json 
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Remapper: 
    def __init__(self, argv):
        if len(argv) == 2:
            if argv[1] in ('-h', '--help'):
                print(f'''{argv[0]} [OPTIONS]
        -h, --help
            Show short info about options
        -u, --upper
            Set selected text to upper case
        -l, --lower
            Set selected text to lower case
        -s, --swapcase
            Swap case of selected text
        -r, --remapper
            Remap chars of selected text following current layout
                    ''') 
                sys.exit()
            elif argv[1] in ('-u', '--upper'):
                self.__sizeChanger(upper=True)
            elif argv[1] in ('-l', '--lower'):
                self.__sizeChanger(low=True)
            elif argv[1] in ('-s', '--swapcase'):
                self.__sizeChanger(swapcase=True)
            elif argv[1] in ('-r', '--remapper'):
                self.remapper()
            elif argv[1] in ('-a', '--add'):
                self.addNewLayoutCLI()
            else:
                print(f'Try \'{argv[0]} -h\' for more information.')


    def __sizeChanger(self, upper=False, low=False, swapcase=False):
        
        clipBuff = self.xcliper(fromClipboard=True)
        var = self.xcliper(fromPrimary=True)

        if upper:
            var = var.upper()
        if low:
            var = var.lower()
        if swapcase:
            var = var.swapcase()

        self.xcliper(var=var, toClipboard=True)
        pyautogui.hotkey('ctrl', 'v')
        self.xcliper(var=clipBuff, toClipboard=True)

    def xcliper(self, var='', fromPrimary=False, fromClipboard=False, toClipboard=False):   
        if fromPrimary:
            selectedText = subprocess.Popen(['xclip', '-o'], stdout=subprocess.PIPE)  
            return selectedText.communicate()[0].decode("utf-8") 
        elif fromClipboard:
            selectedText = subprocess.Popen(['xclip' ,'-out', '-selection', 'clipboard'], \
                                stdout=subprocess.PIPE)  
            return selectedText.communicate()[0].decode("utf-8") 
        elif toClipboard:
            ctrlC = subprocess.Popen(['xclip', '-selection', 'c'], stdin=subprocess.PIPE)
            ctrlC.communicate(bytes(var, encoding='utf8'))
            ctrlC.wait()

    # TODO: make normal remapper :) 

    def decodeIt(self, var, qwerty1, qwerty2):
        rightDecode = ''
        for char in var:
            try:
                index = qwerty1.index(char)
                rightDecode += qwerty2[index]
            except ValueError:
                rightDecode += char
        return rightDecode 


    def getLayoutLang(self):
        lytBeforProc = subprocess.Popen(['xkblayout-state', 'print', '"%n"'], stdout=subprocess.PIPE) #setxkbmap
        lytBefor = lytBeforProc.communicate()[0].decode("utf-8")[1:-1]
        lytBeforProc.poll()
        return lytBefor

    def getLayoutJSON(self):
        with open('layouts.json') as f:
            data = json.load(f)
        return data


    def addNewLayoutCLI(self):
        layout_dict = self.getLayoutJSON()
        new_ley = ''
        msg = f'''
Here is CLI for adding new layout. You will get example from english qwerty layout
and you have to click every button with letters step by step from {bcolors.BOLD}top left corner{bcolors.ENDC} 
to {bcolors.BOLD}bottom rigth corner (did not press '[~|`]'){bcolors.ENDC} there must be {bcolors.BOLD}{len(layout_dict['English'])} letters{bcolors.ENDC} ,
not more not less. If you use language where is more than {bcolors.BOLD}{len(layout_dict['English'])} letters{bcolors.ENDC} 
unfortunatly this version of programm did not support it, 
but you can input all characters without 'Alt'.
            '''
        print(msg)
        while True:
            inputStrLen = len(f'({self.getLayoutLang()})>')
            print(' '*inputStrLen + bcolors.WARNING +layout_dict['English'] + bcolors.ENDC)
            new_ley = input(f'({bcolors.OKBLUE}{self.getLayoutLang()}{bcolors.ENDC})>')
            if(len(new_ley) == len(layout_dict['English']) and input('Save this layout ? ' + f'[{bcolors.UNDERLINE}Y{bcolors.ENDC}/N]\n') not in ('Y', 'y', 'yes')):
                break
            else:
                print(f'\n{bcolors.FAIL}ERROR: You must map one letter from your layout to one letter from example{bcolors.ENDC}')
                if(input('Do you want continue ? ' + f'[{bcolors.UNDERLINE}Y{bcolors.ENDC}/N]\n') in ('Y', 'y', 'yes')):
                    break
                
        print(new_ley)



    def remapper(self):

        pass
        # TODO: smthing with this mess!!!

        #print(data[lytBefor])

        #subprocess.Popen(['killall', 'xkblayout-state'])

        # lytBefor = lytBefor[1:-1]

        # changer = subprocess.Popen(['xkblayout-state', 'set', '+1'])
        # changerEx = changer.poll()

        # var = ''

        # lytAfterProc = subprocess.Popen(['xkblayout-state', 'print', '"%n"'], stdout=subprocess.PIPE) #setxkbmap
        # lytAfter = lytAfterProc.communicate()[0].decode("utf-8") 
        # lytAfterProc.poll()
        # lytAfter = lytAfter[1:-1]

        # selectedText = subprocess.Popen(['xsel'], stdout=subprocess.PIPE) 
        # var = selectedText.communicate()[0].decode("utf-8") 
        # var = var
        # print(var)
        # stCode = selectedText.poll()


        # rightDecode = ''                                     
        # print(lytBefor, 'Polish')
        # if lytBefor == 'Polish':
        #     rightDecode = self.decodeIt(var, self.qwertyLat, self.qwertyCirr)
            
        # if lytBefor == 'Russian' or lytBefor == 'Ukrainian':
        #     rightDecode = self.decodeIt(var, self.qwertyCirr, self.qwertyLat)

        # ctrlV = subprocess.Popen(['xdotool', 'getactivewindow', 'windowfocus', 'type', rightDecode], stdout=subprocess.PIPE, \
        #                             stderr=subprocess.PIPE)  #'getactivewindow', 'windowfocus', 
        # ctrlV.wait()
        # ex = ctrlV.poll()

if __name__ == "__main__" :
    subprocess.Popen(['killall', 'xclip'])
    rmpr = Remapper(sys.argv)    
    #rmpr.main()
    quit(0)
