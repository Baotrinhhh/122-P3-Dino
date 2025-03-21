from tkinter import *
from Pixel import Pixel
import time, random
import numpy as np

# 5x5 Dino pattern: adjust the 1's and 0's to form your desired shape.
dino = np.array([
    [0, 0, 1, 1, 1, 1],
    [0, 0, 1, 1, 0, 1],
    [0, 0, 1, 1, 1, 1],
    [0, 0, 1, 1, 0, 0],
    [1, 0, 1, 1, 1, 1],
    [1, 0, 1, 1, 0, 0],
    [1, 1, 1, 1, 0, 0],
    [0, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 0]
])

class Dino:
    def __init__(self, canv, nrow, ncol, scale, c=2, pattern=dino):
        self.canv = canv
        self.nrow = nrow
        self.ncol = ncol
        self.scale = scale
        self.icolor = c
        self.pattern = pattern
        self.h, self.w = pattern.shape
        self.body = []
        self.i = None
        self.j = None

    def delete(self):
        for b in self.body:
            b.delete()
        self.body = []

    def activate(self, i=None, j=None):
        # Default to center of the grid if no coordinates are provided.
        if i is None:
            i = self.nrow // 2
        if j is None:
            j = self.ncol // 2

        self.i = i % self.nrow
        self.j = j % self.ncol

        self.delete()  # Clear any existing pixels.
        self.body = []
        for iloc in range(self.h):
            for jloc in range(self.w):
                if self.pattern[iloc, jloc] != 0:
                    self.body.append(Pixel(self.canv, (self.i + iloc), (self.j + jloc),
                                             self.nrow, self.ncol, self.scale, self.icolor, vector=[0, 0], tags = "dino"))

    def up(self):
        for b in self.body:
            b.up()
            b.next()
        self.i = (self.i - 1) % self.nrow

    def down(self):
        for b in self.body:
            b.down()
            b.next()
        self.i = (self.i + 1) % self.nrow

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
        
    def jump(self):
        # Move up
        for _ in range(5):
            self.up()
            self.canv.update()
            time.sleep(0.08)
        # Move down
        for _ in range(5):
            self.down()
            self.canv.update()
            time.sleep(0.08)
            

# Test functions
def delete_all(canvas):
    canvas.delete("all")
    print("Deleted All")

def test_dino(root, canvas, nrow, ncol, scale):
    d = Dino(canvas, nrow, ncol, scale)
    d.activate(nrow // 2, ncol // 2)
    
    # Bind arrow keys to move the dino.
    root.bind("<Up>", lambda e: d.up())
    root.bind("<Down>", lambda e: d.down())
    root.bind("<Left>", lambda e: d.left())
    root.bind("<Right>", lambda e: d.right())
    root.bind("<space>", lambda e: d.jump())

def main():
    root = Tk()
    nrow = 40
    ncol = 80
    scale = 20
    canvas = Canvas(root, width=ncol * scale, height=nrow * scale, bg="black")
    canvas.pack()

    # Bind a key for clearing the canvas.
    root.bind("d", lambda e: delete_all(canvas))
    
    test_dino(root, canvas, nrow, ncol, scale)
    root.mainloop()

if __name__ == "__main__":
    main()