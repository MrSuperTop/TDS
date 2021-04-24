import pygame
from pygame.constants import MOUSEWHEEL

import config
from config import windowCenter

from camera import Camera
from config import window
from groups import bullets, texts
from sprites.game_sprite import GameSprite
from sprites.collider import Collider
from sprites.entity import Entity, collidingObjects
from sprites.player import Player
from ui.button import Button, OnClick
from ui.text import Text

pygame.init()

# ? Variables
# * Pygame
clock = pygame.time.Clock()

# * Other
run = True
gameState = 'menu'

# * Camera stuff
camera = Camera(window)

# ? Game sprites
# * UI
ammoText = Text(camera, (25, 25), '', 32, (0, 0, 0), False, 'Arial')

playButton = Button(camera, (windowCenter[0], windowCenter[1] + 100), (150, 75), 'Играть', 32, (255, 255, 255), True, (41, 121, 255))
controlsButton = Button(camera, (windowCenter[0], windowCenter[1] + 15), (250, 75), 'Управление', 32, (255, 255, 255), True, (41, 121, 255))
startText = Text(camera, (windowCenter[0], windowCenter[1] - 200), config.startText, 48, (0, 0, 0), False, 'Arial')

# * Contols
controlsImage = GameSprite(camera, imgPath='controls')
controlsImage.rect.center = windowCenter

# * In-game
player = Player(camera, True, (0, 0), .6, 'knife/idle/survivor-idle_knife_0', 5, Collider((30, 20), (60, 75)), 100, ammoText)
wall = Entity(camera, False, (200, 200), 1, 'walls', Collider((0, 0)))

# ? Events
# * Event handlers
def onClickPlay():
  global gameState
  gameState = 'game'

def onClickControls():
  global gameState
  gameState = 'controls'

playButton.addEvent(OnClick(onClickPlay))
controlsButton.addEvent(OnClick(onClickControls))

# * Adding a player to the camera so will be able to make proper
# * object shift based on the player's movements

camera.addPlayer(player)

def start():
  global run

  # ? Game loop
  while run:
    # print(gameState)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
    window.fill(config.colors['white'])

    if gameState == 'controls':
      controlsImage.draw()

    if gameState == 'menu':
      playButton.update()
      controlsButton.update()
      startText.update()

    if gameState == 'game':
      saveEvent = None

      # * Checking if the user has presse Exit button
      for event in pygame.event.get():
        if event.type == MOUSEWHEEL:
          saveEvent = event

      collidingObjects.update()
      bullets.update()
      player.update(saveEvent)
      camera.scroll()

    pygame.display.flip()
    clock.tick(config.FPS)

  pygame.quit()

if __name__ == '__main__':
  start()
