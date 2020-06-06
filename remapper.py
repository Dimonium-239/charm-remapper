#!/usr/bin/env python3.8

import os, signal
import subprocess 
import logging
import time

logging.basicConfig(filename='remapper.log', format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')
time.sleep(3)
class Remapper: 
    def __init__(self):
        self.qwertyLat = 'QWERTYUIOP[]{}\\ASDFGHJKL;:\'"ZXCVBNM,.//'
        self.qwertyLat += self.qwertyLat.lower()
        self.qwertyCirr ='ЙЦУКЕНГШЩЗХЪХЪ/ФЫВАПРОЛДЖЖЭЭЯЧСМИТЬБЮ.,'
        self.qwertyCirr += self.qwertyCirr.lower()

#print(qwertyCirr)
#print(qwertyLat) #
#print(len(qwertyCirr) == len(qwertyLat)) ghbdtn vbh

    def decodeIt(self, var, qwerty1, qwerty2):
        rightDecode = ''
        for char in var:
            try:
                index = qwerty1.index(char)
                rightDecode += qwerty2[index]
            except ValueError:
                rightDecode += char
        return rightDecode 

    def mainTask(self):

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
        logging.info('------------------------------')
        logging.info('Word before: \t\t' + var)
        logging.info('Word after : \t\t' + rightDecode)
        logging.info('xdotool exit code: ' + str(ex))
        logging.info('xsel exit code: \t' + str(stCode))
        logging.info('layout change exit code: ' + str(changerEx) + '\n')
        lytBefor = lytAfter

if __name__ == "__main__" :
    rmpr = Remapper()    
    rmpr.mainTask()
    quit(0)
