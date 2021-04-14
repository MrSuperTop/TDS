# ? Imports
import pygame
from config import colors

import config as cfg
from classes import Player, window, Entity, collidingObjects, Collider

pygame.init()

# ? Variables
# * Pygame
clock = pygame.time.Clock()

# * Other
run = True

# * Game sprites
player = Player((0, 0), .5, 'survivor-idle_knife_0.png', 5, Collider((30, 20), (60, 75)), 100)
wall = Entity((200, 200), 1, 'walls.png', Collider((0, 0)))

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
