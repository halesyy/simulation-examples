
from PIL import Image
import numpy as np
from random import randint, random, choice
from time import sleep

class Sim:
    names = [
        "Jack",
        "Chris",
        "Farley",
        "Donald",
        "Lachlan",
        "Natasha",
        "Louise",
        "Peter",
        "Ellise",
        "Ellen",
        "Rebekah"
    ]

    def __init__(self, w=100, h=100):
        self.w = w
        self.h = h
        """building np array field"""
        self.field = Image.new("RGBA", (self.w, self.h), color="black")
        self.field = np.array(self.field)
        self.pixels = [(y, x) for y in range(self.w) for x in range(self.h)]
        self.pixels = set(self.pixels)
        self.people = []
        self.tl = [] # taken land

    """
    returns a list of tuples of lands
    currently being occupied by individuals.
    """
    def taken_land(self):
        peoples_spots = [(person["y"], person["x"]) for person in self.people]
        return peoples_spots

    def refresh_taken_land(self): # just a refresh state func
        self.tl = set(self.taken_land())

    def find_safe_spot(self, y=False, x=False):
        while (y == False or x == False) or (y, x) in self.taken_land():
            y, x = randint(0, self.w-1), randint(0, self.h-1)
        return y, x

    def person(self, random=False, y=False, x=False):
        y, x = self.find_safe_spot(y, x)
        self.people.append({
            "y": y,
            "x": x,
            "gender": choice(["male", "female"]),
            "name": choice(self.names)
        })

    def view(self, save=False):
        persons = self.people
        tfld = self.field.copy() # copy field
        for person in persons:
            y, x = person["y"], person["x"]
            tfld[y][x] = [255, 255, 255, 255]
        image = Image.fromarray(tfld)
        if save:
            image.save("board.png")
        else:
            image.show()

    """
    move someone in a random or certain
    direction.
    """
    def safe(self, y, x=False):
        if x == False: y, x = y
        return True if (y < self.h and y >= 0) and (x < self.w and y >= 0) else False
    def move(self, y, x, random=False, direction=False):
        movements = {
            "u": (y-1, x),
            "d": (y+1, x),
            "l": (y, x-1),
            "r": (y, x+1),
            "tr": (y-1, x+1),
            "tl": (y-1, x-1),
            "br": (y+1, x+1),
            "bl": (y+1, x-1)
        }
        movements = {k: v for k, v in movements.items() if v in self.pixels and v not in self.tl}
        if len(movements) == 0: # filtered fully down, sit still!
            return y, x
        movement = movements[choice(list(movements.keys()))] if random == True else movements[direction]
        return movement

    def move_person(self, index, random=False, direction=False):
        person = self.people[index]
        y, x = person["y"], person["x"]
        y, x = self.move(y, x, random, direction)
        self.people[index]["y"] = y
        self.people[index]["x"] = x




s = Sim(w=75, h=75)

for i in range(5000):
    s.person(random=True)
s.refresh_taken_land()

# 50    = 0.001s
# 5,000 = 4.500s

import time

while True:
    srt = time.time()
    for i in range(len(s.people)):
        s.move_person(i, random=True) # move in random direction
        s.refresh_taken_land()
    s.view(save=True)
    # time.sleep(0.1)
    end = time.time()
    print(f"t2l: {end-srt}s")
