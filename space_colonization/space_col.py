import cv2 as cv
import random
import numpy as np
from numpy.typing import ArrayLike
import math

class Vector2D:
    def __init__(self, x, y):
        self.x: float = x
        self.y: float = y

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def normalised(self):
        m = self.mag()
        return Vector2D(self.x / m, self.y / m)

    def mag(self) -> float:
        return (self.mag_sq())**0.5

    def mag_sq(self) -> float:
        return (self.x**2 + self.y**2)

    def get_int_arr(self):
        return np.array([int(self.x), int(self.y)])

    def __repr__(self):
        return f'({self.x}, {self.y})'



class Attractor:
    def __init__(self, pos: Vector2D):
        self.pos = pos

    def draw(self, img: ArrayLike):
        cv.circle(img, (int(self.pos.x), int(self.pos.y)), 10, (100,0,0))


class Node:
    def __init__(self, pos: Vector2D):
        self.pos = pos
        self.attractors: list(Attractor) = []
        self._size = 30
        self.parent = None

    def set_size(self, size):
        if size >= 1:
            self._size = size
        else:
            self._size = 1

    def get_size(self):
        return self._size

    def draw(self, img: ArrayLike):
        # cv.circle(img, (int(self.pos.x), int(self.pos.y)), int(self.size), (0,100,0))
        if self.parent:
            cv.line(img, (int(self.pos.x), int(self.pos.y)), (int(self.parent.pos.x), int(self.parent.pos.y)), (0,100,0), int(self._size))

    def add_attractor(self, a: Attractor):
        self.attractors.append(a)

    def clear_attractors(self):
        self.attractors = []
    
    def __repr__(self):
        return f'Node at {self.pos}'


class Sim:
    def __init__(self, width, height, starting_attractors = 250):
        self.width = width
        self.height = height
        self.attractors = []
        self.nodes = []
        self.running = True

        self.kill_dist = 40
        self.attractor_range = 1000
        self.speed = 20

        self.wiggle = 5

        for i in range(starting_attractors):
            # new_pos = Vector2D(random.randrange(self.width), random.randrange(self.height//2))
            r = random.randrange(self.width//3)
            a = random.uniform(0, 2 * math.pi)
            x = r * math.cos(a) + self.width //2
            y = r * math.sin(a) + self.height // 3
            new_pos = Vector2D(x, y)
            self.attractors.append(Attractor(new_pos))

        
        starting_pos = Vector2D(self.width //2, self.height - 20)
        self.nodes.append(Node(starting_pos))

        self.img = np.zeros((self.width, self.height, 3), dtype=np.uint8)

    def update(self):
        for n in self.nodes:
            n.clear_attractors()

        # Iterate through attractors, finding nearest node (if any) for each one
        dead_attractors = set()
        for a in self.attractors:
            nearest_node = None
            nearest_dist_sq  = 1000000000 # A big number, fix this...
            for n in self.nodes:
                dist_v = a.pos - n.pos
                dist_squ = dist_v.mag_sq()
                if dist_squ < self.kill_dist ** 2:
                    dead_attractors.add(a)
                # elif dist_squ < nearest_dist_sq:
                elif dist_squ < self.attractor_range**2 and dist_squ < nearest_dist_sq:
                    nearest_dist_sq = dist_v.mag_sq()
                    nearest_node = n
            if nearest_node != None:
                cv.line(self.img, a.pos.get_int_arr(), nearest_node.pos.get_int_arr(), (0,0,100), 2)
                nearest_node.add_attractor(a)
        
        for a in dead_attractors:
            self.attractors.remove(a)
        
        # work out the sum of the 1/d for attractors to each node
        new_nodes = []
        for n in self.nodes:
            if len(n.attractors) > 0:
                distance_sum = Vector2D(0,0)
                for a in n.attractors:
                    dist_v = (a.pos - n.pos)
                    dist = dist_v.mag()

                    distance_sum = distance_sum + dist_v.normalised() * (1/dist)
                
                # Create the new node
                wiggle = Vector2D(random.randint(-self.wiggle//2, self.wiggle//2), random.randint(-self.wiggle//2, self.wiggle//2))
                new_pos = n.pos + distance_sum.normalised() * self.speed + wiggle
                new_n = Node(Vector2D(new_pos.x, new_pos.y))
                new_n.set_size(n.get_size() * 0.95)
                new_n.parent = n
                new_nodes.append(new_n)
            # else:
            #     n.set_size(10)

        self.nodes.extend(new_nodes)
            

    def draw(self):
        self.img = np.zeros((self.width, self.height, 3), dtype=np.uint8)

        for a in self.attractors:
            a.draw(self.img)
        
        for n in self.nodes:
            n.draw(self.img)

        cv.imshow("Window", self.img)
        if cv.waitKey(1) == 27:
            self.running = False

sim = Sim(1200, 1200, 600)
while sim.running:
    sim.update()
    sim.draw()    

