from PIL import Image

import argparse
import os
import sys
import tmg_viewer

tmg_header = 'TMG'
tmg_version = 1

color_table_64_16 = [
    ("000", 0), ("001", 1), ("002", 1), ("003", 1),
    ("010", 2), ("011", 8), ("012", 9), ("013", 9),
    ("020", 2), ("021", 2), ("022", 3), ("023", 3),
    ("030", 10), ("031", 10), ("032", 10), ("033", 11),
    ("100", 4), ("101", 5), ("102", 1), ("103", 1),
    ("110", 6), ("111", 8), ("112", 9), ("113", 9),
    ("120", 2), ("121", 2), ("122", 3), ("123", 3),
    ("130", 10), ("131", 10), ("132", 10), ("133", 11),
    ("200", 4), ("201", 12), ("202", 5), ("203", 13),
    ("210", 6), ("211", 12), ("212", 5), ("213", 9),
    ("220", 14), ("221", 7), ("222", 7), ("223", 7),
    ("230", 10), ("231", 10), ("232", 10), ("233", 11),
    ("300", 4), ("301", 12), ("302", 5), ("303", 13),
    ("310", 4), ("311", 12), ("312", 5), ("313", 13),
    ("320", 6), ("321", 6), ("322", 7), ("323", 13),
    ("330", 14), ("331", 14), ("332", 14), ("333", 15)
]
color_table = [
    ('white', '40', '30', 15),
    ('yellow', '103', '93', 14),
    ('light purple', '105', '95', 13),
    ('light red', '101', '91', 12),
    ('light cyan', '106', '96', 11),
    ('light green', '102', '92', 10),
    ('light blue', '104', '94', 9),
    ('dark grey', '100', '90', 8),
    ('grey', '47', '37', 7),
    ('brown', '43', '33', 6),
    ('purple', '45', '35', 5),
    ('red', '41', '31', 4),
    ('cyan', '46', '36', 3),
    ('green', '42', '32', 2),
    ('blue', '44', '34', 1),
    ('black', '107', '97', 0)
]
color_range = [
    [(-1, 20), (21, 127), (128, 235), (236, 256)],
    [(-1, 31), (32, 127), (128, 224), (225, 256)],
    [(-1, 42), (43, 127), (128, 212), (213, 256)],
    [(-1, 52), (53, 127), (128, 202), (203, 256)],
    [(-1, 63), (64, 127), (128, 191), (192, 256)],
    [(-1, 73), (74, 127), (128, 181), (182, 256)],
    [(-1, 83), (84, 127), (128, 171), (172, 256)]
]
alpha_range = [64, 92, 128, 150, 172]
pixel_list = []


# pos = True <- bg
# pos = False <- fg
def get_terminal_color(rgba, color_range_list):
    def get_color_range(r_value):
        if r_value is 0:
            return range(color_range_list[0][0], color_range_list[0][1])
        if r_value is 1:
            return range(color_range_list[1][0], color_range_list[1][1])
        if r_value is 2:
            return range(color_range_list[2][0], color_range_list[2][1])
        if r_value is 3:
            return range(color_range_list[3][0], color_range_list[3][1])
        else:
            return range(color_range_list[0][0], color_range_list[0][1])

    r, g, b, a = rgba
    rgb_list = [r, g, b]
    rgb = ""

    for value in rgb_list:
        if value in get_color_range(0):
            rgb = rgb + "0"
        elif value in get_color_range(1):
            rgb = rgb + "1"
        elif value in get_color_range(2):
            rgb = rgb + "2"
        else:
            rgb = rgb + "3"

    for color in color_table_64_16:
        if rgb == color[0]:
            for final_color in color_table:
                if final_color[3] is color[1]:
                    if a < alpha_range[args.alpha]:
                        return 'alpha', final_color[1], final_color[2], final_color[3]
                    else:
                        return final_color


def load_image(image_file):
    print('\033[42;97m Load image ' + image_file + ' and get all colors right \033[39m')
    im = Image.open(image_file)
    pix = im.load()
    print(' \033[100;92m Width:  ' + str(im.size[0]) + 'px \033[39m')
    print(' \033[100;92m Height: ' + str(im.size[1]) + 'px \033[39m')
    if im.size[0] > 255 or im.size[1] > 255:
        print('\033[41;97m Your input picture is to big for tmg, max. resolution is 255x255px! \033[39m')
        sys.exit(1)
    print(' \033[100;92m ' + str(im.size[0] * im.size[1]) + ' parsed pixels \033[39m')

    if im.size[1] % 2 is 1:
        y_size = im.size[1] - 1
    else:
        y_size = im.size[1]

    for y_pix in range(0, y_size, 2):
        row = []
        for x_pix in range(0, im.size[0]):
            row.append((get_terminal_color(pix[x_pix, y_pix],       color_range[args.range]),
                        get_terminal_color(pix[x_pix, (y_pix + 1)], color_range[args.range])))
        pixel_list.append(row)


