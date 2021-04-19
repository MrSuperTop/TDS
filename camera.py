from pygame.math import Vector2
from config import windowSize
from abc import ABC, abstractmethod


class Camera():
  """
  Camera All the info needed to blit sprite with a shift will be got from here
  """  

  def __init__(
    self,
    renderSurface: object
  ) -> None:
    self.surface = renderSurface  # ~ Save the surface where all sprites will be rendered
    self.offset = Vector2(0, 0)

  def addPlayer(self, player: object) -> None:
    self.player = player

  def scroll(self):
    self.offset.x += int(self.player.velocity.x)
    self.offset.y += int(self.player.velocity.y)