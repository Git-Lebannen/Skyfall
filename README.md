# Skyfall
#### Video Demo:  https://youtu.be/cW78YobUDjo 
#### Description:
  My final project is a pixel-artsy platformer, which I have named Skyfall.
  I implemented it using the pygame library, which I learned about online.
  The game is made for one player and includes a level selection, 6 different levels, animations, sound, different causes of death, a win condition and a timer to time the player's completion time.

##### Folder structure:
  - project/
    - Skyfall/
      - audio/
        - sfx/
          - *sound effects* (o.gg file format)
        - tracks/
          - *tracks* (.ogg file format)
        - credits.txt (credits for audio tracks)
      - code/
        - helpers.py (helper functions)
        - lvl.py (runs a level)
        - lvlData.py (saves paths to the .csv files in "../levels/*folders with each level's .csv files*")
        - main.py (plays tracks, switches between level and level selection)
        - menu.py (runs an instance of the level selection)
        - player.py (player class)
        - settings.py (small file saving some important game variables)
        - tiles.py (different kinds of tile classes used to render the graphics)
      - graphics/
        - *level graphics*
        - *menu graphics*
        - *player graphics*
        - screen_icon/
          - screenIcon.png (icon for the pygame display)
        - ui
          - strainBar.png
          - *font.ttf*
      - levels/
        - *folders with each level's .csv files*
        - *Tiled projects folder*
        - *tileset folder for Tile projects*
    - README.md

##### Graphics:
  The graphics are based on 64 by 64 pixel tiles (the trees are an exception). The layouts for graphic tiles in the levels are saved in .csv files, for ease of level creation these were exported from "Tiled" projects, a tile based graphics editor ([install](https://www.mapeditor.org/download.html)). I edited the animations and formatted everything accordinlgy (using [paint.net](https://www.getpaint.net)), but most of the original images are from the web.

##### Level selection:
  The level selection scrolls if need be to display levels that would otherwise not be visible, an animated arrow marks the selected level. When in the level selection, the game will loop background music and animate the background image. The unlocked levels have animated panels with text on them, indicating the level number and the players best time.
  To enter a level, the player has to press the **return**/**enter** key. To navigate between unlocked levels, the **up** and **down** arrows are used.

##### Level:
  The movement commands are jump (**space**), left and right (**left** and **right** arrows).
  When starting a level via the level selection, the level first loads the graphics layout and player and then displays them on the screen. 
  In the beginning of each level, the player's inputs are blocked for the game to load properly. When the inputs are unlocked, the timer and strainBar will appear in the top left of the screen.
  Strain is built up by making (too) big jumps, it's max value is 1.0. The game rolls three random values and checks if all of them are smaller than the player's current strain. If they are all smaller, then the player 'snaps' (much like a stick), and the level is failed.

  The level can be failed by:
  - the player hitting a barrier that restricts his roaming and stops him from falling infinitely
  - taking longer to complete the level than allowed (60 seconds)
  - dying due to strain
  The level is only cleared once the player collides with the floating grey mask.

  When the level is cleared and the time taken is smaller than the previous best time, the time is updated on the selection panel.

##### Story:
  When making the levels in the editor, I wanted to create a bit of a story. A groot like being falls from it's floating tree island one night, following a grey mask. He wakes up on the ground, finding only one way to go, which is down. If you pay attenion, you will see that each level from then on begins where the previous level left off. 
  The strain meter was inspired by wood snapping, I thought it would be more fun than a regular health bar.

##### Audio:
  All audio tracks and sound effects come from https://uppbeat.io.
  I apologize in advance if the sfx aren't great, I realized myself that depending on the speaker/headphones it can sound better or worse. 

