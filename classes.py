# ? Import
from typing import Tuple, Union
from math import sqrt

import pygame
from pygame.constants import K_LEFT, K_RIGHT, K_a, K_d, K_UP, K_DOWN, K_w, K_s

import config as cfg


# ? Variables
window = pygame.display.set_mode([*cfg.windowSize])

# * Groups
collidingObjects = pygame.sprite.Group()


# ? Function
def getSize(image: object, multiplier: Union[int, float]) -> tuple[int, int]:
  """
  getSize Will return a new size of an image getting current and multipling

  Args:
      imagePath (str): Path to an image
      multiplier (int, float): Size of an image will by multiplied by it
  """

  width, height = image.get_size()
  return int(width * multiplier), int(height * multiplier)


# ? Classes
class GameSprite(pygame.sprite.Sprite):
  def __init__(
    self,
    # TODO: Can add an ability too pass only one valuem then x = y = value
    coords: Union[tuple[float, float], list[float, float]] = (0, 0),
    sizeScaler: float = 1,
    imgPath: str = ''
  ) -> None:

    super().__init__()

    # * Adding ./images/ to the path to be able to pass a shorter path
    imgPath = './images/' + imgPath

    tempImage = pygame.image.load(imgPath).convert_alpha()
    self.image = pygame.transform.scale(tempImage, getSize(tempImage, sizeScaler))

    self.mask = pygame.mask.from_surface(self.image)
    self.rect = self.image.get_rect()
    self.rect.x, self.rect.y = coords

  def draw(self) -> None:
    """
    draw Draws prite on a next frame, has to be called before display.update()
    """

    window.blit(self.image, (self.rect.x, self.rect.y))

  update = draw


class Entity(GameSprite):
  dead = False

  def __init__(
    self,
    coords: Union[tuple[float, float], list[float, float]] = (0, 0),
    sizeScaler: float = 1,
    imgPath: str = '',
    health: int = 100
  ) -> None:
    super().__init__(coords, sizeScaler, imgPath)

    self.hp = health

  def die(self):
    """
    die Sets dead attr to True and prite won't be rendered anymore
    """

    self.dead = True

  @property
  def hp(self):
    return self._hp

  @hp.setter
  def hp(self, value):
    if value <= 0:
      self.die()
      self.kill()  # ~ removes sprite from all groups
    else:
      self._hp = value

  def checkCollisions(self) -> None:
    # * Checking collisions for each collided object
    collisionList = pygame.sprite.spritecollide(
      self,
      collidingObjects,
      False,
      pygame.sprite.collide_mask
    )

    for gameObject in collisionList:
      objectRect = gameObject.rect

      # TODO: Make proper masks collision
      # * Y collsions
      if self.velocity.y > 0 and \
          objectRect.top <= self.rect.bottom + self.speed < objectRect.bottom:
        self.velocity.y = 0
      if self.velocity.y < 0 and \
          objectRect.bottom >= self.rect.top - self.speed > objectRect.top:
        self.velocity.y = 0

      # * X collisions
      if self.velocity.x > 0 and \
          objectRect.left <= self.rect.right - self.speed < objectRect.right:
        self.velocity.x = 0
      if self.velocity.x < 0 and \
          objectRect.right >= self.rect.left - self.speed > objectRect.left:
        self.velocity.x = 0


class Player(Entity):
  def __init__(
    self,
    coords: Union[tuple[float, float], list[float, float]] = (0, 0),
    sizeScaler: float = 1,
    imgPath: str = '',
    # TODO: Add an ability to set vertical and horizontal speeds
    speed: Union[Tuple, int] = 5,
    health: int = 100
  ) -> None:
    super().__init__(coords, sizeScaler, imgPath, health)

    self.rect = self.image.get_bounding_rect()
    self.speed = speed

    # * Saves sprite speed for the next frame
    self.velocity = pygame.math.Vector2(0, 0)

  def update(self) -> None:
    if self.dead:
      return

    # * Moving player in 1 dirrection if keys are pressed
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
      diagonalSpeed = sqrt(self.speed ** 2 + self.speed ** 2) / 2
      if pressed['left'] and pressed['up']:
        self.velocity.xy = -diagonalSpeed, -diagonalSpeed
      if pressed['left'] and pressed['down']:
        self.velocity.xy = -diagonalSpeed, diagonalSpeed

      if pressed['right'] and pressed['up']:
        self.velocity.xy = diagonalSpeed, -diagonalSpeed
      if pressed['right'] and pressed['down']:
        self.velocity.xy = diagonalSpeed, diagonalSpeed

    self.checkCollisions()
    self.rect.move_ip(*self.velocity)

    self.draw()


class MapObject(GameSprite):
  def __init__(
    self,
    coords: Union[tuple[float, float], list[float, float]] = (0, 0),
    sizeScaler: float = 1,
    imgPath: str = '',
    collides: bool = True
  ) -> None:
    super().__init__(coords, sizeScaler, imgPath)

    self.collides = collides

    # * Adding object to a group, so we will be able to detect collisioins
    if collides:
      collidingObjects.add(self)
