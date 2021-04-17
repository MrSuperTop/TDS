from typing import Union

import pygame


# TODO: Make a collider really useful not just to replace it with get_bounding_rect in rotateCenter
class Collider(pygame.Rect):
  """
  Collider Allows to set a sprite area which will be an actual collider.
  Will replace the rect in collisions.
  """

  def __init__(
    self,
    relativeCoords: Union[tuple[float, float], list[float, float]] = (0, 0),
    size:  Union[tuple[float, float], list[float, float]] = (0, 0)
  ) -> None:
    super().__init__(relativeCoords, size)
