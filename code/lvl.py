# three important classes related to the level, particle animations, and the shifting/scrolling of the screen 

import pygame as pg
from tiles import Tile, TreeTile, StaticTile, AnimatedTile, bgTerrainTile
from player import Player
from random import random
from lvlData import lvls
from helpers import *
from settings import *

class Lvl():
    
    def __init__(self, currentLvl, screen, createMenu):    
        # audio
        self.groundLand = pg.mixer.Sound("../audio/sfx/groundLand.ogg")
        self.playerBreak = pg.mixer.Sound("../audio/sfx/playerBreak.ogg")
        self.playerStrain = pg.mixer.Sound("../audio/sfx/playerStrain.ogg")
        
        # ui
        self.ui = UI(screen)

        # general setup
        self.screen = screen
        pg.display.set_caption(f"Skyfall > Level {currentLvl}")
        self.currentX = 0
        self.createMenu = createMenu
        
        # Menu connection
        self.createMenu = createMenu
        self.currentLvl = currentLvl
        self.lvlData = lvls[self.currentLvl]
        self.newUnlockedLvls = self.lvlData["unlock"]
        self.bgColor = self.lvlData["color"]
        self.dayTime = self.lvlData["dayTime"]
        self.maxTime = self.lvlData["maxTime"]
        # player
        playerMap = importCsvFile(self.lvlData["player"])
        self.player = pg.sprite.GroupSingle()
        self.playerGoal = pg.sprite.GroupSingle()
        self.setupPlayer(playerMap)
        self.airtime = 0.0


        # grass setup
        grassMap = importCsvFile(self.lvlData["grass"])
        self.grassSprites = self.createTiles(grassMap, "grass")
        
        # fgTerrain setup
        fgTerrainMap = importCsvFile(self.lvlData["fgTerrain"])
        self.fgTerrainSprites = self.createTiles(fgTerrainMap, "fgTerrain")

        # bgTerrain setup
        bgTerrainMap = importCsvFile(self.lvlData["bgTerrain"])
        self.bgTerrainSprites = self.createTiles(bgTerrainMap, "bgTerrain")

        # bgDecoration setup
        bgDecorationMap = importCsvFile(self.lvlData["bgDecoration"])
        self.bgDecorationSprites = self.createTiles(bgDecorationMap, "bgDecoration")

        # shadow setup
        shadowMap = importCsvFile(self.lvlData["shadow"])
        self.shadowSprites = self.createTiles(shadowMap, "shadow")

        # level barrier setup
        barrierMap = importCsvFile(self.lvlData["barrier"])
        self.barrierSprites = self.createTiles(barrierMap, "barrier")

        # tree setup
        treeMap = importCsvFile(self.lvlData["tree"])
        self.treeSprites = self.createTiles(treeMap, "tree")

        # sprite group groups
        self.visibleSprites = ScrollableSprites()
        self.visibleSprites.add(self.bgTerrainSprites, self.treeSprites, self.bgDecorationSprites, self.player, self.shadowSprites, self.fgTerrainSprites, self.grassSprites, self.playerGoal)

        self.activeSprites = pg.sprite.Group()
        self.activeSprites.add(self.bgDecorationSprites, self.grassSprites, self.treeSprites, self.player, self.playerGoal)

        self.collideSprites = pg.sprite.Group()
        self.collideSprites.add(self.fgTerrainSprites)

        # particles
        self.importRunParticles()
        self.particleIndex = 0
        self.particleAnimationSpeed = 0.15
        self.onGrass = False

        # particles
        self.particle = pg.sprite.GroupSingle()
        self.playerOnGround = False

        self.timerStart = False
        self.timer = None

