import pygame as pg
from time import sleep # to pause between receiving inputs
from helpers import importFrames
from lvlData import lvls
from settings import font, tileSize, screenH

# selector arrow
class Selector(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # animation
        self.frames = importFrames("../graphics/menu/selector")
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.image = self.frames[self.frameIndex]
        self.rect = self.image.get_rect(midright = pos)

    def animate(self):
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(self.frames):
            self.frameIndex = 0
        self.image = self.frames[int(self.frameIndex)]
    
    def update(self):
        self.animate()

# selection panels
class Selection(pg.sprite.Sprite):
    def __init__(self, index, status):
        super().__init__()

        # vertical distance between two selections 
        self.gap = 30

        self.status = status       
        if self.status == "available":
            # animation if selection is available
            self.frames = importFrames("../graphics/menu/selectionA")
            self.frameIndex = 0
            self.animationSpeed = 0.05
            self.image = self.frames[int(self.frameIndex)]
            self.rect = self.image.get_rect(topleft = (tileSize * 2, tileSize * (index * 2) + index * self.gap))
        else:
            # no animation if selection is locked
            self.image = pg.image.load("../graphics/menu/selectionL.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = (tileSize * 2, tileSize * (index * 2) + index * self.gap))

    def animate(self):
        # only animate available selections
        if self.status == "available":
            self.frameIndex += self.animationSpeed
            if self.frameIndex >= len(self.frames):
                self.frameIndex = 0
            self.image = self.frames[int(self.frameIndex)]
    
    def move(self, y):
        self.rect.top += y

    def update(self):
        self.animate()

# text on the selection
class SelectionInfo(pg.sprite.Sprite):
    def __init__(self, selection, index, time):
        super().__init__()
        if time == 0.0:
            time = "N/A"
        self.image = font.render(f"Level {index}, Best: {time}s", True, "White") 
        selectionPos = selection.rect.topleft
        offset = pg.Vector2(10, 31) 
        self.rect = self.image.get_rect(topleft = (selectionPos + offset))

    def move(self, y):
        self.rect.top += y

class Menu:
    def __init__(self, startLvl, unlockedLvls, screen, createLvl):

        # setup
        self.screen = screen
        self.unlockedLvls = unlockedLvls
        self.currentLvl = startLvl
        self.createLvl = createLvl

        # animation
        self.frameIndex = 0
        self.animationSpeed = 0.05
        self.backgroundFrames = importFrames("../graphics/menu/background")

        # setup selection panels and selector
        self.setupSelections()
        self.setupSelector()

# setup the selections with the current best time values every time a new instance of the overworld class is created
    def setupSelections(self):
        self.selections = pg.sprite.Group()
        self.selectionInfo = pg.sprite.Group()

        for i in range(len(lvls)):
            if i <= self.unlockedLvls:
                selectionSprite = Selection(i, "available")               
                selectionInfo = SelectionInfo(selectionSprite, i, lvls[i]["time"])
                self.selectionInfo.add(selectionInfo)
            else:
                selectionSprite = Selection(i, "locked")

            self.selections.add(selectionSprite)

    def setupSelector(self):
        self.selector = pg.sprite.GroupSingle()
        selectorSprite = Selector(self.selections.sprites()[self.currentLvl].rect.midleft)
        self.selector.add(selectorSprite)


    def input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_DOWN] and self.currentLvl < self.unlockedLvls:
            self.currentLvl += 1
            sleep(0.1)
        elif keys[pg.K_UP] and self.currentLvl > 0:
            self.currentLvl -= 1
            sleep(0.1)
        elif keys[pg.K_RETURN]:
            self.createLvl(self.currentLvl)

    def animate(self):
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(self.backgroundFrames):
            self.frameIndex = 0
        self.screen.blit(self.backgroundFrames[int(self.frameIndex)], (0, 0))
    
# updates the selector and the selection panels, also animates the background
    def update(self):
        self.selector.sprite.rect.midright = self.selections.sprites()[self.currentLvl].rect.midleft
        if self.selector.sprite.rect.top > screenH:
            for sprite in self.selections.sprites():
                sprite.move(-(tileSize * 2))
            for sprite in self.selectionInfo.sprites():
                sprite.move(-(tileSize * 2))
        elif self.selector.sprite.rect.top < 0:
            for sprite in self.selections.sprites():
                sprite.move(tileSize * 2)
            for sprite in self.selectionInfo.sprites():
                sprite.move(tileSize * 2)             
        self.selector.update()
        self.selections.update()
        self.animate()

    def run(self):
        # update
        self.input()
        self.update()

        # display
        self.selections.draw(self.screen)
        self.selectionInfo.draw(self.screen)
        self.selector.draw(self.screen)