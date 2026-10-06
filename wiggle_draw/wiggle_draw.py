from PIL import Image, ImageEnhance, ImageFile
import math


def wiggle_image(
        original_img: Image,
        r_increase=15, # increase in r per circle
        rotations=18,

        wiggle_amplitude=5,
        wiggle_freq=0.8,
    ) -> Image:
    
    ###############
    enhancer = ImageEnhance.Contrast(original_img)
    modified_img = enhancer.enhance(2)
    mod_pixels = modified_img.load()
    # modified_img.show()


    output_image = Image.new('RGB', original_img.size, color=(0,0,0))
    out_pixels = output_image.load()
    width, height = output_image.size

    ox, oy = width//2, height//2
    a = 0
    spiral_radius = 1

    d = 0
    delta_d = r_increase/150

    while a < (2 * math.pi) * rotations:
        wiggle = wiggle_amplitude * math.sin(d * wiggle_freq)
        px = ox + spiral_radius * (math.cos(a) )
        py = oy + spiral_radius * (math.sin(a))
        try:
            r, g, b = mod_pixels[px, py]
            intensity = (r + g + b) / (255 * 3)

            # intensity = 1 
            px = ox + (spiral_radius + wiggle * intensity) * (math.cos(a))
            py = oy + (spiral_radius + wiggle * intensity) * (math.sin(a))

            out_pixels[px,py] = (255,255,255)
        except(IndexError):
            print("Out of range")
            return output_image
            pass


        delta_a = math.atan2(delta_d, spiral_radius) 

        spiral_radius += r_increase / (2 * math.pi) * delta_a
        a += delta_a
        d += delta_d

    return output_image


original_img = Image.open("OTL.jpg")
# original_img.show()
w, h = original_img.size
original_img = original_img.resize((w//2, h//2))
# modified_img = original_img.copy()

# mod_pixels = original_img.load()
# modified_img.show()

new_image = wiggle_image(original_img, rotations=20, wiggle_freq=1)

new_image.show()
# new_image.save('temp.png')
