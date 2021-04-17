import pygame

import config as cfg
from config import window

from sprites.collider import Collider
from sprites.entity import Entity, collidingObjects
from sprites.player import Player

pygame.init()

# ? Variables
# * Pygame
clock = pygame.time.Clock()

# * Other
run = True

# * Game sprites
player = Player((300, 300), .6, './knife/idle/survivor-idle_knife_0.png', 5, Collider((30, 20), (60, 75)), 100)
wall = Entity((200, 200), 1, 'walls.png', Collider((0, 0)))

# ? Game loop
while run:
  window.fill(cfg.colors['white'])

  # * Checking if the user has presse Exit button
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  collidingObjects.update(window)
  player.update(window)

  pygame.display.flip()
  clock.tick(cfg.FPS)

pygame.quit()
