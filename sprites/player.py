from dataclasses import dataclass
from math import sqrt, cos, sin, radians
from time import time
from typing import Union

import config
import pygame
from config import windowSize
from pygame.constants import (BUTTON_WHEELDOWN, BUTTON_WHEELUP, K_1, K_2, K_3,
                              K_DOWN, K_LEFT, K_RIGHT, K_UP, MOUSEWHEEL, K_a,
                              K_d, K_s, K_w)
from pygame.math import Vector2

from sprites.bullet import Bullet
from sprites.collider import Collider
from sprites.entity import Entity, collidingObjects



class ShottingPoint:
  def __init__(self, player, surface, rect, offset):
    self.player = player

    self.surface = surface
    self.rect = rect
    self.startPosition = rect.centerx + offset[0], rect.centery + offset[1]

    self.offset = Vector2(offset)

  @property
  def center(self):
    return self.rect.center

  @center.setter
  def center(self, newValue):
    self.rect.center = newValue

  @property
  def globalRect(self):
    return self.player.rect.move(self.startPosition).move(self.offset)

  def __repr__(self):
    return self.surface

@dataclass
class Weapon:
  name: str
  canShoot: bool
  shottingDelay: int = 0
  toTheEnd: float = 0
  shiftAngle: float = 0
  magCapacity: int = 0
  reloadDuration: int = 0

  def __post_init__(self):
    self.ammo = self.magCapacity

