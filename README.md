# charm-remapper
Script only for X Window System.
Help to change case of text or remap letters following current layout.

## Description
It is script which must be setted to hotkeys for correct work. 
It have such abilities as change selected text to *upper*, *lower* or *switch case*. Also this script remap chars according current layout. This help you fluent change miswritten text and rewrite it.

## Usage

**NOTE:** this is specified as program only for usage with hotkeys because you must run program when text which must be edited is selected. 

```
  SYNOPSIS
    python remapper.py [OPTIONS]
    
  OPTIONS
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
```

## Instalation

### Dependencies
```
X-Server  : X11
Utility   : xclip
Program   : xkblayout-state
```
**NOTE**: All of the above requirements must be met on your computer.

**LINKS:**

[xclip](https://github.com/astrand/xclip) needed for comunication beetween primary section and clipboard

[xkblayout-state](https://github.com/nonpop/xkblayout-state) needed for change keyboard layout and get layouts name


### Setup
Make git clone of this repo. 
Run ```chmod u+x remaper.py```
Set hotkeys for necessary options.

*Example of command/URL, setted as custom hotkeys action:*
```/path/to/script/remapper.py -s```
