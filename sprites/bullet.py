from math import cos, radians, sin

import pygame
from groups import bullets
from pygame.math import Vector2

from sprites.collider import Collider
from sprites.entity import Entity
import config

class Bullet(Entity):
  def __init__(
    self,
    camera: object,
    sizeScaler: float,
    imgPath: str,
    damage: int = 100,
    player: object = None,
    killAfter: int = 1
  ) -> None:
    super().__init__(camera, True, player.pivot.center, sizeScaler=sizeScaler, imgPath=imgPath, collider=Collider())

    self.damage = damage
    self.speed = 5
    self.existsFor = 0
    self.killAfter = killAfter

    angle = -self.lookAtMouse(-90)
  
    self.pos = Vector2(player.pivot.center)
    self.velocity = Vector2([-self.speed] * 2)
    self.velocity.rotate_ip(angle + 45)

  def update(self):
    self.pos += self.velocity
    self.rect.topleft = self.pos
    self.draw()
    self.existsFor += 1

    if self.existsFor > self.killAfter * config.FPS:
      self.kill()
