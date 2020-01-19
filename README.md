# Text Mode Graphic [TMG]

### Image file format for [elfboot](https://github.com/croemheld/elfboot).
elfboot is a bootloader for the x86 architecture which uses VGA video mode 3 for displaying information. Since a bootloader usually resides in the first 64 KB of memory, loading and displaying images might waste precious memory.
The TMG project aims to drastically reduce image files by only using the [16 available colors](https://wiki.osdev.org/Printing_To_Screen#Color_Table) in VGA video mode 3 and the ASCII/Code Page 737 character 220 (bottom half block &lhblk;).

#### VGA video mode 3 font
Usually, VGA video mode 3 uses 9x16 pixels for each glyph. Since an image consists of square pixels, we use the &lhblk; glyph to cover half of the area, which results in two vertically stacked pixels. By using the attribute byte of screen character, we can color both "pixels" by defining the foreground color for the bottom and the background color for the top half of the glyph.

```
    __ __ __ __ __ __ __ __ __
   |                          |
   |                          |
   |                          |
   |        Background        |
   |                          |
   |                          |
   |                          |
   |                          |
   ----------------------------
   |                          |
   |                          |
   |                          |
   |       Code Page 737      |
   |       Character 220      |
   |                          |
   |                          |
   |__ __ __ __ __ __ __ __ __|
```


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
