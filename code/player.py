# a player sprite, player inputs and correct animations are handled here, movement and and particles are partially handled in lvl.py

import pygame as pg
from helpers import importFrames

class Player(pg.sprite.Sprite):
    def __init__(self, pos, screen, createJumpParticles):
        super().__init__()
        self.importAnimations()

        self.deathProb = 0.0
        self.airtime = 0.0
        self.jumped = False

        # animation related
        self.frameIndex = 0
        self.animationSpeed = 0.20
        self.status = "idle"
        self.facingRight = True
        self.image = self.animations["idle"][0]
        self.rect = self.image.get_rect(topleft = pos)

        # the method to create jump particles are passed to the player through the Level class in lvl.py
        self.createJumpParticles = createJumpParticles
        self.screen = screen

        # player movement variables, used in the Level class
        self.direction = pg.math.Vector2(0, 0)
        self.speed = 7
        self.jumpSpeed = -18
        self.grav = 0.8

        # player collision, needed to correctly handle collisions, used in the level class
        self.onGround = False
        self.onCeiling = False
        self.onLeft = False
        self.onRight = False

        self.startTime = pg.time.get_ticks()
        self.allowInput = False
        self.timerLength = 5000

    def importAnimations(self):
        path = "../graphics/player/default/"
        self.animations = {"idle": [], "run": [], "jump": [], "fall": []}

        for animation in self.animations.keys():
            animationPath = path + animation
            self.animations[animation] = importFrames(animationPath)

    def animate(self):
        animation = self.animations[self.status]

        self.frameIndex += self.animationSpeed
        if self.status == "jump":
            if self.frameIndex >= len(animation):
                self.frameIndex = len(animation) - 1
        else:
            if self.frameIndex >= len(animation):   
                self.frameIndex = 0

        # flip the image depening on the direction the player is facing
        image = animation[int(self.frameIndex)]
        if self.facingRight:
            self.image = image
        else:
            flippedImage = pg.transform.flip(image, True, False)
            self.image = flippedImage

        # set the rectangle

        # player on ground
        if self.onGround and self.onRight:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.onGround and self.onLeft:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.onGround:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

        # player touching ceiling
        elif self.onCeiling and self.onRight:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.onCeiling and self.onLeft:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.onCeiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def inputTimer(self):
        if not self.allowInput:
            currentTime = pg.time.get_ticks()
            if currentTime - self.startTime >= self.timerLength:
                self.allowInput = True

    def getInput(self):
        inputs = pg.key.get_pressed()

        if self.allowInput:
            if inputs[pg.K_RIGHT]:
                self.direction.x = 1
                self.facingRight = True
            elif inputs[pg.K_LEFT]:
                self.direction.x = -1
                self.facingRight = False
            else:
                self.direction.x = 0

            if inputs[pg.K_SPACE] and self.onGround:
                self.jumped = True
                self.jump()
                self.createJumpParticles(self.rect.midbottom)

    def getStatus(self):
        if self.direction.y < 0:
            self.status = "jump"

        elif self.direction.y > 1:
            self.status = "fall"

        else:
            if self.direction.x != 0:
                self.status = "run"
            else:
                self.status = "idle"

    def applyGrav(self):
        self.direction.y += self.grav
        self.rect.y += self.direction.y

    def jump(self):
        self.frameIndex = 0
        self.direction.y = self.jumpSpeed

    def update(self):
        self.getInput()
        self.getStatus()
        self.animate()