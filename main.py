# ? Imports
import pygame
from config import colors

import config as cfg
from classes import Player, window, MapObject, collidingObjects

pygame.init()

# ? Variables
# * Pygame
clock = pygame.time.Clock()

# * Other
run = True

# * Game sprites
player = Player((0, 0), .5, 'survivor-idle_knife_0.png', 5, 100)
wall = MapObject((200, 200), 1, 'walls.png', True)

# ? Game loop
while run:
  window.fill(colors['white'])

  # * Checking if the user has presse Exit button
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  collidingObjects.update()
  player.update()

  pygame.display.flip()
  clock.tick(cfg.FPS)

pygame.quit()
