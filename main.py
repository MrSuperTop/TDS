import pygame

import config as cfg
from config import window

from sprites.collider import Collider
from sprites.entity import Entity, collidingObjects
from sprites.player import Player
from camera import Camera

pygame.init()

# ? Variables
# * Pygame
clock = pygame.time.Clock()

# * Other
run = True

# * Camera stuff
camera = Camera(window)

# * Game sprites
player = Player(None, (0, 0), .6, 'knife/idle/survivor-idle_knife_0', 5, Collider((30, 20), (60, 75)), 100)
wall = Entity(camera, (200, 200), 1, 'walls', Collider((0, 0)))

# * Adding a player to the camera so will be able to make proper
# * object shift based on the player's movements

camera.addPlayer(player)


# ? Game loop
while run:
  window.fill(cfg.colors['white'])

  # * Checking if the user has presse Exit button
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  collidingObjects.update()
  player.update(window)
  camera.scroll()

  pygame.display.flip()
  clock.tick(cfg.FPS)

pygame.quit()
