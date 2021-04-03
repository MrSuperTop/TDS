# ? Import
from typing import Tuple, Union

import imagesize
import pygame
from pygame.constants import K_LEFT, K_RIGHT, K_a, K_d, K_UP, K_DOWN, K_w, K_s

import config as cfg


# ? Variables
window = pygame.display.set_mode([*cfg.windowSize])

# * Groups
collidingObjects = pygame.sprite.Group()

# ? Function
def getSize(imagePath: str, multiplier: Union[int, float]) -> tuple[int, int]:
  """
  getSize Will return a new size of an image getting current and multipling

  Args:
      imagePath (str): Path to an image
      multiplier (int, float): Size of an image will by multiplied by it
  """

  width, height = imagesize.get(imagePath)
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
    self.image = pygame.transform.scale(tempImage, getSize(imgPath, sizeScaler))

    self.mask = pygame.mask.from_surface(self.image)
    self.rect = self.image.get_rect()
    self.rect.x, self.rect.y = coords

  def update(self) -> None:
    """
    update Draws prite on a next frame, has to be called before display.update()
    """

    window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
  def __init__(
    self,
    coords: Union[tuple[float, float], list[float, float]] = (0, 0),
    sizeScaler: float = 1,
    imgPath: str = '',
    # TODO: Add an ability to set vertical and horizontal speeds
    speed: Union[Tuple, int] = 5
  ) -> None:
    super().__init__(coords, sizeScaler, imgPath)

    self.speed = speed

    # * Saves sprite speed for the next frame
    self.velocity = pygame.math.Vector2(0, 0)

  def update(self) -> None:
    # * Moving player if keys are pressed
    self.velocity.xy = 0, 0

    keys = pygame.key.get_pressed()
    if keys[K_LEFT] or keys[K_a]:
      self.velocity.x = -self.speed
    elif keys[K_RIGHT] or keys[K_d]:
      self.velocity.x = self.speed

    if keys[K_UP] or keys[K_w]:
      self.velocity.y = -self.speed
    elif keys[K_DOWN] or keys[K_s]:
      self.velocity.y = self.speed

    # * Checking collisions
    collisionList = pygame.sprite.spritecollide(
      self,
      collidingObjects,
      False,
      pygame.sprite.collide_mask
    )

    print(self.velocity)

    for gameObject in collisionList:
      # * Getting absolute coordinates for our collision
      collisionPoint = pygame.sprite.collide_mask(self, gameObject)
      collision = pygame.math.Vector2(
        self.rect.x + collisionPoint[0],
        self.rect.y + collisionPoint[1]
      )

      # TODO: Make proper masks collision
      # # * Top collision
      # if (
      #   self.velocity.y > 0 and
      #   gameObject.rect.bottom - 10 > collision.y >= gameObject.rect.top
      # ):
      #   print('set ZERO')
      #   self.velocity.y = 0
      # # elif not self.acceleration.y > 0:
      # #   self.acceleration.y = -1

      # # * Bottom collision
      # if (
      #   self.velocity.y < 0 and
      #   gameObject.rect.top + 10 < collision.y <= gameObject.rect.bottom
      # ):
      #   print('set ZERO')
      #   self.velocity.y = 0
      # # elif not self.acceleration.y:
      # #   self.acceleration.y = 1

      # # * Left collision
      # # if (
      # #   self.velocity.x > 0 and
      # #   gameObject.rect.right - 5 > collision.y >= gameObject.rect.left
      # # ):
      # #   print('set XX')
      # #   self.velocity.x = 0
      # # elif not self.acceleration.y > 0:
      # #   self.acceleration.y = -1
  
    self.rect.topleft += self.velocity

    super().update()


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
    else:
      notCollidingObjects.add(self)
