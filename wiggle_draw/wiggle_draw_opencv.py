# from PIL import Image, ImageEnhance, ImageFile
import math
import cv2 as cv
import numpy as np
from numpy.typing import ArrayLike

def wiggle_image(
        original_img: ArrayLike,
        r_increase=15, # increase in r per circle
        rotations=18,

        wiggle_amplitude=10,
        wiggle_freq=0.8,
    ) -> ArrayLike:
    
    output_image = np.zeros(original_img.shape, dtype=np.uint8)
    width, height, _ = output_image.shape

    oy, ox = width//2, height//2
    a = 0
    spiral_radius = 1

    d = 0
    delta_d = r_increase/150

    while a < (2 * math.pi) * rotations:
        wiggle = wiggle_amplitude * math.sin(d * wiggle_freq)
        px = ox + spiral_radius * (math.cos(a) )
        py = oy + spiral_radius * (math.sin(a))
        try:
            # r, g, b = original_img[int(py), int(px)]
            # intensity = (int(r) + int(g) + int(b)) / (255 * 3)
            intensity = np.mean(original_img[int(py), int(px)]) / 255
            # intensity = 1 
            px = int(ox + (spiral_radius + wiggle * intensity) * (math.cos(a)))
            py = int(oy + (spiral_radius + wiggle * intensity) * (math.sin(a)))

            output_image[py,px] = [255,255,255]
            # print(original_img[py, px])
            # output_image[0,0] = np.array([255,255,255])
        except(IndexError):
            print("Out of range")
            return output_image
            pass


        delta_a = math.atan2(delta_d, spiral_radius) 

        spiral_radius += r_increase / (2 * math.pi) * delta_a
        a += delta_a
        d += delta_d
    return output_image


original_img = cv.imread("/home/otl/code/random_python/wiggle_draw/OTL2.jpeg")
# cv.imshow("Original", original_img)

# for r in range(30):
new_image = wiggle_image(original_img, rotations=30, wiggle_freq=1)
print(original_img.shape)

cv.imshow("hello", new_image) #; cv.waitKey(0)

print("OpenCV:", cv.__version__)

cv.imshow("hello", new_image); cv.waitKey(0)
cv.imwrite("hello.png", new_image)