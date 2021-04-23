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
    self.speed = config.bulletSpeed
    self.existsFor = 0
    self.killAfter = killAfter

    self.lookAtMouse(-90)
    angle = -player.angle + 90
    # self.rotateCenter(angle)

    self.startPos = Vector2(player.pivot.center)
    self.rect.center = self.startPos
    self.velocity = Vector2([-self.speed] * 2)
    self.velocity.rotate_ip(angle + 45)

  def update(self):
    self.startPos += self.velocity
    self.rect.center = self.startPos

    self.existsFor += 1
    if self.existsFor > self.killAfter * config.FPS:
      self.kill()

    self.draw()
