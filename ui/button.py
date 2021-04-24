from typing import Union
from dataclasses import dataclass

import pygame
from groups import buttons

from ui.text import Text


# * Events
class OnClick:
  name = 'click'

  def __init__(self, handler):
    self.handler = handler

  def check(self, buttonRect: pygame.Rect):
    x, y = pygame.mouse.get_pos()
    inButton = buttonRect.left <= x <= buttonRect.right and buttonRect.top <= y <= buttonRect.bottom
    pressed = pygame.mouse.get_pressed()[0]
    return inButton and pressed


# * Class itself
class Button(pygame.sprite.Sprite):
  event = None

  def __init__(
    self,
    camera,
    # TODO: Make defaults to be window center is None is passed for x or y
    centerCoords: Union[tuple[float, float], list[float, float]] = (0, 0),
    size: Union[tuple[float, float], list[float, float]] = (0, 0),
    text = '',
    fontSize = 16,
    textColor = (0, 0, 0),
    boldText = False,
    color = (255, 0, 0)
  ):
    super().__init__()

    self.renderSurface = camera.surface
    self.color = color

    self.surface = pygame.Surface(size)
    self.rect = self.surface.fill(color)

    self.rect.center = centerCoords
    self.text = Text(camera, (0, 0), text, fontSize, textColor, bold=boldText)
    self.text.rect.center = self.rect.center

    buttons.add(self)

  def addEvent(self, event: object):
    self.event = event

  def update(self):
    if self.event is not None and self.event.name == 'click':
      if self.event.check(self.rect):
        self.event.handler()

    self.renderSurface.blit(self.surface, self.rect)
    self.text.update()
