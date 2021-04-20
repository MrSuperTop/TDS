from math import cos, radians, sin

import pygame
from groups import bullets
from pygame.math import Vector2

from sprites.collider import Collider
from sprites.entity import Entity

class Bullet(Entity):
  def __init__(
    self,
    camera: object,
    sizeScaler: float,
    imgPath: str,
    damage: int = 100,
    playerRect: pygame.Rect = None
  ) -> None:
    super().__init__(camera, True, playerRect.center, sizeScaler=sizeScaler, imgPath=imgPath, collider=Collider())

    self.damage = damage
    self.speed = 20
    # self.rect = self.image.get_rect(center=playerRect.center)

    # self.rotateCenter(angle, True)
    angle = -self.lookAtMouse(-90)

    # self.pos = Vector2(playerRect.center)
    offset = Vector2(25, -45).rotate(angle)
    # Use the offset to change the starting position.
    self.pos = Vector2(playerRect.center) + offset
    self.velocity = Vector2([-self.speed] * 2)
    self.velocity.rotate_ip(angle + 35)

  def update(self):
    self.pos += self.velocity
    self.rect.center = self.pos
    self.draw()
