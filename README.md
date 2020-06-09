# chars-general
Script only for X Window System.
Help to change case of text or remap letters following current layout.

# Description
It is script which must be setted to hotkeys for correct work. 
It have such abilities as change selected text to *upper*, *lower* or *switch case*. Also this script remap chars according current layout. This help you fluent change miswritten text and rewrite it.

# Usage
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
# Instalation
## Dependencies

**X-Server:   X11**
**Utility:  (xclip)[https://github.com/astrand/xclip]**
**Program:  (xkblayout-state)[https://github.com/nonpop/xkblayout-state]**

All of the above requirements must be met on your computer.

## Setup
Make git clone of this repo. 
Run ```chmod u+x remaper.py```
Set hotkeys for necessary options.

*Example:*
```/path/to/script/remapper.py -s```
