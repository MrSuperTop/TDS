from typing import Union

import pygame

from groups import texts


class Text(pygame.sprite.Sprite):
    def __init__(
      self,
      camera,
      coords: Union[tuple[float, float], list[float, float]] = (0, 0),
      text = '',
      fontSize = 16,
      color = (0, 0, 0),
      bold = False,
      font='Arial'
    ):
      super(Text, self).__init__()

      self.surface = camera.surface
      self.color = color
      self.font = pygame.font.SysFont(font, fontSize, bold)
      self.value = text

      self.rect = None
      self.text = text
      self.rect = self.image.get_rect(center=coords)

      texts.add(self)

    @property
    def text(self):
      return self.value

    @text.setter
    def text(self, newText):
      self.image = self.font.render(str(newText), 1, self.color)
      if self.rect is not None:
        self.rect = self.image.get_rect(center=self.rect.topleft)
      else:
        self.rect = self.image.get_rect()

      self.value = newText

    def update(self):
      self.surface.blit(self.image, self.rect)

# class Text(pygame.sprite.Sprite):
#   def __init__(
#     self,
#     fontName: str,
#     color,
#     coords: 
#   ):
#     self.
