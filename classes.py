# ? Import
from typing import Tuple, Union, overload
from math import atan2, degrees, sqrt

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
# * Colliders
# TODO: Make a collider really useful not just to replace it with get_bounding_rect in rotateCenter
class Collider(pygame.Rect):
  def __init__(
    self,
    relativeCoords: Union[tuple[float, float], list[float, float]] = (0, 0),
    size:  Union[tuple[float, float], list[float, float]] = (0, 0)
  ) -> None:
    super().__init__(relativeCoords, size)


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
    self.image = pygame.transform.scale(
      tempImage,
      getSize(tempImage, sizeScaler)
    )

    self.originalImage = self.image

    self.mask = pygame.mask.from_surface(self.image)
    self.rect = self.image.get_bounding_rect()
    self.rect.x, self.rect.y = coords

  def draw(self) -> None:
    """
    draw Draws prite on a next frame, has to be called before display.update()
    """

    window.blit(self.image, self.rect.topleft)

  def rotateCenter(self, angle: int = 0) -> None:
    """
    rotateCenter Will rotate a sprite around center by a given angle (clockwise)

    Args:
        angle (int): An angle to rotate by
    """

    image = self.image
    topLeft = self.rect.topleft

    self.image = pygame.transform.rotate(self.originalImage, angle)
    self.rect = self.image.get_rect(center=image.get_rect(topleft=topLeft).center)

    # return image, new_rect

    # surf.blit(rotated_image, new_rect.topleft)

  # def drawWithoutBg(self):
  #   tempRect = self.image.get_bounding_rect()
  #   tempRect.x = self.x + 25
  #   tempRect.y = self.y + 25

    # x = int(tempRect.width/2)
    # y = int(tempRect.height/2)

    # window.blit(self.image, (tempRect.x, tempRect.y))

  # * Making rect.x and y easier to access
  @property
  def x(self):
    return self.rect.x

  @property
  def y(self):
    return self.rect.y

  # TODO: If will change posiotion using self.rect.x = expression and setters

  update = draw


class Entity(GameSprite):
  dead = False

  def __init__(
    self,
    coords: Union[tuple[float, float], list[float, float]] = (0, 0),
    sizeScaler: float = 1,
    imgPath: str = '',
    collider: Collider = None,
    health: int = 100,
    drawCollider: bool = cfg.drawColliderBorders
  ) -> None:
    super().__init__(coords, sizeScaler, imgPath)

    self.hp = health
    self.collider = collider
    self.drawCollider = drawCollider

    # * Adding object to a group, so we will be able to detect collisioins
    if collider is not None:
      collider = Collider()
      collidingObjects.add(self)

      if collider.width == 0:
        collider.width = self.image.get_width()
      if collider.height == 0:
        collider.height = self.image.get_height()

      self.collider = collider

  def die(self):
    """
    die Sets dead attr to True and prite won't be rendered anymore
    """

    self.dead = True

  def draw(self):
    if self.drawCollider:
      pygame.draw.rect(window, (0, 255, 0), self.rect, 4)
      pygame.draw.rect(window, (255, 0, 0), self.collider.move(self.rect.topleft), 4)
    super().draw()

  update = draw

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

  def rotateCenter(self, angle: int = 0, spinCollider: bool = True) -> None:
    """
    rotateCenter Will rotate a sprite around center by a given angle (clockwise)
    spins the collider is spinCollider set to True

    Args:
        angle (int): An angle to rotate by
        spinCollider(bool): Set weather you want to spin the collide with the
        image
    """

    super().rotateCenter(angle)
    if spinCollider:
      self.collider = self.image.get_bounding_rect()

  def checkCollisions(self) -> None:
    """
    checkCollisions Checks the collision with other object which are in the
    colliding objects group and changes the self.velocity values
    """

    # * Checking collisions for each collided object
    collisionList = []

    # * Creating a class object and setting its rect attribute to collider
    # * so it will be really to use pygame fucntion to check collisions, because
    # * it needs a sprite instead of a simple rect for some reason

    # TODO: Make it more pythonic and avoiding pylint errors somehow
    playerCollider = lambda: None
    playerCollider.rect = self.collider.move(self.rect.topleft)

    for sprite in collidingObjects:
      colliderObject = lambda: None
      colliderObject.rect = sprite.collider.move(sprite.rect.topleft)

      if pygame.sprite.collide_rect(playerCollider, colliderObject):
        collisionList.append(sprite)

    for gameObject in collisionList:
      objectCol = gameObject.collider.move(gameObject.rect.topleft)
      collider = self.collider.move(self.rect.topleft)

      # TODO: Make it's impossible to move through colliders by spinning and pressing a movement button
      # * Y collsions
      if self.velocity.y > 0 and \
          objectCol.top <= collider.bottom + self.speed < objectCol.bottom:
        self.velocity.y = 0
      if self.velocity.y < 0 and \
          objectCol.bottom >= collider.top - self.speed > objectCol.top:
        self.velocity.y = 0

      # * X collisions
      if self.velocity.x > 0 and \
          objectCol.left <= collider.right - self.speed < objectCol.right:
        self.velocity.x = 0
      if self.velocity.x < 0 and \
          objectCol.right >= collider.left - self.speed > objectCol.left:
        self.velocity.x = 0


class Player(Entity):
  def __init__(
    self,
    coords: Union[tuple[float, float], list[float, float]] = (0, 0),
    sizeScaler: float = 1,
    imgPath: str = '',
    # TODO: Add an ability to set vertical and horizontal speeds
    speed: Union[Tuple, int] = 5,
    collider: Collider = None,
    health: int = 100
  ) -> None:
    super().__init__(coords, sizeScaler, imgPath, collider, health)

    collidingObjects.remove(self)

    self.rect = self.image.get_bounding_rect()
    self.speed = speed

    # * Saves sprite speed for the next frame
    self.velocity = pygame.math.Vector2(0, 0)

  def lookAtMouse(self):
    """
    lookAtMouse Will rotate a player's sprite and rect to make it look
    at the mouse
    """

    mouseX, mouseY = pygame.mouse.get_pos()
    relativeX, relativeY = mouseX - (self.x + self.collider.x), mouseY - (self.y + self.collider.y)
    angle = degrees(-atan2(relativeY, relativeX))

    self.rotateCenter(angle - 15)

  def update(self) -> None:
    """
    update Will move a player and call all the needed methods
    """

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

    # * Cheking collisions and moving player based on corrected values
    self.checkCollisions()
    self.rect.move_ip(*self.velocity)
    self.lookAtMouse()

    self.draw()
