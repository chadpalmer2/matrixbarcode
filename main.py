from curses.panel import top_panel
from turtle import left
from PIL import Image, ImageDraw, ImageEnhance, ImageStat, ImageFilter
import os
from math import sqrt, sin, cos, atan2, pi
from reedsolo import RSCodec, ReedSolomonError
import pdb

## hardcoded encoding sizes

encoding_size = 108
ecc_len = 27
data_size_limit = encoding_size - ecc_len

rsc = RSCodec(ecc_len)

## hardcoded spoke parameters

lines_per_spoke = 24
spacing = 1

## parameters to manipulate for image feature proportions

line_resolution = 20

center_spoke_length = 12 * line_resolution
main_spoke_length = (lines_per_spoke * (1 + spacing) + 1) * line_resolution
endpoint_spoke_length = 6 * line_resolution

total_spoke_length = center_spoke_length + main_spoke_length + endpoint_spoke_length

image_size = int(total_spoke_length * 2.5)

## data encoding and decoding functions

def encode_payload(data):
    return rsc.encode(data)

def decode_payload(payload):
    return rsc.decode(payload)

def encode_line_lengths(payload):
    lengths = []
    parse_list = []
    for encoded_byte in payload:
        parse_list.append(encoded_byte)
        if len(parse_list) == 3:
            lengths += [
                parse_list[0] // 32,
                (parse_list[0] % 32) // 4,
                ((parse_list[0] % 4) * 2) + parse_list[1] // 128,
                (parse_list[1] % 128) // 16,
                (parse_list[1] % 16) // 2,
                ((parse_list[1] % 2) * 4) + parse_list[2] // 64,
                (parse_list[2] % 64) // 8,
                parse_list[2] % 8
            ]
            parse_list = []

    return lengths

def decode_line_lengths(lengths):
    payload = []
    parse_list = []
    for line in lengths:
        parse_list.append(line)
        if len(parse_list) == 8:
            payload += [
                (parse_list[0] * 32) + (parse_list[1] * 4) + (parse_list[2] // 2),
                ((parse_list[2] % 2) * 128) + (parse_list[3] * 16) + (parse_list[4] * 2) + (parse_list[5] // 4),
                ((parse_list[5] % 4) * 64) + (parse_list[6] * 8) + parse_list[7]
            ]
            parse_list = []

    return bytearray(payload)

# image encoding functions

def get_translated_point(xy, d, angle):
    return (int(xy[0] + d * cos(angle)), int(xy[1] + d * sin(angle)))

def get_distance(xy1, xy2):
    x_side = xy2[0] - xy1[0]
    y_side = xy2[1] - xy1[1]

    return [
        sqrt(x_side**2 + y_side**2), 
        atan2(y_side, x_side)
    ]

def draw_hexagon(d, xy, spoke, color):
    d.polygon([
        get_translated_point(xy, spoke, pi / 6),
        get_translated_point(xy, spoke, pi / 2),
        get_translated_point(xy, spoke, 5 * pi / 6),
        get_translated_point(xy, spoke, 7 * pi / 6),
        get_translated_point(xy, spoke, 3 * pi / 2),
        get_translated_point(xy, spoke, 11 * pi / 6),
    ], fill=color)

def draw_full_hexagon(d, xy, spoke, color, fill_in=True):
    draw_hexagon(d, xy, spoke, (0, 0, 0))
    draw_hexagon(d, xy, spoke - line_resolution, (255, 255, 255))
    if fill_in:
        draw_hexagon(d, xy, spoke - 2 * line_resolution, (0, 0, 0))

## build and decode image functions

def build_image(lengths):
    img = Image.new('RGB', (image_size, image_size), "white")
    d = ImageDraw.Draw(img)

    spoke_point_translation_angles = [
        pi / 2,
        3 * pi / 2,
        5 * pi / 6,
        pi / 6,
        7 * pi / 6,
        11 * pi / 6
    ]

    middle = (image_size // 2, image_size // 2)
    spoke_points = [ get_translated_point(middle, total_spoke_length, angle) for angle in spoke_point_translation_angles ]
    top, bottom, left_top, right_top, left_bottom, right_bottom = spoke_points

    d.line([top, bottom], fill=(0,0,0), width=line_resolution)
    d.line([left_top, right_bottom], fill=(0,0,0), width=line_resolution)
    d.line([right_top, left_bottom], fill=(0,0,0), width=line_resolution)

    draw_full_hexagon(d, middle, center_spoke_length, (0, 0, 0))

    for point in [top, bottom, left_bottom]:
        draw_full_hexagon(d, point, endpoint_spoke_length, (0, 0, 0), fill_in=True)

    for point in [left_top, right_top, right_bottom]:
        draw_full_hexagon(d, point, endpoint_spoke_length, (0, 0, 0), fill_in=False)

    for index, length in enumerate(lengths):
        spoke = index // 48
        clockwise_spin = (index // 24) % 2
        spoke_index = index % 24

        distance_from_origin = (1 + spacing) * line_resolution * (1 + spoke_index) + center_spoke_length
        angle_from_origin = spoke_point_translation_angles[spoke]

        spoke_point = get_translated_point(middle, distance_from_origin, angle_from_origin)
        max_point = get_translated_point(middle, int(distance_from_origin * sqrt(3) / 2), angle_from_origin + (pi / 6)*(-1)**(clockwise_spin))

        max_distance = get_distance(spoke_point, max_point)
        end_point = get_translated_point(spoke_point, max_distance[0] * (length / 8), max_distance[1])

        d.line([spoke_point, end_point], fill=(0,0,0), width=line_resolution)

    img.show()

def decode_image(filename):
    try:
        img = Image.open(filename)
    except:
        print("no such file.")
        return

    # Rendering image in black and white

    # out = Image.new('I', img.size, 0xffffff)
    # thresh = sum(ImageStat.Stat(img).mean) / (3 * 2)
    # fn = lambda x : 255 if x > thresh else 0
    # out = img.convert('L').point(fn, mode='1')
    # out.show()

    # Conversion of processed image to lengths

    pdb.set_trace()

def main():
    print("encoding or decoding?")
    option = input()
    if len(option) != 0 and option[0] in ['e', 'E']:
        print("encoding selected. provide payload:")
        data = input().encode()

        if len(data) > data_size_limit:
            print(f"limit: { data_size_limit } character maximum")
            return

        data += (b'\0') * (data_size_limit - len(data)) # null character padding

        payload = encode_payload(data)
        
        lengths = encode_line_lengths(payload)

        build_image(lengths)
    else:
        print("decoding selected. provide filename:")
        decode_image(input())

main()
