
"""
Given a map of land, how would
random rain drops affect erosion and
land masses to create waterflow bias.
"""

from PIL import Image
from random import randint
import numpy as np

width, height = 500, 500 # globalized
field = Image.new("RGBA", (width, height), color="#d19775") # field
field = np.array(field)
oclr = tuple(field[0][0])

rain_drops = []
radius_check = 10 # radius of drop to check for roughness


"""
take image, and get the elements
outside within a radius from the point.
"""
def within(y, x):
    global width, height
    return (y, x) if (y < height and y >= 0) and (x < width and x >= 0) else False

"""
taken radius, using n^2 + n-1^2 we can
calc the iterations required to build a
mapped series around a point with a diamond
shape. this uses that, and identifies which
depth the iter is at in the diamond wrap.
starts at 2, since original point is ignored.
allows us to compute distance from the point,
without using any annoying testing - direct
mathematic proof.
"""
def rr_depth(radius, iteration, offset=False):
    if iteration == 1:
        return 1
    iteration = iteration + offset if offset != False else iteration # + offset if there's offset required
    for i in range(radius+1): # safety
        allowed = (i**2 + (i-1)**2)
        if iteration <= allowed:
            return i

"""

"""
def outside_of(y, x, radius):
    check = [(y, x)]
    done = []
    # r = 1, a = 1,
    # r = 2, a = 5,
    # r = 3, a = 13
    iters = 0
    iters_allowed = (radius**2 + (radius-1)**2) # calcs the iters required
    # print(iters_allowed)
    while len(check) != 0:
        if iters == iters_allowed:
            break
        y, x = check[0]
        check.append(within(y+1, x)) # down
        check.append(within(y-1, x)) # up
        check.append(within(y, x-1)) # left
        check.append(within(y, x+1)) # right
        check = [c for c in check if c != False and c not in done]
        done.append((y, x)) # add to "done"
        del check[0] # remove from stack
        iters += 1
    return done

"""
from yx1, determine the direction
towards yx2.
"""
def compass_direction(yx1, yx2):
    y1, x1 = yx1 # from
    y2, x2 = yx2 # to
    y_delta = y2 - y1
    x_delta = x2 - x1
    if y_delta > 0 and x_delta >= 0:
        return "up"
    elif y_delta < 0 and x_delta >= 0:
        return "down"
    elif x_delta > 0 and y_delta >= 0:
        return "right"
    elif x_delta < 0 and y_delta >= 0:
        return "left"
    else:
        return "stagnant"

radius = 3
hard_coded_perc = [0, 0.5, 0.25, 0.1] # 33% at index 1
from random import random

def erode(x):
    global field
    for _ in range(x):
        y, x = randint(0, 499), randint(0, 499)
        point = tuple(field[y][x]) # tuplized point
        if point == oclr: # original land
            field[y][x] = [50, 80, 255, 255]
        else:
            field[y][x][0] += 25 if field[y][x][0] <= 200 else 0
        for i, yx in enumerate(outside_of(y, x, radius)):
            y2, x2 = yx
            distance = rr_depth(radius=10, iteration=i+1)
            perc = hard_coded_perc[distance]
            perc = True if random() <= perc else False
            if perc == True:
                cd = compass_direction(
                    (y2, x2), # radius point
                    (y, x) # moving towards
                )
                if cd == "stagnant":
                    continue
                actions = {
                    "up": [y2-1, x2],
                    "down": [y2+1, x2],
                    "left": [y2, x2-1],
                    "right": [y2, x2+1],
                    # "stagnant": [y2, x2]
                }
                y2, x2 = actions[cd]
                if within(y2, x2):
                    field[y2][x2][0] += 25 if field[y2][x2][0] <= 200 else 0

erode(100000)
Image.fromarray(field).show()
