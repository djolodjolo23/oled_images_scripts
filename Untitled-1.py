from PIL import Image, ImageFilter

image = Image.open('spaghetti.jpg')

gray_image = image.convert('L')

resized_image = gray_image.resize((96, 81))

blurred_image = resized_image.filter(ImageFilter.GaussianBlur(2))
edge_image = blurred_image.filter(ImageFilter.FIND_EDGES)

# Apply a binary threshold to emphasize the edges
threshold = 1
bw_edge_image = edge_image.point(lambda x: 255 if x > threshold else 0, mode='1')

width, height = bw_edge_image.size
pixels = bw_edge_image.load()

for i in range(width):
    pixels[i, 0] = 255  # Top border
    pixels[i, height - 1] = 255  # Bottom border

for j in range(height):
    pixels[0, j] = 255  # Left border
    pixels[width - 1, j] = 255  # Right border

bw_edge_image.save('spaghetti_bw.jpeg')
bw_edge_image.save('spaghetti_bw.xbm')

with open('spaghetti_bw.xbm', 'r') as xbm_file:
    xbm_content = xbm_file.readlines()

array_start = None
for i, line in enumerate(xbm_content):
    if line.startswith('static char'):
        array_start = i
        break

header_array = xbm_content[array_start:]

# Save the array into a C header file
with open('spaghetti_oled_image.h', 'w') as header_file:
    header_file.write('#include <cstdint>\n')
    header_file.write('#ifndef SPAGHETTI_OLED_IMAGE_H\n')
    header_file.write('#define SPAGHETTI_OLED_IMAGE_H\n\n\n')
    header_file.write('const unsigned char oled_image [] = {\n')

    # Write the XBM array (excluding static char declaration)
    for line in header_array[1:]:
        header_file.write(line)
    header_file.write('#endif\n')

print('Done!')
