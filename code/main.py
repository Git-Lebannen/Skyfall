# main file that runs an instance of a level class

import pygame as pg
from lvl import Lvl
from menu import Menu
from sys import exit
from random import randrange    
from settings import *

class Game:
    def __init__(self):
        # menu and level audio
        self.lvlMusicDay = [pg.mixer.Sound("../audio/tracks/HaquinTrackAcorn.ogg"), pg.mixer.Sound("../audio/tracks/HaquinTrackAsAboveSoBelow.ogg")]
        self.lvlMusicNight = [pg.mixer.Sound("../audio/tracks/KisnouTrackShorterDays.ogg"), pg.mixer.Sound("../audio/tracks/WisangaTrackMeteorite.ogg")]

        # turn down volume for level music
        for i in range(len(self.lvlMusicDay)):
            self.lvlMusicDay[i].set_volume(0.2)
            self.lvlMusicNight[i].set_volume(0.2)

        self.menuMusic = pg.mixer.Sound("../audio/tracks/HaquinTrackForestOfTheAncients.ogg")

        # highest unlocked level
        self.unlockedLvls = 0

        # create first Menu instance and loop menu Music
        self.Menu = Menu(0, self.unlockedLvls, screen, self.createLvl)
        self.status = "menu"
        self.playMenuMusic()

    def createLvl(self, currentLvl):
        self.lvl = Lvl(currentLvl, screen, self.createMenu)
        self.status = "lvl"
        self.playLvlMusic()

    def createMenu(self, currentLvl, newUnlockedLvls):
        if newUnlockedLvls > self.unlockedLvls:
            self.unlockedLvls = newUnlockedLvls
        self.Menu = Menu(currentLvl, self.unlockedLvls, screen, self.createLvl)
        self.status = "menu"
        self.playMenuMusic()

    def playLvlMusic(self):
        pg.mixer.fadeout(3000)
        if self.lvl.dayTime == "day":
            self.lvlMusicDay[randrange(0, 2)].play()
        else:
            self.lvlMusicNight[randrange(0, 2)].play()

    def playMenuMusic(self):
        pg.mixer.fadeout(3000)
        self.menuMusic.play(loops = -1)

    def run(self):
        if self.status == "menu":
            self.Menu.run()
        else:
            self.lvl.run()

pg.init()
screen = pg.display.set_mode((screenW, screenH))
pg.display.set_caption("Skyfall")
pg.display.set_icon(pg.image.load("../graphics/screen_icon/icon.png").convert_alpha())
clock = pg.time.Clock()
gameSpeed = 60
game = Game()

while True:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    game.run()
    pg.display.update()
    clock.tick(60)