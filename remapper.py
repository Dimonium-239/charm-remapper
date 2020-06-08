#!/usr/bin/env python3.8

import os, signal
import sys
import subprocess 
import logging
import time
import pyautogui
import clipboard

logging.basicConfig(filename='remapper.log', format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')
class Remapper: 
    def __init__(self):
        self.qwertyLat = 'QWERTYUIOP[]{}\\ASDFGHJKL;:\'"ZXCVBNM,.//'
        self.qwertyLat += self.qwertyLat.lower()
        self.qwertyCirr ='ЙЦУКЕНГШЩЗХЪХЪ/ФЫВАПРОЛДЖЖЭЭЯЧСМИТЬБЮ.,'
        self.qwertyCirr += self.qwertyCirr.lower()


    def main(self, argv):
        if len(argv) == 2:
            if argv[1] == '-h':
                print(f'{argv[0]} [-u | -r]')
                sys.exit()
            elif argv[1] in ('-u', '--upper'):
                self.__sizeChanger(upper=True)
            elif argv[1] in ('-l', '--lower'):
                self.__sizeChanger(low=True)
            elif argv[1] in ('-sc', '--swapcase'):
                self.__sizeChanger(swapcase=True)
            elif argv[1] in ('-r', '--remapper'):
                print('remapper')

    def __sizeChanger(self, upper=False, low=False, swapcase=False):
        
        var = self.getSelectedText()

        if upper:
            var = var.upper()
        if low:
            var = var.lower()
        if swapcase:
            var = var.swapcase()

        self.setClipboardData(bytes(var, encoding = 'utf-8') )
        
        pyautogui.hotkey('ctrl', 'v')

        subprocess.Popen(['killall', 'xclip'])


    def getSelectedText(self):
        selectedText = subprocess.Popen(['xclip', '-o'], stdout=subprocess.PIPE) 
        selectedText.wait()
        data = selectedText.stdout.read()
        return data.decode("utf-8") 

    def getClipboardData(self):
        p = subprocess.Popen(['xclip','-selection', 'clipboard', '-o'], stdout=subprocess.PIPE)
        retcode = p.wait()
        data = p.stdout.read()
        return data

    def setClipboardData(self, data):
        p = subprocess.Popen(['xclip','-selection','clipboard'], stdin=subprocess.PIPE)
        p.stdin.write(data)
        p.stdin.close()
        retcode = p.wait()

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
        lytBefor = lytBeforProc.communicate()[0].decode("utf-8") 
        lytBeforProc.poll()
        lytBefor = lytBefor[1:-1]

        changer = subprocess.Popen(['xkblayout-state', 'set', '+1'])
        changerEx = changer.poll()

        var = ''

        lytAfterProc = subprocess.Popen(['xkblayout-state', 'print', '"%n"'], stdout=subprocess.PIPE) #setxkbmap
        lytAfter = lytAfterProc.communicate()[0].decode("utf-8") 
        lytAfterProc.poll()
        lytAfter = lytAfter[1:-1]

        selectedText = subprocess.Popen(['xsel'], stdout=subprocess.PIPE) 
        var = selectedText.communicate()[0].decode("utf-8") 
        var = var
        print(var)
        stCode = selectedText.poll()


        rightDecode = ''                                     
        print(lytBefor, 'Polish')
        if lytBefor == 'Polish':
            rightDecode = self.decodeIt(var, self.qwertyLat, self.qwertyCirr)
            
        if lytBefor == 'Russian' or lytBefor == 'Ukrainian':
            rightDecode = self.decodeIt(var, self.qwertyCirr, self.qwertyLat)

        ctrlV = subprocess.Popen(['xdotool', 'getactivewindow', 'windowfocus', 'type', rightDecode], stdout=subprocess.PIPE, \
                                    stderr=subprocess.PIPE)  #'getactivewindow', 'windowfocus', 
        ctrlV.wait()
        ex = ctrlV.poll()


if __name__ == "__main__" :
    rmpr = Remapper()    
    rmpr.main(sys.argv)
    #rmpr.remapper()
    quit(0)
