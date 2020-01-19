# Text Mode Graphic [TMG]

### *Image* file format for [elfboot](https://github.com/croemheld/elfboot).
elfboot is a text-based boot loader that cannot load and print normal image files. However, in order to display images, the ASCII character 220 (bottom half block) &lhblk;, a background color and the foreground color are used to paint two *pixels* per text character.

These colors are available in text mode: [color table](https://wiki.osdev.org/Printing_To_Screen#Color_Table)


#### File schematic: (work in progress)
```
   +--------------------------+
   |                          | Header 
   +--------------------------+
   | dc fc dc ff dc a3 ...    | Body
   |                          |
   |                          |
   +--------------------------+
```

`dc ff dc ff dc a3` <- this are six pixel   
   
`dc` <- 220 <- ascii value: &lhblk;   
`fc` <- `f`: 15 = white background, `c`: 12 = light red foreground (&lhblk;)   
   
...   



### How to use tmg.py:

```
usage: tmg.py [-h] -i INPUT -o OUTPUT [-a] [-r RANGE]

Create *.tmg files for elfboot 

required arguments:
  -i INPUT, --input INPUT
                        path of input file (has to be a *.png file)
  -o OUTPUT, --output OUTPUT
                        path of output file

optional arguments:
  -h, --help            show this help message and exit
  -a, --ascii           add ascii 220 ▄ to file
  -r RANGE, --range RANGE
                        change range of rgb values, try it (values from 0-6)

```
##### Requirements: 
- __required:__
    - python3   
    - pip3    
        - [pillow](https://python-pillow.org/)
- __optional:__
    - gimp   
