
"""
create an initially equal probability map,
then use this to generate the probability to hit
a certain point. if the point is full, move to
the next radius.
"""

from PIL import Image
import numpy as np
from random import choice

w, h = 100, 100
field = Image.new("RGBA", (w, h), color="black")
field = np.array(field)
pixels = [(y, x) for x in range(h) for y in range(w)]

def within(y, x):
    global w, h
    return (y, x) if (y < h and y >= 0) and (x < w and x >= 0) else False

def find_first(yx):
    y, x = yx
    check, iters, done = [(y, x)], 0, []
    while len(check) != 0:
        if iters >= 1000:
            break
        y, x = check[0]
        check.append(within(y+1, x)) # down
        check.append(within(y-1, x)) # up
        check.append(within(y, x-1)) # left
        check.append(within(y, x+1)) # right
        check = [c for c in check if c != False and c not in done]
        done.append((y, x))
        if field[y][x][2] != 250:
            return (y, x)
        del check[0]
        iters += 1
    return (False, False)

for i in range(20000000):
    y, x = find_first(choice(pixels))
    # print(y, x)
    if y == False and x == False:
        continue
    # r, g, b, a = field[y][x]
    # print(r, g, b, a)
    field[y][x][2] += 1
    pixels.append((y, x))
    if i % 10000 == 0:
        Image.fromarray(field).save("progress.png")

Image.fromarray(field).show()
