# from curses.panel import top_panel
# from turtle import left
from PIL import Image, ImageDraw, ImageEnhance, ImageStat, ImageFilter, ImageChops
import os
import numpy
from math import sqrt, sin, cos, atan2, pi
from reedsolo import RSCodec, ReedSolomonError
import pdb

## hardcoded encoding sizes

encoding_size = 108
ecc_len = 27
data_size_limit = encoding_size - ecc_len

rsc = RSCodec(ecc_len)

## hardcoded coding features

spoke_count = 6
lines_per_spoke = 24
line_gradations = 8

### storage capacity in bytes = 2 * spoke_count * lines_per_spoke * log_2(line_gradations) / 8

## parameters to manipulate for image feature proportions

line_resolution = 20
spacing = 1

center_spoke_length = 12 * line_resolution
main_spoke_length = (lines_per_spoke * (1 + spacing) + 1) * line_resolution
endpoint_spoke_length = 6 * line_resolution

total_spoke_length = center_spoke_length + main_spoke_length + endpoint_spoke_length

image_size = int(total_spoke_length * 2.5)

## numpy helper function for perspective transform
## https://stackoverflow.com/questions/14177744/how-does-perspective-transformation-work-in-pil

def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)

def perspective_transform(img, start_coords, end_coords):
    coeffs = find_coeffs(end_coords, start_coords)

    return img.transform((image_size, image_size), Image.Transform.PERSPECTIVE, coeffs, Image.Resampling.BICUBIC)

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

def draw_full_hexagon(d, xy, spoke, fill_in=True):
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

    draw_full_hexagon(d, middle, center_spoke_length)

    for point in [top, bottom, left_bottom]:
        draw_full_hexagon(d, point, endpoint_spoke_length, fill_in=True)

    for point in [left_top, right_top, right_bottom]:
        draw_full_hexagon(d, point, endpoint_spoke_length, fill_in=False)

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

