from time import time

import pygame
from pygame.constants import K_ESCAPE, KEYDOWN, MOUSEWHEEL

import config
from camera import Camera
from config import window, windowCenter
from groups import bullets, texts
from sprites.collider import Collider
from sprites.entity import Entity, collidingObjects
from sprites.game_sprite import GameSprite
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
previousState = 'menu'
lastChange = 0

# * Camera stuff
camera = Camera(window)

# ? Game sprites
# * UI
# & Game
ammoText = Text(camera, 'left', (25, 25), '', 32, (0, 0, 0), False, 'Arial')

# & Start screen
playButton = Button(camera, (windowCenter[0], windowCenter[1] + 100), (150, 75), 'Играть', 32)
controlsButton = Button(camera, (windowCenter[0], windowCenter[1] + 15), (250, 75), 'Управление', 32)
quitButton = Button(camera, (windowCenter[0], windowCenter[1] + 185), (150, 75), 'Выйти', 32, color=(213, 0, 0))
startText = Text(camera, 'center', (windowCenter[0], windowCenter[1] - 200), config.startText, 48, (0, 0, 0), False, 'Arial')

# & Controls
controlsImage = GameSprite(camera, imgPath='controls')
controlsImage.rect.center = windowCenter
exitControlsButton = Button(camera, (85, 35), (150, 50), 'Назад', 32)

# & Pause
pauseText = Text(camera, 'center', (windowCenter[0], 150), 'Пауза...', 48, (0, 0, 0), True, 'Arial')
backToGameButton = Button(camera, (windowCenter[0], windowCenter[1] + 100), (250, 75), 'Назад к игре', 32)
toMenuButton = Button(camera, (windowCenter[0], windowCenter[1] - 70), (200, 75), 'В меню', 32)

# * In-game
player = Player(camera, True, (0, 0), .6, 'knife/idle/survivor-idle_knife_0', 5, Collider((30, 20), (60, 75)), 100, ammoText)
wall = Entity(camera, False, (200, 200), 1, 'walls', Collider((0, 0)))

# ? Button events setup
# * Event handlers
def goTo(newState, prevState):
  print(prevState, newState)
  global gameState, previousState, lastChange

  lastChange = time()
  gameState = newState
  previousState = prevState

def goBack(_ = None):
  print('Going back')
  global gameState, previousState, lastChange

  lastChange = time()
  gameStateCopy = gameState
  gameState = previousState
  previousState = gameStateCopy

def exit(_ = None):
  global run
  run = False

playButton.addEvent(OnClick(lambda x: goTo('game', x)))
controlsButton.addEvent(OnClick(lambda x: goTo('controls', x)))
exitControlsButton.addEvent(OnClick(goBack))
backToGameButton.addEvent(OnClick(lambda x: goTo('game', x)))
toMenuButton.addEvent(OnClick(lambda x: goTo('menu', x)))
quitButton.addEvent(OnClick(exit))

# * Adding a player to the camera so will be able to make proper
# * object shift based on the player's movements

camera.addPlayer(player)

def start():
  global gameState

  # ? Game loop
  while run:
    eventsList = pygame.event.get()
    # print(gameState)
    for event in eventsList:
      if event.type == pygame.QUIT:
        exit()

      canGoBack = gameState not in ['game', 'pause']
      if canGoBack and event.type == KEYDOWN and event.key == K_ESCAPE:
        goBack()
      # if gameState == 'game' and event.type == KEYDOWN and event.key == K_ESCAPE:

    window.fill(config.colors['white'])

    if gameState == 'controls':
      controlsImage.draw()
      exitControlsButton.update(gameState)

    elif gameState == 'menu':
      playButton.update(gameState)
      controlsButton.update(gameState)
      quitButton.update(gameState)
      startText.update()

    elif gameState == 'game':
      saveEvent = None

      # * Checking if the user has presse Exit button
      for event in eventsList:
        if event.type == MOUSEWHEEL:
          saveEvent = event
        if event.type == KEYDOWN and event.key == K_ESCAPE:
          goTo('pause', 'game')

      collidingObjects.update()
      bullets.update()
      player.update(saveEvent)
      camera.scroll()

    elif gameState == 'pause':
      for event in eventsList:
        if event.type == KEYDOWN and event.key == K_ESCAPE and time() - lastChange >= 0.1:
          gameState = 'game'

      controlsButton.update(gameState)
      backToGameButton.update(gameState)
      quitButton.update(gameState)
      toMenuButton.update(gameState)
      pauseText.update()

    pygame.display.flip()
    clock.tick(config.FPS)

  pygame.quit()

if __name__ == '__main__':
  start()