# particle related
    def importRunParticles(self):
        self.runParticles = importFrames("../graphics/player/particles/run/default")
        self.grassParticles = importFrames("../graphics/player/particles/run/grass")

    def animateRunParticles(self):
        player = self.player.sprite
        if player.status == "run" and player.onGround:

            self.particleIndex += self.particleAnimationSpeed
            if self.particleIndex >= len(self.runParticles):
                self.particleIndex = 0

            if self.onGrass:
                particle = self.grassParticles[int(self.particleIndex)]
            else:
                particle = self.runParticles[int(self.particleIndex)]

            if player.facingRight:
                if self.onGrass:
                    pos = player.rect.bottomleft - self.visibleSprites.offset - pg.math.Vector2(6, 14)
                else:
                    pos = player.rect.bottomleft - self.visibleSprites.offset - pg.math.Vector2(6, 10)
                self.screen.blit(particle, pos)

            else:
                if self.onGrass:
                    pos = player.rect.bottomright - self.visibleSprites.offset - pg.math.Vector2(6, 14)
                else:
                    pos = player.rect.bottomright - self.visibleSprites.offset - pg.math.Vector2(6, 10)
                flippedParticle = pg.transform.flip(particle, True, False)
                self.screen.blit(flippedParticle, pos)

    def createJumpParticles(self, pos):
        if self.player.sprite.facingRight:
            pos += pg.math.Vector2(4, -16)
        else:
            pos += pg.math.Vector2(-4, -16)
        particle = ParticleEffect(pos, "jump", self.onGrass)
        self.particle.add(particle)
        self.visibleSprites.add(self.particle)
        self.activeSprites.add(self.particle)

    def createLandingParticles(self):
        if not self.playerOnGround and self.player.sprite.onGround and not self.particle.sprites():
            if self.player.sprite.facingRight:
                offset = pg.math.Vector2(0, -20)
            else:
                offset = pg.math.Vector2(0, -20)
            particle = ParticleEffect(self.player.sprite.rect.midbottom + offset, "land", self.onGrass)
            self.particle.add(particle)
        self.visibleSprites.add(self.particle)
        self.activeSprites.add(self.particle)

    def checkOnGrass(self):
        player = self.player.sprite
        self.onGrass = False

        for sprite in self.grassSprites.sprites():
            if player.rect.bottom == sprite.rect.top :
                self.onGrass = True

# level setup related
    def createTiles(self, map, type):
        sprites = ScrollableSprites()

        for rowIndex, row in enumerate(map):
            for colIndex, val in enumerate(row):
                if val != "-1":
                    x = colIndex * tileSize
                    y = rowIndex * tileSize

                    if type == "grass":
                        if val == "0":
                            sprite = AnimatedTile(tileSize, x, y,  "../graphics/level/environment/decoration/foreground/left_grass_part")
                        elif val == "1":
                            sprite = AnimatedTile(tileSize, x, y,  "../graphics/level/environment/decoration/foreground/center_grass_part")
                        elif val == "2":
                            sprite = AnimatedTile(tileSize, x, y,  "../graphics/level/environment/decoration/foreground/right_grass_part")
                        else:
                            sprite = AnimatedTile(tileSize, x, y,  "../graphics/level/environment/decoration/foreground/single_grass")

                    elif type == "fgTerrain":
                        fgTerrainTiles = importTileSet("../graphics/level/environment/terrain/fgTerrainTiles.png")
                        sprite = StaticTile(tileSize, x, y, fgTerrainTiles[int(val)])

                    elif type == "bgTerrain":
                        bgTerrainTiles = importTileSet("../graphics/level/environment/terrain/bgTerrainTiles.png")
                        sprite = bgTerrainTile(tileSize, x, y, bgTerrainTiles[int(val)])

                    elif type == "bgDecoration":
                        if val == "0":
                            sprite = AnimatedTile(tileSize, x, y, "../graphics/level/environment/decoration/background/left_bush_part")
                        elif val == "1":
                            sprite = AnimatedTile(tileSize, x, y, "../graphics/level/environment/decoration/background/center_bush_part")
                        elif val == "2":
                            sprite = AnimatedTile(tileSize, x, y, "../graphics/level/environment/decoration/background/right_bush_part")
                        elif val == "3":
                            sprite = AnimatedTile(tileSize, x, y, "../graphics/level/environment/decoration/background/single_bush")
                        else:
                            sprite = AnimatedTile(tileSize, x, y, "../graphics/level/environment/decoration/background/grass_straws")

                    elif type == "shadow":
                        shadowTiles = importTileSet("../graphics/level/environment/decoration/foreground/shadowTiles.png")
                        sprite = StaticTile(tileSize, x, y, shadowTiles[int(val)])

                    elif type == "barrier":
                        sprite = Tile(tileSize, x, y)

                    elif type == "tree":
                        if val == "0":
                            sprite = TreeTile(x, y, ("../graphics/level/environment/decoration/background/shortTree"))
                        else:
                            sprite = TreeTile(x, y, ("../graphics/level/environment/decoration/background/tallTree"))

                    sprites.add(sprite)

        return sprites

    def setupPlayer(self, map):
        for rowIndex, row in enumerate(map):
            for colIndex, val in enumerate(row):
                x = colIndex * tileSize
                y = rowIndex * tileSize

                if val == "0":
                    sprite = Player((x, y), self.screen, self.createJumpParticles)
                    self.player.add(sprite)
                if val == "1":
                    sprite = AnimatedTile(tileSize, x, y, "../graphics/level/environment/player_goal")
                    self.playerGoal.add(sprite)

