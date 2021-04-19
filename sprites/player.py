from math import atan2, degrees, sqrt
from typing import Union

import pygame
from config import windowSize
from pygame.constants import (K_1, K_3, K_DOWN, K_LEFT, K_RIGHT, K_UP, K_a,
                              K_d, K_s, K_w)
from pygame.math import Vector2

from sprites.collider import Collider
from sprites.entity import Entity, collidingObjects


class Player(Entity):
  def __init__(
    self,
    camera: object,
    coords: Union[tuple[float, float], list[float, float]] = (0, 0),
    sizeScaler: float = 1,
    imgPath: str = '',
    # TODO: Add an ability to set vertical and horizontal speeds
    speed: int = 5,
    collider: Collider = None,
    health: int = 100,
  ) -> None:
    super().__init__(camera, coords, sizeScaler, imgPath, collider, health)

    collidingObjects.remove(self)
    self.rect.topleft = (windowSize[0] / 2 - self.rect.center[0], windowSize[1] / 2 - self.rect.center[1])

    self.speed = speed
    # TODO: If needed implament this in the GameSprite class
    self.staticPosition = Vector2(self.rect.topleft)

    # * Saves sprite speed for the next frame
    self.velocity = pygame.math.Vector2(0, 0)

    # * Weapons
    self.weaponName = 'knife'
    self.weaponsList = []

    # * Loading animations
    self._animation = 'knife_idle' # ~ animation name
    self.loadAnimation('knife/idle', 'knife_idle', 20)
    self.loadAnimation('knife/move', 'knife_move', 20, 9)
    self.loadAnimation('rifle/idle', 'rifle_idle', 20)
    self.loadAnimation('rifle/move', 'rifle_move', 10)

  def nextFrame(self):
    if self.velocity == (0, 0):
      self.animation = f'{self.weaponName}_idle'
    else:
      self.animation = f'{self.weaponName}_move'

    super().nextFrame()

  def lookAtMouse(self):
    """
    lookAtMouse Will rotate a player's sprite and rect to make it look
    at the mouse
    """

    mouseX, mouseY = pygame.mouse.get_pos()
    relativeX, relativeY = mouseX - (self.x + self.collider.centerx), mouseY - (self.y + self.collider.centery)
    angle = degrees(-atan2(relativeY, relativeX))

    self.rotateCenter(angle + 5)

  def move(self):
    self.velocity.xy = 0, 0
    keys = pygame.key.get_pressed()
    pressed = {
      'left': keys[K_LEFT] or keys[K_a],
      'right': keys[K_RIGHT] or keys[K_d],
      'up':  keys[K_UP] or keys[K_w],
      'down': keys[K_DOWN] or keys[K_s]
    }

    # * Number of pressed keys for this frame
    pressedKeys = len([key[1] for key in pressed.items() if key[1]])

    # * 1 diretion movements
    if pressedKeys == 1:
      if pressed['left']:
        self.velocity.x = -self.speed
      elif pressed['right']:
        self.velocity.x = self.speed

      if pressed['up']:
        self.velocity.y = -self.speed
      elif pressed['down']:
        self.velocity.y = self.speed

    # * Diagonal movements
    if pressedKeys >= 2:
      diagonalSpeed = sqrt(self.speed ** 2 + self.speed ** 2) * 2 / 3
      if pressed['left'] and pressed['up']:
        self.velocity.xy = -diagonalSpeed, -diagonalSpeed
      if pressed['left'] and pressed['down']:
        self.velocity.xy = -diagonalSpeed, diagonalSpeed

      if pressed['right'] and pressed['up']:
        self.velocity.xy = diagonalSpeed, -diagonalSpeed
      if pressed['right'] and pressed['down']:
        self.velocity.xy = diagonalSpeed, diagonalSpeed

  def weaponChange(self):
    keys = pygame.key.get_pressed()
    pressed = {
      'main': keys[K_1],
      'secondary': keys[K_3],
    }

    if pressed['main']:
      self.weaponName = 'rifle'
    if pressed['secondary']:
      self.weaponName = 'knife'

  def update(self, surface: pygame.Surface) -> None:
    """
    update Will move a player and call all the needed methods
    """

    if self.dead:
      return

    self.move()
    self.weaponChange()

    # * Cheking collisions and moving player based on corrected values
    self.checkCollisions()
    self.staticPosition += self.velocity

    self.nextFrame()
    self.lookAtMouse()

    self.draw()
