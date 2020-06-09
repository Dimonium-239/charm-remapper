#!/usr/bin/env python3.8

import os, sys, signal
import subprocess 
import pyautogui
import json 

class Remapper: 
    def __init__(self):
        self.qwertyLat = 'QWERTYUIOP[]{}\\ASDFGHJKL;:\'"ZXCVBNM,.//'
        self.qwertyLat += self.qwertyLat.lower()
        self.qwertyCirr ='ЙЦУКЕНГШЩЗХЪХЪ/ФЫВАПРОЛДЖЖЭЭЯЧСМИТЬБЮ.,'
        self.qwertyCirr += self.qwertyCirr.lower()


    def main(self, argv):
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
            else:
                print(f'Try \'{argv[0]} -h\' for more information.')

    def __sizeChanger(self, upper=False, low=False, swapcase=False):
        
        var = self.xcliper(fromPrimary=True)

        if upper:
            var = var.upper()
        if low:
            var = var.lower()
        if swapcase:
            var = var.swapcase()

        self.xcliper(var=var, toClipboard=True)


    def xcliper(self, var='', fromPrimary=False, toClipboard=False):   
        if fromPrimary:
            selectedText = subprocess.Popen(['xclip', '-o'], stdout=subprocess.PIPE)  
            return selectedText.communicate()[0].decode("utf-8") 
        elif toClipboard:
            ctrlC = subprocess.Popen(['xclip', '-selection', 'c'], stdin=subprocess.PIPE)
            ctrlC.communicate(bytes(var, encoding='utf8'))
            ctrlC.wait()

            pyautogui.hotkey('ctrl', 'v')
    
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

    def remapper(self):

        lytBeforProc = subprocess.Popen(['xkblayout-state', 'print', '"%n"'], stdout=subprocess.PIPE) #setxkbmap
        lytBefor = lytBeforProc.communicate()[0].decode("utf-8")[1:-1]
        lytBeforProc.poll()
        print(lytBefor)
        with open('layouts.json') as f:
            data = json.load(f)
        
        print(data[lytBefor])
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
    rmpr = Remapper()    
    rmpr.main(sys.argv)
    quit(0)
