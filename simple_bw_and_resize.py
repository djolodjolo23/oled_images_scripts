from PIL import Image
import os
import argparse

parser = argparse.ArgumentParser(description='Process images from the internet to be displayed on the OLED screen.')
parser.add_argument('image_name', type=str, help='Name of the image you want to process.')
parser.add_argument('target_image_size', type=str, help='Target image size, type it in a format like 45x61.')
parser.add_argument('--invert', action='store_true', help='Invert the image colors')

args = parser.parse_args()
input_images_folder = 'input_images'
output_images_folder = 'output_images'
header_files_folder = 'header_files'

full_image_name = os.path.join(input_images_folder, args.image_name)
image_name = os.path.basename(full_image_name).split('.')[0]
target_image_size = args.target_image_size
target_image_width, target_image_height = map(int, target_image_size.split('x'))

image = Image.open(full_image_name)

if image.mode == 'RGBA':
    background = Image.new('RGBA', image.size, (255, 255, 255, 255))
    # Paste the image on the background using alpha channel as mask
    background.paste(image, (0, 0), image)
    image = background.convert('RGB')

image = image.convert('L')

if args.invert:
    image = Image.eval(image, lambda x: 255 - x)

resized_image = image.resize((target_image_width, target_image_height))

bw_image = resized_image.convert('1')

os.makedirs(output_images_folder, exist_ok=True)
os.makedirs(header_files_folder, exist_ok=True)

xbm_image_name = os.path.join(output_images_folder, f"{image_name}_{target_image_size}.xbm")
bw_image.save(xbm_image_name)

with open(xbm_image_name, 'r') as xbm_file:
    xbm_content = xbm_file.readlines()

array_start = next(i for i, line in enumerate(xbm_content) if line.startswith('static char'))

header_array = xbm_content[array_start:]
header_oled_image_name = f"{image_name}_oled_image_{target_image_size}.h"
header_guard_name = os.path.basename(header_oled_image_name).replace('.', '_').upper()

with open(os.path.join(header_files_folder, header_oled_image_name), 'w') as header_file:
    header_file.write('#include <cstdint>\n')
    header_file.write(f'#ifndef {header_guard_name}\n')
    header_file.write(f'#define {header_guard_name}\n\n\n')
    header_file.write(f'const unsigned char {image_name}_oled_image_{target_image_width}x{target_image_height} [] = {{\n')
    for line in header_array[1:]:
        header_file.write(line)
    header_file.write('#endif\n')

print('Done!')