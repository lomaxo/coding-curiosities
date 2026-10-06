# from hashlib import new
from PIL import Image

def create_swirls(source_image):
    
    new_image = Image.new('RGB', source_image.size)
    pixels = new_image.load()
    width, height = source_image.size

    for y in range(height):
        for x in range(width):
            pixels[x, y] = (int(x/width * 255), int(y / height * 255), 255)
            # print(f'x:{x}, y:{y}, RGB:{pixels[x, y]}')

    return new_image.convert('RGB')


def within_tolerance(test_colour, target_colour, tolerance_range):
    for channel in range(3):
        if test_colour[channel] < target_colour[channel] - tolerance_range[channel]:
            return False
        elif test_colour[channel] > target_colour[channel] + tolerance_range[channel]:
            return False
    return True

def im_replace(background_image, foreground_image, target_colour, tolerance):
    foreground_image = foreground_image.resize(background_image.size)
    assert(background_image.size == foreground_image.size)
    background_pixels = background_image.load()
    foreground_pixels = foreground_image.load()
    
    width, height = background_image.size
    combined_image = Image.new('RGB', background_image.size)
    combined_pixels = combined_image.load()
    for x in range(width):
        for y in range(height):
            if within_tolerance(foreground_pixels[x, y][0:3], target_colour, tolerance):
                combined_pixels[x, y] = background_pixels[x, y]
            else:
                combined_pixels[x, y] = foreground_pixels[x, y]

    return combined_image


# landscape_image = Image.open("landscape.png")
# foreground = create_swirls(landscape_image)
shia = Image.open("shia_labeouf_wants_you_to_get_motivated.jpg")
background = Image.open("Abingdon_school.jpg")
new_image = im_replace(background, shia, (124, 232, 147), (50, 50, 50))
new_image.convert('RGB').save('temp.png', 'PNG')
new_image.show()
