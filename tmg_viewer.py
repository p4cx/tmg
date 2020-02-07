import argparse
import os
import sys


color_table = [
    ('white',         '40',   '30',   15),
    ('yellow',        '103',  '93',   14),
    ('light purple',  '105',  '95',   13),
    ('light red',     '101',  '91',   12),
    ('light cyan',    '106',  '96',   11),
    ('light green',   '102',  '92',   10),
    ('light blue',    '104',  '94',   9),
    ('dark grey',     '100',  '90',   8),
    ('grey',          '47',   '37',   7),
    ('brown',         '43',   '33',   6),
    ('purple',        '45',   '35',   5),
    ('red',           '41',   '31',   4),
    ('cyan',          '46',   '36',   3),
    ('green',         '42',   '32',   2),
    ('blue',          '44',   '34',   1),
    ('black',         '107',  '97',   0)
]


def get_color(position, orig_color):
    for color in color_table:
        if orig_color is color[3]:
            if position is 'bg':
                return color[1]
            else:
                return color[2]


def get_value(number):
    if number is 32:
        return ' '
    elif number is 220:
        return u'\u2584'
    elif number is 219:
        return u'\u2588'
    elif number is 223:
        return u'\u2580'
    else:
        return ' '


def preview(input_path, debug):
    with open(input_path, 'rb') as f:
        header_raw = f.read(3)
        if header_raw == b'TMG':
            header = header_raw.decode('ascii')
            version = ord(f.read(1))
            mode = ord(f.read(1))
            alpha_color = ord(f.read(1))
            width = ord(f.read(1))
            height = ord(f.read(1))

            if debug:
                print('\033[41;30m DEBUG \033[39m')
                print(' \033[31mPATH                   :  ' + input_path + '\033[39m')
                print(' \033[31mSIZE            (Bytes):  ' + str(os.path.getsize(args.input)) + '\033[39m')
                print(' \033[31mTAG           (3 Bytes):  ' + header + '\033[39m')
                print(' \033[31mVERSION       (1 Bytes):  ' + str(version) + '\033[39m')
                print(' \033[31mMODE          (1 Bytes):  ' + str(mode) + '\033[39m')
                print(' \033[31mALPHA_COLOR   (1 Bytes):  ' + str(alpha_color) + '\033[39m'
                      + ' \u2794 \033[' + get_color('bg', alpha_color) + 'm  \033[39m')
                print(' \033[31mWIDTH         (1 Bytes):  ' + str(width) + '\033[39m')
                print(' \033[31mHEIGHT        (1 Bytes):  ' + str(height) + '\033[39m')

            if mode is 0:
                print(' ')
                for x in range(0, int(height / 2)):
                    print(' ', end=' ')
                    for y in range(0, width):
                        color_value = ord(f.read(1))
                        bg_color = int(color_value / 16)
                        fg_color = int(color_value % 16)
                        print('\033[' + get_color('bg', bg_color) + ';'
                              + get_color('fg', fg_color) + 'm' + get_value(220) + '\033[39m', end='')
                    print(' ')
                print(' ')
            elif mode is 1:
                print(' ')
                for x in range(0, int(height / 2)):
                    print(' ', end=' ')
                    for y in range(0, width):
                        value = ord(f.read(1))
                        color_value = ord(f.read(1))
                        bg_color = int(color_value / 16)
                        fg_color = int(color_value % 16)
                        print('\033[' + get_color('bg', bg_color) + ';'
                              + get_color('fg', fg_color) + 'm' + get_value(value) + '\033[39m', end='')
                    print(' ')
                print(' ')

            else:
                print('\033[41;97m Mode ' + str(mode) + ' is not supported! \033[39m')
                sys.exit(1)
        else:
            print('\033[41;97m This is no valid tmg file! \033[39m')
            sys.exit(1)


if __name__ == "__main__":
    def check_input(input):
        _, file_extension = os.path.splitext(input)
        if os.path.exists(input) and file_extension == ".tmg":
            return input
        else:
            print('\033[41;97m ' + input + ' is no valid input file! \033[39m')
            sys.exit(1)


    parser = argparse.ArgumentParser(description='\033[41;97m View *.tmg files for elfboot \033[39m')
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument('-i', '--input', dest='input', required=True,
                          help='path of input file (has to be a *.tmg file)', type=check_input)
    optional.add_argument('-d', '--debug', dest='debug', default=False, action="store_true",
                          help='print all available information about the image ')
    parser._action_groups.append(optional)
    args = parser.parse_args()

    preview(args.input, args.debug)


