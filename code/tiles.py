# classes related to the graphics tiles used to render the level

import pygame as pg
from helpers import importFrames

# standard tile class which creates tile sprites, all other tile classes inherit from this class 
class Tile(pg.sprite.Sprite):
    def __init__(self, tileSize, x, y):
        super().__init__()
        self.image = pg.Surface((tileSize, tileSize))
        self.rect = self.image.get_rect(topleft = (x, y))

# an animated tile class for trees
class TreeTile(pg.sprite.Sprite):
    def __init__(self, x, y, path):
        super().__init__()
        self.frames = importFrames(path)
        self.frameIndex = 0
        self.animationSpeed = 0.05
        self.image = self.frames[self.frameIndex]
        self.rect = self.image.get_rect(bottomleft = (x, y + 64))

    def animate(self):
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(self.frames):
            self.frameIndex = 0
        self.image = self.frames[int(self.frameIndex)]

    def update(self):
        self.animate()

# static tile class, used to display any non animated tiles within the level (except for background terrain)
class StaticTile(Tile):
    def __init__(self, tileSize, x, y, image):
        super().__init__(tileSize, x, y)
        self.image = image

# a "subclass" of the static tile class, used to display the backgorund terrain within the level which moves inverted to the players movement
class bgTerrainTile(StaticTile):
    def __init__(self, tileSize, x, y, image):
        super().__init__(tileSize, x, y, image)
        self.pos = self.rect.center 

    def update(self, posChange):
        posX = self.pos[0]
        posY = self.pos[1]
        posX += posChange[0]
        posY += posChange[1]
        self.pos = (posX, posY) 
        self.rect = self.image.get_rect(center = self.pos)

# a tile class that is used for animated tiles, animation of a tile happens within the class
class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = importFrames(path)
        self.frameIndex = 0
        self.animationSpeed = 0.05
        self.image = self.frames[self.frameIndex]

    def animate(self):
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(self.frames):
            self.frameIndex = 0
        self.image = self.frames[int(self.frameIndex)]

    def update(self):
        self.animate()
