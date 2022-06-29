# important variables
import pygame.font

# the size of a square shaped tile within a level, most graphics are based around 64x64 png images
tileSize = 64

# the width and height of the pygame window
screenW = 14 * tileSize
screenH = 12 * tileSize 

# the game font
pygame.font.init()
font = pygame.font.Font("../graphics/ui/Pixeau.ttf", 22) 

# a dict that holds the locations of the border within a level that triggers screen scrolling
camBorders = {
    "left": 200,
    "right": 200,
    "top": 150,
    "bottom": 150
}