def mod_image(image_file):
    image = Image.open(image_file)
    image = image.convert("RGBA")
    image.save(image_file)


def show_colors():
    color_table_string = '\n'
    for color in color_table:
        color_table_string += '\033[' + str(color[1]) + 'm  \033[39m ' + color[0] + ' = ' + str(color[3] + 1) + '\n'
    return color_table_string


def main(args):
    mod_image(args.input)
    load_image(args.input)

    header = bytearray(b'')
    body = bytearray(b'')

    transparency = False
    transparency_color = 0

    print('\n\033[42;97m Create and save TMG file \033[39m')

    # header
    for letter in tmg_header:
        header.append(ord(letter))  # TMG
    header.append(tmg_version)  # version
    if 0 < args.color <= 16:
        transparency = True
        transparency_color = args.color - 1
        header.append(1)
        header.append(transparency_color)
    else:
        header.append(0)
        header.append(0)
    header.append(len(pixel_list[0]))
    header.append(int(len(pixel_list) * 2))

    # body
    for x in range(0, len(pixel_list)):
        for y in range(0, len(pixel_list[0])):
            color_background = pixel_list[x][y][0]
            color_foreground = pixel_list[x][y][1]
            if transparency:
                if color_background[0] == 'alpha' and color_foreground[0] == 'alpha':
                    color_val = transparency_color * 16
                    body.append(32)  # space
                elif color_background[0] == 'alpha' and color_foreground[0] != 'alpha':
                    color_val = transparency_color * 16 + color_foreground[3]
                    body.append(220)  # down half block
                elif color_background[0] != 'alpha' and color_foreground[0] == 'alpha':
                    color_val = transparency_color * 16 + color_foreground[3]
                    body.append(223)  # up half block
                elif color_background[3] is color_foreground[3]:
                    color_val = transparency_color * 16 + color_foreground[3]
                    body.append(219)  # full block
                else:
                    color_val = color_background[3] * 16 + color_foreground[3]
                    body.append(220)  # full block
            else:
                color_val = color_background[3] * 16 + color_foreground[3]
            body.append(int(color_val))

    if os.path.isdir(args.output):
        filename, _ = os.path.splitext(args.input)
        output_file_path = os.path.join(args.output, os.path.basename(filename) + '.tmg')
    else:
        output_file_path = args.output
    output_file = open(output_file_path, 'wb')
    output_file.write(header)
    output_file.write(body)
    output_file.close()

    print(' \033[100;92m Size of ' + output_file_path + ' is ' + str(os.path.getsize(output_file_path)) +
          " byte " + '\033[39m')

    if args.preview:
        print('\n\033[42;97m Preview \033[39m')
        tmg_viewer.preview(output_file_path, False)


if __name__ == "__main__":
    def check_input(input):
        _, file_extension = os.path.splitext(input)
        if os.path.exists(input) and file_extension == ".png":
            return input
        else:
            print('\033[41;97m ' + input + ' is no valid input file! \033[39m')
            sys.exit()

    def check_output(output):
        _, file_extension = os.path.splitext(output)
        if os.path.exists(output) and file_extension == ".tmg":
            return output
        elif os.path.isdir(output):
            return output
        elif os.path.exists(os.path.dirname(output)):
            return output
        else:
            print('\033[41;97m ' + output + ' is no valid output file or path! \033[39m')
            sys.exit()

    parser = argparse.ArgumentParser(description='\033[41;97m Create *.tmg files for elfboot \033[39m',
                                     formatter_class=argparse.RawTextHelpFormatter)
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument('-i', '--input', dest='input', required=True,
                          help='path of input file (has to be a *.png file)', type=check_input)
    required.add_argument('-o', '--output', dest='output', required=True,
                          help='path of output file', type=check_output)
    optional.add_argument('-t', '--transparency', dest='color', default=0,
                          help='add transparency to file with selected background color:' + show_colors(), type=int)
    optional.add_argument('-p', '--preview', dest='preview', default=False, action="store_true",
                          help='show preview of the generated image file')
    optional.add_argument('-r', '--range', dest='range', default=4,
                          help='change sensitivity of rgb values detection, try it (values from 0-6)', type=int)
    optional.add_argument('-a', '--alpha', dest='alpha', default=2,
                          help='change sensitivity of alpha values detection, try it (values from 0-4)', type=int)
    parser._action_groups.append(optional)
    args = parser.parse_args()

    main(args)