def decode_processed_image(img):
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

    lengths = []
    for index in range(2 * spoke_count * lines_per_spoke):
        spoke = index // 48
        clockwise_spin = (index // 24) % 2
        spoke_index = index % 24

        distance_from_origin = (1 + spacing) * line_resolution * (1 + spoke_index) + center_spoke_length
        angle_from_origin = spoke_point_translation_angles[spoke]

        spoke_point = get_translated_point(middle, distance_from_origin, angle_from_origin)
        max_point = get_translated_point(middle, int(distance_from_origin * sqrt(3) / 2), angle_from_origin + (pi / 6)*(-1)**(clockwise_spin))

        max_distance = get_distance(spoke_point, max_point)

        for length in range(1, 8):
            end_point = get_translated_point(spoke_point, max_distance[0] * (length / 8), max_distance[1])
            
            x, y = end_point
            avg = 0
            for i in range(-4, 5):
                for j in range(-4, 5):
                    avg += img.getpixel((x + i, y + j))
            avg /= 81

            if avg >= 20 and avg <= 225:
                lengths.append(length)
                break
        else:
            lengths.append(0)

    # RS decoding

    payload = decode_line_lengths(lengths)
    data = decode_payload(payload)[0].decode()

    print(data)

def decode_image(filename):
    try:
        img = Image.open(filename)
    except:
        print("no such file.")
        return

    # Rendering image in black and white

    out = Image.new('I', img.size, 0xffffff)
    thresh = (0.5) * (sum(ImageStat.Stat(img).mean) / 3)
    fn = lambda x : 255 if x > thresh else 0
    out = img.convert('L').point(fn, mode='1')

    # get crop bounds

    pixels = out.load()
    
    left = 0
    white_pixel_count = 0
    for x in range(out.size[0]):
        for y in range(out.size[1]):
            if pixels[x, y] == 255:
                white_pixel_count += 1
        if (white_pixel_count / out.size[1]) >= 0.95:
            left = x
            break
        else:
            white_pixel_count = 0
    
    right = out.size[0] - 1
    white_pixel_count = 0
    for x in range(out.size[0] - 1, -1, -1):
        for y in range(out.size[1]):
            if pixels[x, y] == 255:
                white_pixel_count += 1
        if (white_pixel_count / out.size[1]) >= 0.95:
            right = x
            break
        else:
            white_pixel_count = 0
    
    up = 0
    white_pixel_count = 0
    for y in range(out.size[1]):
        for x in range(out.size[0]):
            if pixels[x, y] == 255:
                white_pixel_count += 1
        if (white_pixel_count / out.size[0]) >= 0.95:
            up = y
            break
        else:
            white_pixel_count = 0
    
    down = out.size[1] - 1
    white_pixel_count = 0
    for y in range(out.size[1] - 1, -1, -1):
        for x in range(out.size[0]):
            if pixels[x, y] == 255:
                white_pixel_count += 1
        if (white_pixel_count / out.size[0]) >= 0.95:
            down = y
            break
        else:
            white_pixel_count = 0

    out = out.crop((left, up, right, down))

    # find real spoke_points

    real_outer_spoke_points = []
    find = False

    for x in range(out.size[0]):
        for y in range(out.size[1] - 1, -1, -1):
            if pixels[x, y] == 0:
                real_outer_spoke_points.append((x, y))
                find = True
                break
        if find:
            find = False
            break

    for x in range(out.size[0] - 1, -1, -1):
        for y in range(out.size[1]):
            if pixels[x, y] == 0:
                real_outer_spoke_points.append((x, y))
                find = True
                break
        if find:
            find = False
            break

    for y in range(out.size[1]):
        for x in range(out.size[0]):
            if pixels[x, y] == 0:
                real_outer_spoke_points.append((x, y))
                find = True
                break
        if find:
            find = False
            break

    for y in range(out.size[1] - 1, -1, -1):
        for x in range(out.size[0]):
            if pixels[x, y] == 0:
                real_outer_spoke_points.append((x, y))
                find = True
                break
        if find:
            find = False
            break

    # perspective transform real spoke_points to ideal spoke_points

    outer_spoke_point_translation_angles = [
        7 * pi / 6,
        pi / 6,
        pi / 2,
        3 * pi / 2
    ]

    middle = (image_size // 2, image_size // 2)
    ideal_outer_spoke_points = [ get_translated_point(middle, total_spoke_length + endpoint_spoke_length, angle) for angle in outer_spoke_point_translation_angles ]
    out = perspective_transform(out, real_outer_spoke_points, ideal_outer_spoke_points)

    # rotate image to proper orientation

    spoke_point_translation_angles = [
        pi / 6,
        pi / 2,
        5 * pi / 6,
        3 * pi / 2,
        7 * pi / 6,
        11 * pi / 6
    ]

    spoke_points = [ get_translated_point(middle, total_spoke_length, angle) for angle in spoke_point_translation_angles ]
    right_top, top, left_top, left_bottom, bottom, right_bottom = spoke_points

    if out.getpixel(right_top) == 255 and out.getpixel(left_bottom) == 255:
        # rotate 60 degrees widdershins
        out = out.rotate(angle=60, fillcolor=255)
        pass
    elif out.getpixel(left_top) == 255 and out.getpixel(right_bottom) == 255:
        # rotate 60 degrees clockwise
        out = out.rotate(angle=300, fillcolor=255)
        pass

    if out.getpixel(left_bottom) == 255:
        # flip horizontally
        out = out.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)
    elif out.getpixel(right_top) == 255:
        # flip vertically
        out = out.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)
    elif out.getpixel(right_bottom) == 255:
        # flip both ways AKA rotate 180 degrees
        out = out.transpose(method=Image.Transpose.ROTATE_180)
        pass

    out.resize((image_size, image_size))

    # decode processed image

    decode_processed_image(out)

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