class Player(Entity):
  def __init__(
    self,
    camera: object,
    static: bool,
    coords: Union[tuple[float, float], list[float, float]] = (0, 0),
    sizeScaler: float = 1,
    imgPath: str = '',
    # TODO: Add an ability to set vertical and horizontal speeds
    speed: int = 5,
    collider: Collider = None,
    health: int = 100,
  ) -> None:
    super().__init__(camera, static, coords, sizeScaler, imgPath, collider)

    collidingObjects.remove(self)
    self.rect.topleft = (windowSize[0] / 2 - self.rect.center[0], windowSize[1] / 2 - self.rect.center[1])

    self.speed = speed
    # TODO: If needed implament this in the GameSprite class
    self.staticPosition = Vector2(self.rect.topleft)

    # * Saves sprite speed for the next frame
    self.velocity = pygame.math.Vector2(0, 0)

    # * Weapons change
    self.weaponName = 'knife'
    self.weaponIndex = 2
    self.weaponsList = [
      Weapon('rifle', True, 0.1, 80, -15, 30, 1),
      Weapon('handgun', True, 0.25, 75, -25, 15, .75),
      Weapon('knife', False)
    ]

    framerates = [
      [[10, 0], [20, 0], [20, 0], [20, 0]],
      [[10, 0], [20, 0], [20, 0], [20, 0]],
      [[10, 0], [20, 0]],
    ]

    self.lastChangeTime = 0
    self.lastShot = 0

    # * Loading animations
    self._animation = 'knife_idle'  # ~ Default animation name
    for i, weapon in enumerate(self.weaponsList):
      self.loadAnimation(f'{weapon.name}/idle', *framerates[i][0])
      self.loadAnimation(f'{weapon.name}/move', *framerates[i][1])
      if weapon.canShoot:
        self.loadAnimation(f'{weapon.name}/shoot', *framerates[i][2])
        self.loadAnimation(f'{weapon.name}/reload', *framerates[i][3])


    # self.loadAnimation('knife/idle', 10)
    # self.loadAnimation('knife/move', 20, 9)
    # self.loadAnimation('rifle/idle', 10)
    # self.loadAnimation('rifle/move', 20)
    # self.loadAnimation('rifle/shoot', 20)
    # self.loadAnimation('handgun/idle', 10)
    # self.loadAnimation('handgun/move', 20)
    # self.loadAnimation('handgun/shoot', 20)

    # * Rotation pivot
    pivotSurface = pygame.Surface((15, 15))
    pivotRect = pivotSurface.fill((255, 0, 0))
    self.pivot = ShottingPoint(self, pivotSurface, pivotRect, (0, 0))
    self.pivot.center = self.pivot.globalRect.center

    # * Health
    self.hp = health

    # * Ammo system
    self.reloading = False
    self.reloadStarted = 0

  @property
  def weapon(self):
    return self.weaponsList[self.weaponIndex]

  @property
  def animation(self):
    return self._animation

  @animation.setter
  def animation(self, animationType: str) -> None:
    fullName = f'{self.weapon.name}_{animationType}'
    if fullName != self._animation and not self.animationLock:
      self._animation = fullName
      self.frame = self.startingFrames[fullName]

  def nextFrame(self):
    if self.velocity == (0, 0):
      self.animation = 'idle'
    else:
      self.animation = 'move'

    super().nextFrame()

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

  def weaponChange(self, event):
    if not time() - self.lastChangeTime > config.weaponChangeDelay:
      return
    
    keys = pygame.key.get_pressed()
    pressed = {
      'main': keys[K_1],
      'secondary': keys[K_2],
      'melee': keys[K_3],
    }

    if event is not None:
      if event.y > 0:
        self.weaponIndex -= 1
      elif event.y < 0:
        self.weaponIndex += 1

    if pressed['main']:
      self.weaponIndex = 0
    if pressed['secondary']:
      self.weaponIndex = 1
    if pressed['melee']:
      self.weaponIndex = 2

    if self.weaponIndex >= len(self.weaponsList):
      self.weaponIndex = 0
    elif self.weaponIndex < 0:
      self.weaponIndex = len(self.weaponsList) - 1

    newName = self.weaponsList[self.weaponIndex].name
    if newName != self.weaponName:
      self.lastChangeTime = time()

    self.weaponName = newName

  def reload(self):
    self.reloading = True
    self.reloadStarted = time()
    self.animationLock = False
    self.animation = 'reload'
    self.animationLock = True

  def shoot(self):
    if self.reloading and time() - self.reloadStarted > self.weapon.reloadDuration:
      self.reloading = False
      self.animationLock = False
      self.weapon.ammo = self.weapon.magCapacity

    if self.reloading:
      return

    buttons = pygame.mouse.get_pressed()
    canShootNow = time() - self.lastShot > self.weapon.shottingDelay

    if buttons[0] and canShootNow and self.weapon.ammo > 0:
      Bullet(self.camera, .075, 'bullet', player=self, killAfter=3)
      self.lastShot = time()
      self.animation = 'shoot'
      self.lockedFrames = config.FPS / 20 * 3
      self.weapon.ammo -= 1
    elif self.weapon.ammo <= 0:
      self.reload()


  @property
  def hp(self):
    return self._hp

  @hp.setter
  def hp(self, value):
    if value <= 0:
      self.die()
    else:
      self._hp = value

  def die(self):
    """
    die Sets dead attr to True and prite won't be rendered anymore
    """

    self.kill()
    self.dead = True

  def lookAtMouse(self):
    angle = super().lookAtMouse()
    x, y = self.rect.center
    c = self.weapon.toTheEnd

    radAngle = -radians(angle + self.weapon.shiftAngle)
    self.pivot.center = x + c * cos(radAngle), y + c * sin(radAngle)

  def draw(self):
    super().draw()
    if config.drawColliderBorders:
      self.surface.blit(self.pivot.surface, self.pivot.center)

  def update(self, event) -> None:
    """
    update Will move a player and call all the needed methods
    """

    if self.dead:
      return

    self.move()
    self.weaponChange(event)

    if self.weapon.canShoot:
      self.shoot()

    # * Cheking collisions and moving player based on corrected values
    self.checkCollisions()
    self.staticPosition += self.velocity

    self.nextFrame()
    self.lookAtMouse()

    self.draw()

