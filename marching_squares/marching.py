import cv2 as cv
import numpy as np
from numpy.typing import ArrayLike



def get_tl(x, y, grid_size):
    return x, y

def get_tr(x, y, grid_size):
    return x + grid_size, y

def get_bl(x, y, grid_size):
    return x, y + grid_size

def get_br(x, y, grid_size):
    return x + grid_size, y + grid_size

def lerp(value, h1, h2, p1, p2):
    factorN = value - int(h1)
    factorD = int(h2) - int(h1)
    factor = factorN / factorD
    ret_val = p1 + factor * (p2 - p1)
    return ret_val
    # return (p2 + p1) // 2

def get_l(x, y, target, img, grid_size):
    h1 = img[y, x]
    h2 = img[y + grid_size, x]
    return x, int(lerp(target, h1, h2, y, y+grid_size))

def get_t(x, y, target, img, grid_size):
    h1 = img[y, x]
    h2 = img[y ,x + grid_size]
    return int(lerp(target, h1, h2, x, x+grid_size)), y

def get_r(x, y, target, img, grid_size):
    h1 = img[y, x+grid_size]
    h2 = img[y + grid_size, x+grid_size]
    return x+grid_size, int(lerp(target, h1, h2, y, y+grid_size))

def get_b(x, y, target, img, grid_size):
    h1 = img[y+grid_size, x]
    h2 = img[y+grid_size,x + grid_size]
    return int(lerp(target, h1, h2, x, x+grid_size)), y +grid_size

def add_contours(iso_value, input_img, output_img, colour=(255,0,0), grid_size=4) -> ArrayLike:
    gs = grid_size
    for y in range(0, height-grid_size, grid_size):
        for x in range(0, width-grid_size, grid_size):
            test_value = 0
            test_value += 1 if input_img[get_tl(x,y, gs)[::-1]] > iso_value else 0
            test_value += 2 if input_img[get_tr(x,y, gs)[::-1]] > iso_value else 0
            test_value += 4 if input_img[get_br(x,y, gs)[::-1]] > iso_value else 0
            test_value += 8 if input_img[get_bl(x,y, gs)[::-1]] > iso_value else 0
            # print(normalized_img[y,x], normalized_img[y, x+GRID_SIZE], normalized_img[y+GRID_SIZE,x+GRID_SIZE], normalized_img[y+GRID_SIZE,x], iso_value, test_value)
            # cv.rectangle(contour_img, get_tl(x,y), get_br(x,y), (0,255,255), 1)

            # normalized_img[y,x] = 1
            if test_value in (1, 14):
                # line from left to top
                cv.line(output_img, get_l(x, y, iso_value, input_img, gs), get_t(x, y, iso_value, input_img, gs), colour,1)
            elif test_value in (2, 13):
                # line from right to top
                cv.line(output_img, get_r(x ,y, iso_value, input_img, gs), get_t(x, y, iso_value, input_img, gs), colour,1)
            elif test_value in (3, 12):
                # line from left to right
                cv.line(output_img, get_l(x ,y, iso_value, input_img, gs), get_r(x, y, iso_value, input_img, gs), colour,1)
            elif test_value in (4, 11):
                # line from bottom to right
                cv.line(output_img, get_b(x ,y, iso_value, input_img, gs), get_r(x, y, iso_value, input_img, gs), colour,1)
            elif test_value == 5:
                # saddle
                # line from left to top and bottom to right
                cv.line(output_img, get_l(x, y, iso_value, input_img, gs), get_t(x, y, iso_value, input_img, gs), colour,1)
                cv.line(output_img, get_b(x ,y, iso_value, input_img, gs), get_r(x, y, iso_value, input_img, gs), colour,1)
            elif test_value == 10:
                # saddle
                # line from left to bottom and top to right
                cv.line(output_img, get_l(x, y, iso_value, input_img, gs), get_b(x, y, iso_value, input_img, gs), colour,1)
                cv.line(output_img, get_t(x ,y, iso_value, input_img, gs), get_r(x, y, iso_value, input_img, gs), colour,1)
            elif test_value in (6, 9):
                # line from bottom to top
                cv.line(output_img, get_b(x ,y, iso_value, input_img, gs), get_t(x, y, iso_value, input_img, gs), colour,1)
            elif test_value in (7, 8):
                # line from left to bottom
                cv.line(output_img, get_b(x ,y, iso_value, input_img, gs), get_l(x, y, iso_value, input_img, gs), colour,1)
            # print(x, y, test_value)
    return output_img


if __name__ == "__main__":
    from noise import pnoise2

    width, height = 500, 500
    scale = 200
    octaves = 2
    persistence = 1.5
    lacunarity = 2.0

    img = np.zeros((width, height), dtype=np.float32)

    for y in range(height):
        for x in range(width):
            val = pnoise2( 
                    x / scale,
                    y / scale,
                    octaves=octaves,
                    persistence=persistence,
                    lacunarity=lacunarity,
                    repeatx=width,
                    repeaty=height,
                    base=0
                )
            img[y, x] = val

    normalized_img = cv.normalize(
        img, None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U
    )

    contour_img = normalized_img.copy() #  np.zeros(normalized_img.shape, dtype=np.uint8)    
    contour_img = cv.cvtColor(contour_img, cv.COLOR_GRAY2RGB)

    for h in range(0, 255, 20):
        contour_img = add_contours(h, normalized_img, contour_img, (h//2,h,0), 5)
    cv.imshow("Noise", contour_img)
    cv.waitKey(0)