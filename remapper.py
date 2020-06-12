#!/usr/bin/env python

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
        -c, --capitalize
            Change all first letters of selected text to capital leters
        -a, --add
            Added new layout to file
                    ''') 
                sys.exit()
            elif argv[1] in ('-u', '--upper'):
                self.selectedTextChanger(upper=True)
            elif argv[1] in ('-l', '--lower'):
                self.selectedTextChanger(low=True)
            elif argv[1] in ('-s', '--swapcase'):
                self.selectedTextChanger(swapcase=True)
            elif argv[1] in ('-r', '--remapper'):
                self.selectedTextChanger(remapper=True)
            elif argv[1] in ('-c', '--capitalize'):
                self.selectedTextChanger(capitalize=True)
            elif argv[1] in ('-a', '--add'):
                self.addNewLayoutCLI()
            else:
                print(f'Try \'{argv[0]} -h\' for more information.')


    def selectedTextChanger(self, upper=False, low=False, swapcase=False, remapper=False, \
                                    capitalize=False):
        
        clipBuff = self.xcliper(fromClipboard=True)
        var = self.xcliper(fromPrimary=True)

        if upper:
            var = var.upper()
        if low:
            var = var.lower()
        if swapcase:
            var = var.swapcase()
        if remapper:
            qwerty1 = self.getLayoutLang()
            changer = subprocess.Popen(['xkblayout-state', 'set', '+1']) 
            changer.poll()
            qwerty2 = self.getLayoutLang()
            var = self.decodeIt(var, qwerty1, qwerty2)
        if capitalize:
            var = ' '.join([a[0].upper() + a[1:] for a in var.split(' ')])

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


    def decodeIt(self, var, lang1, lang2):
        layout_dict = self.getLayoutJSON()
        if lang1 in layout_dict and lang2 in layout_dict:
            qwerty1 = layout_dict[lang1] 
            qwerty2 = layout_dict[lang2]
            qwerty1 += qwerty1.swapcase()
            qwerty2 += qwerty2.swapcase()
            rightDecode = ''
            for char in var:
                try:
                    index = qwerty1.index(char)
                    rightDecode += qwerty2[index]
                except ValueError:
                    rightDecode += char
            return rightDecode 
        else:
            return var


    def getLayoutLang(self):
        lytBeforProc = subprocess.Popen(['xkblayout-state', 'print', '"%n"'], stdout=subprocess.PIPE) #setxkbmap
        lytBefor = lytBeforProc.communicate()[0].decode("utf-8")[1:-1]
        lytBeforProc.poll()
        return lytBefor

    def getLayoutJSON(self):
        with open(os.path.dirname(sys.argv[0]) + '/layouts.json') as f:
            data = json.load(f)
        return data

    def writeLayoutToJSON(self, data): 
        with open(os.path.dirname(sys.argv[0]) + '/layouts.json', 'w', encoding='utf8') as f: 
            json.dump(data, f, indent=4) 

    def addNewLayoutCLI(self):
        layout_dict = self.getLayoutJSON()
        new_ley = ''
        startedLayout = self.getLayoutLang()
        if startedLayout not in layout_dict:
            msg = f'''
Here is CLI for adding new layout. You will get example from English qwerty layout
and you have to click every button with letters step by step from {bcolors.BOLD}top left corner{bcolors.ENDC} 
to {bcolors.BOLD}bottom rigth corner (do not press '[~|`]'){bcolors.ENDC} there must be {bcolors.BOLD}{len(layout_dict['English'])} letters{bcolors.ENDC} ,
not more not less. If you use language where is more than {bcolors.BOLD}{len(layout_dict['English'])} letters{bcolors.ENDC} 
unfortunatly this version of programm does not support it, 
but you can input all characters without 'Alt'.
                '''
            print(msg)
            while True:
                if self.getLayoutLang() in layout_dict:
                    print(f'{bcolors.FAIL}ERROR: layout changed to one whitch is present in the base. Program halted {bcolors.ENDC}')
                    break
                inputStrLen = len(f'({startedLayout})>')
                print(' '*inputStrLen + bcolors.OKGREEN +layout_dict['English'] + bcolors.ENDC)
                new_ley = input(f'({bcolors.OKBLUE}{self.getLayoutLang()}{bcolors.ENDC})>')
                
                if startedLayout != self.getLayoutLang() and self.getLayoutLang() not in layout_dict:
                    print(f'\n{bcolors.WARNING}WARNING: layout changed from {startedLayout} to {self.getLayoutLang()} {bcolors.ENDC}\n')
                    startedLayout= self.getLayoutLang()
                    continue
                elif(len(new_ley) == len(layout_dict['English']) and input('Save this layout ? ' + f'[{bcolors.UNDERLINE}Y [1]{bcolors.ENDC}/N [0]]\n') not in ('N', 'n', 'no', '0')):
                    print(new_ley)
                    layout_dict[startedLayout] = new_ley
                    self.writeLayoutToJSON(layout_dict)
                    print(f'{startedLayout} layout is succesfully added, now you can use this program with -r option')
                    break
                else:
                    print(f'\n{bcolors.FAIL}ERROR: You must map one letter from your layout to one letter from example{bcolors.ENDC}')
                    if(input('Do you want to continue ? ' + f'[{bcolors.UNDERLINE}Y [1]{bcolors.ENDC}/N [0]]\n') in ('N', 'n', 'no', '0')):
                        break
        else:
            print(f'{bcolors.WARNING}Such layout is present in the base{bcolors.ENDC}') 


if __name__ == "__main__" :
    subprocess.Popen(['killall', 'xclip'])
    rmpr = Remapper(sys.argv)    