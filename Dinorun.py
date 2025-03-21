from tkinter import *
from Pixel import Pixel
import time

class Game:
    def __init__(self,root,nrow=30,ncol=12,scale=20):
        super().__init__(root,nrow,ncol,scale)
        self.block=None
        self.__game_over=False
        self.__pause=False

    