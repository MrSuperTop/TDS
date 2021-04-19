from typing import Union

import pygame

from config import window

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


class GameSprite(pygame.sprite.Sprite):
  def __init__(
    self,
    camera: object,
    # TODO: Can add an ability too pass only one valuem then x = y = value
    coords: Union[tuple[float, float], list[float, float]] = (0, 0),
    sizeScaler: float = 1,
    imgPath: str = '',
  ) -> None:
    super().__init__()

    # * Adding ./images/ to the path to be able to pass a shorter path
    imgPath = './images/' + imgPath + '.png'

    tempImage = pygame.image.load(imgPath).convert_alpha()
    self.image = pygame.transform.scale(
      tempImage,
      getSize(tempImage, sizeScaler)
    )

    # self.imageScale = sizeScaler
    self.originalImage = self.image
    self.imageScale = sizeScaler

    self.mask = pygame.mask.from_surface(self.image)
    self.rect = self.image.get_rect()
    self.rect.x, self.rect.y = coords

    # * Setting up a camera
    if camera is not None:
      self.surface = camera.surface
      self.camera = camera
    else:
      self.camera = None
      self.surface = window

  def draw(self) -> None:
    """
    draw Draws prite on a next frame, has to be called before display.update()
    """

    self.surface.blit(self.image, self.rect.topleft)
      # surface.blit(self.image, (self.rect.x - camera.offset.x, self.rect.y - camera.offset.y))

  update = draw

  def rotateCenter(self, angle: int = 0) -> None:
    """
    rotateCenter Will rotate a sprite around center by a given angle (clockwise)

    Args:
        angle (int): An angle to rotate by
    """

    oldImage = self.image
    self.image = pygame.transform.rotate(self.originalImage, angle)
    self.rect = self.image.get_rect(center=oldImage.get_rect(topleft=self.rect.topleft).center)

  # * Making rect.x and y easier to access
  @property
  def x(self):
    return self.rect.x

  @property
  def y(self):
    return self.rect.y

  # TODO: If will change posiotion using self.rect.x = expression and setters