# player movement related
    def xCollide(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.collideSprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.onLeft = True
                    self.currentX = player.rect.left

                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.onRight = True
                    self.currentX = player.rect.right

        if player.onLeft and (player.rect.left < self.currentX or player.direction.x >= 0):
            player.onLeft = False
        if player.onRight and (player.rect.left > self.currentX or player.direction.x <= 0):
            player.onRight = False

    def yCollide(self):
        player = self.player.sprite
        directionY = player.direction.y
        player.applyGrav()

        for sprite in self.collideSprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if directionY > 0:
                    player.jumped = False
                    self.airtime = player.airtime
                    player.airtime = 0.0
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGround = True
                elif directionY < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.onCeiling = True

        # get player location to correct animation rectangles
        if player.onGround and directionY < 0 or directionY > 1:
            player.onGround = False
        if player.onCeiling and directionY > 0:
            player.onCeiling = False   

    def getPlayerOnGround(self):
        if self.player.sprite.onGround:
            self.playerOnGround = True
        else:
            self.playerOnGround = False

# scroll function for bgTerrain
    def scrollBgTerrain(self):
        player = self.player.sprite
        directionX = player.direction.x
        directionY = player.direction.y
        posChange = (0, 0)

        if directionX > 0 and player.rect.right != self.currentX:
            posChange = (-1, 0)
        if directionX < 0 and player.rect.left != self.currentX:
            posChange = (1, 0)
        if directionY < 0:
            posChange = (0, 1)           
        if directionY > player.grav:
            posChange = (0, -1)    
        self.bgTerrainSprites.update(posChange)

# lvl escape states
    def checkDeath(self):
        if self.timerStart:
            for sprite in self.barrierSprites.sprites():
                if sprite.rect.colliderect(self.player.sprite.rect):
                    self.createMenu(self.currentLvl, 0)
                if self.player.sprite.airtime > 3:
                    self.createMenu(self.currentLvl, 0)
                if self.timer.runtime > self.maxTime:
                    self.createMenu(self.currentLvl, 0)
 
    def checkWin(self):
        if pg.sprite.spritecollide(self.player.sprite, self.playerGoal, False):
            if self.lvlData["time"] == 0.0:
                self.lvlData["time"] = "{:.2f}".format(self.timer.runtime)
            elif float(self.timer.runtime) < float(self.lvlData["time"]):
                self.lvlData["time"] = "{:.2f}".format(self.timer.runtime)
            self.createMenu(self.currentLvl, self.newUnlockedLvls)

    def run(self):
        # run the entire game / lvl
        self.player.sprite.inputTimer()
        if self.player.sprite.allowInput and self.timer == None:
            self.timer = Timer(self.screen)
            self.timerStart = True

        # game end states
        self.checkDeath()
        self.checkWin()

        self.screen.fill(self.bgColor)
        self.scrollBgTerrain()
        self.activeSprites.update()
        self.checkOnGrass()

        self.xCollide()
        self.getPlayerOnGround()
        self.yCollide()
        self.createLandingParticles()

        self.animateRunParticles()
        self.visibleSprites.customDraw(self.player)

        if self.dayTime == "night":
            overlay = pg.Surface((screenW, screenH))
            overlay.set_alpha(200)
            overlay.fill("0x000000")
            self.screen.blit(overlay, (0, 0))

        if self.player.sprite.jumped == True:
            self.player.sprite.airtime += 1 / 60 

        if self.airtime != 0.0:
            if self.airtime > 0.76 and self.player.sprite.deathProb < 1:
                self.player.sprite.deathProb += (self.airtime - 0.8) / 3
                self.playerStrain.play()
                if random() < self.player.sprite.deathProb and random() < self.player.sprite.deathProb and random() < self.player.sprite.deathProb:
                    self.createMenu(self.currentLvl, 0)
                    self.playerBreak.play()
            else:
                self.player.deathProb = 1
                self.groundLand.play()            
     
        if self.timerStart:
            self.ui.showStrainBar(100 - int(self.player.sprite.deathProb * 100))   
            self.timer.run()

class Timer:
    def __init__(self, screen):
        self.runtime = 0.0

        # setup
        self.screen = screen
        self.timerDisplay = font.render(str("{:.2f}".format(self.runtime)), True, "White")
        self.timerRect = self.timerDisplay.get_rect(topleft = (64, 32))

    def run(self):
        self.timerDisplay = font.render(str("{:.2f}".format(self.runtime)), True, "White")
        self.screen.blit(self.timerDisplay, self.timerRect)
        self.runtime += 1 / 60

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.strainBar = pg.image.load("../graphics/ui/strainBar.png").convert_alpha()
        self.strainBarRect = self.strainBar.get_rect(topright = (264, 64))

    def showStrainBar(self, coverNum):
        self.screen.blit(self.strainBar, self.strainBarRect)
        self.cover = pg.Surface((2, 4))
        for i in range(coverNum):
            self.screen.blit(self.cover, (258 - i * 2, 70))

# a sprite group to which all sprites on the screen are added, has the functionality to shift / scroll the screen
class ScrollableSprites(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pg.display.get_surface()

        # cam box
        camL = camBorders["left"]
        camT = camBorders["top"]
        camW = self.screen.get_width() - (camL + camBorders["right"])
        camH = self.screen.get_height() - (camT + camBorders["bottom"])
        
        self.camRect = pg.Rect(camL, camT, camW, camH)

    def customDraw(self, player):

        # get cam pos
        if player.sprite.rect.left < self.camRect.left:
            self.camRect.left = player.sprite.rect.left
        if player.sprite.rect.right > self.camRect.right:
            self.camRect.right = player.sprite.rect.right
        if player.sprite.rect.top < self.camRect.top:
            self.camRect.top = player.sprite.rect.top
        if player.sprite.rect.bottom > self.camRect.bottom:
            self.camRect.bottom = player.sprite.rect.bottom

        # cam offset
        self.offset = pg.math.Vector2(self.camRect.left - camBorders["left"], self.camRect.top - camBorders["top"])

        for sprite in self.sprites():
            offsetPos = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image, offsetPos)

# particle class that can blit jumping and landing particles on the screen at the players location
class ParticleEffect(pg.sprite.Sprite):
    def __init__(self, pos, type, onGrass):
        super().__init__()

        # animation
        self.frameIndex = 0
        self.animationSpeed = 0.5

        if type == "jump" and onGrass:
            self.frames = importFrames("../graphics/player/particles/jump/grass")
        elif type == "jump":
            self.frames = importFrames("../graphics/player/particles/jump/default")

        if type == "land" and onGrass:
            self.frames = importFrames("../graphics/player/particles/land/grass")
        elif type == "land":
            self.frames = importFrames("../graphics/player/particles/land/default")

        self.image = self.frames[self.frameIndex]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frameIndex += self.animationSpeed

        if self.frameIndex >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frameIndex)]

    def update(self):
        self.animate()