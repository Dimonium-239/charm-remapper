# charm-remapper
Script is for any system with an X11 implementation.
Help to change case of text or remap letters following current layout.

## Description
It is script which must be setted to hotkeys for correct work. 
It have such abilities as change selected text to *upper*, *lower* or *switch case*. Also this script remap chars according current layout. This help you fluent change miswritten text and rewrite it.

**For me good hotkeys was:**
  - <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>1</kbd> -- for remapper
  - <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>2</kbd> -- for upper
  - <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>3</kbd> -- for lower
  - <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>4</kbd> -- for swapcase
  - <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>5</kbd> -- for capitalize
  
## Demonstration
- Remapper in action:

![Remapper in action](https://i.imgur.com/eJEx9Ue.gif)

- Adding new layout:

![Adding new layout](https://i.imgur.com/g9kYXZO.gif)


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
    -c, --capitalize
        Change all first letters of selected text to capital leters
    -a, --add
        Added new layout to file
```

## Instalation

### Dependencies
```
X-Server  : any implementation of X11
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

### License
MIT License

See ```LICENSE.md``` for detail information.
