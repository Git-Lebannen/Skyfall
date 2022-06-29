# three helper functions that are used to import: 

# - a csv file (importCsvFile() returns a list of lists, can be used to read the values of the csv file)
# - a folder of png files (importFrames() returns a list of pg.image objects, used to import animation frames)
# - a png file (importTileSet() returns a list of pg.Surface objects, is used to import a png file that contains more than one tile as multiple tile sized surfaces, e.g. terrain tile sets)

import pygame as pg
from csv import reader
from os import walk
from settings import tileSize

def importCsvFile(path):
    fileList = []

    with open(path) as f:
        file = reader(f, delimiter = ",")
        
        for row in file:
            fileList.append(row)

    return fileList

def importFrames(path):
    images = []

    for unused, unused, folder in walk(path):
        for index in range(len(folder)):
            images.append(pg.image.load(f"{path}/{(index + 1)}.png").convert_alpha())

    return images

def importTileSet(path):
    file = pg.image.load(path).convert_alpha()

    numDx = int(file.get_width() / tileSize)
    numDy = int(file.get_height() / tileSize)

    tilesSet = []
    for row in range(numDy):
        for col in range(numDx):
            x = col * tileSize
            y = row * tileSize

            tile = pg.Surface((tileSize, tileSize), flags = pg.SRCALPHA)
            tile.blit(file, (0, 0), pg.Rect(x, y, tileSize, tileSize))
            tilesSet.append(tile)

    return tilesSet