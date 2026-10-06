from PIL import Image, ImageEnhance
import math

original_img = Image.open("Duck.bmp")

modified_img = original_img.copy()

mod_pixels = original_img.load()
# modified_img.show()


new_image = Image.new('RGB', original_img.size)
pixels = new_image.load()
width, height = new_image.size

ox, oy = width//2, height//2
a = 0
radius = 1
r_increase = 15 # increase in r per circle
rotations =  18

wiggle_amplitude = 5
wiggle_freq = 0.8
d = 0
delta_d = r_increase/100
brightnesses = []
while a < (2 * math.pi) * rotations:
    wiggle = wiggle_amplitude * math.sin(d * wiggle_freq)
    px = ox + radius * (math.cos(a) )
    py = oy + radius * (math.sin(a))

    r, g, b = mod_pixels[px, py]
    intensity = (r + g + b) / (255 * 3)
    brightnesses.append(intensity)

    # intensity = 1 
    px = ox + (radius+wiggle*intensity) * (math.cos(a) )
    py = oy + (radius+wiggle*intensity) * (math.sin(a))

    # pixels[px,py] = mod_pixels[px, py] #(255,255,255) #(r, g, b)
    pixels[px,py] = (255,255,255)


    delta_a = math.atan2(delta_d, radius) 
    # delta_a = math.atan2(d, r) 

    radius += r_increase / (2 * math.pi) * delta_a
    a += delta_a
    d += delta_d
new_image.show()
# print(brightnesses)
print(max(brightnesses))
print(min(brightnesses))

