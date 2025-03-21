from tkinter import *
from Pixel import Pixel
import time, random
import numpy as np

class Obstacles:
    def __init__(self, canv, nrow, ncol, scale, c=2):
        self.canv = canv
        self.nrow = nrow
        self.ncol = ncol
        self.icolor = c
        self.scale = scale
        self.body = []
        self.i = None
        self.j = None

    def delete(self):
        for b in self.body:
            b.delete()
        self.body = []

    def activate(self, i=None, j=None, pattern=None):
        if i is None:
            i = self.nrow // 2
        if j is None:
            j = self.ncol // 2

        self.i = i % self.nrow
        self.j = j % self.ncol

        # Delete all obstacles and ensure canvas processes this before drawing new ones
        self.canv.delete("obstacle")
        self.canv.update()

        self.body = []
        for iloc in range(len(pattern)):
            for jloc in range(len(pattern[0])):
                if pattern[iloc][jloc] != 0:
                    self.body.append(Pixel(self.canv, (self.i + iloc), (self.j + jloc),
                                            self.nrow, self.ncol, self.scale, self.icolor, vector=[0, 0], tags="obstacle"))



    def down(self):
        for b in self.body:
            b.down()
            b.next()
        self.i = (self.i + 1) % self.nrow

    def up(self):
        for b in self.body:
            b.up()
            b.next()
        self.i = (self.i - 1) % self.nrow
            
    def left(self):
        for b in self.body:
            b.left()
            b.next()
        self.j = (self.j - 1) % self.ncol
            
    def right(self):
        for b in self.body:
            b.right()
            b.next()
        self.j = (self.j + 1) % self.ncol
        
    def swipe_left(self):
        while self.j >= 0:
            time.sleep(0.03) 
            self.left()
            self.canv.update()
        self.canv.delete("obstacle")
        

    @staticmethod
    def random_select(canv, nrow, ncol, scale):
        t1 = Box(canv, nrow, ncol, scale)
        t2 = Tree(canv, nrow, ncol, scale)
        t3 = Desk(canv, nrow, ncol, scale)
        return random.choice([t1, t2, t3])

class Box(Obstacles):
    def __init__(self, canv, nrow, ncol, scale):
        super().__init__(canv, nrow, ncol, scale, c=2)
        self.name = "box"
        self.pattern = [[1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1]]

class Tree(Obstacles):
    def __init__(self, canv, nrow, ncol, scale):
        super().__init__(canv, nrow, ncol, scale, c=3)
        self.name = "tree"
        self.pattern = [[1, 1, 1],
                        [1, 1, 1],
                        [0, 1, 0]]

class Desk(Obstacles):
    def __init__(self, canv, nrow, ncol, scale):
        super().__init__(canv, nrow, ncol, scale, c=4)
        self.name = "desk"
        self.pattern = [[1, 1, 1],
                        [1, 0, 1],
                        [1, 0, 1]]

#########################################################
############# Testing Functions #########################
#########################################################
def delete_all(canvas):
    canvas.delete("all")
    print("Delete All")

def test1(root, canvas, nrow, ncol, scale):
    print("")
    t0 = Box(canvas, nrow, ncol, scale)   # instantiate
    t1 = Tree(canvas, nrow, ncol, scale)   # instantiate
    t2 = Desk(canvas, nrow, ncol, scale)   # instantiate
    objects = [t0, t1, t2]
    for t in objects:
        print(t.name)

    # Place the objects at different positions.
    for i in range(4):
        for j in range(2):
            k = i * 2 + j
            objects[k].activate(5 + i * 10, 8 + j * 10, objects[k].pattern)
      
def test2(root, canvas, nrow, ncol, scale):
    print("Moving Obstacle Object")
    obj = Obstacles.random_select(canvas, nrow, ncol, scale)  # choose at random
    print(obj.name)
        
    # Tkinter bindings for movement:
    root.bind("<Up>", lambda e: obj.up())
    root.bind("<Down>", lambda e: obj.down())
    root.bind("<Left>", lambda e: obj.left())
    root.bind("<Right>", lambda e: obj.right())

    obj.activate(pattern=obj.pattern)  # Defaults to center if no coordinates provided.

def test3(root, canvas, nrow, ncol, scale):
    print("Testing swipe_left function")
    while not root.stop_swipe:
        obj = Obstacles.random_select(canvas, nrow, ncol, scale)  # choose at random
        print(obj.name)
        obj.activate(i=nrow // 2, j=ncol - 1, pattern=obj.pattern)
        obj.swipe_left()

def stop_swipe(root):
    root.stop_swipe = True

#########################################################
############# Main code #################################
#########################################################
def main():
    # Create a window and canvas 
    root = Tk()  # instantiate a tkinter window
    root.stop_swipe = False
    nrow = 40
    ncol = 80
    scale = 20
    canvas = Canvas(root, width=ncol * scale, height=nrow * scale, bg="black")
    canvas.pack()

    # Bind keys to testing functions.
    root.bind("1", lambda e: test1(root, canvas, nrow, ncol, scale))
    root.bind("2", lambda e: test2(root, canvas, nrow, ncol, scale))
    root.bind("3", lambda e: test3(root, canvas, nrow, ncol, scale))
    root.bind("<d>", lambda e: delete_all(canvas))
    root.bind("<s>", lambda e: stop_swipe(root))

    root.mainloop()  # Wait until the window is closed        

if __name__ == "__main__":
    main()