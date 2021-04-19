import os
from typing import Union

import config as cfg
import pygame
from config import FPS, window

from sprites.collider import Collider
from sprites.game_sprite import GameSprite, getSize


# * Groups
collidingObjects = pygame.sprite.Group()


class Entity(GameSprite):
  dead = False

  def __init__(
    self,
    camera: object,
    coords: Union[tuple[float, float], list[float, float]] = (0, 0),
    sizeScaler: float = 1,
    imgPath: str = '',
    collider: Collider = None,
    health: int = 100,
    drawCollider: bool = cfg.drawColliderBorders,
  ) -> None:
    super().__init__(camera, coords, sizeScaler, imgPath)

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

    # * Stuff to position the sprite correctly on the first frame
    self.startPosition = self.rect.topleft
  
    # TODO: Make an ability to set animations throught the GameSprite class for every sprite in the game
    # * Animations
    self.animations = {}
    self.startingFrames = {}
    self.animationFrames = {}
    self.frame = 0  # ~ stores current frame number

  @property
  def animation(self) -> str:
    return self._animation

  @animation.setter
  def animation(self, newValue: str) -> None:
    if newValue != self._animation:
      self._animation = newValue
      self.frame = self.startingFrames[newValue]

  def loadAnimation(self, folderPath: str, frame_id: str, frameRate: int, startFrame: int = 0):
    folderPath = 'images/' + folderPath
    numberOfFrames = len([item for item in os.listdir(folderPath)])
    framesDuration = [int(FPS / frameRate)] * numberOfFrames

    animationName = folderPath.split('/')[-1]
    weaponName = folderPath.split('/')[-2]
    self.animationsFrameData = []

    for i, frame in enumerate(framesDuration):
      frameId = f'{frame_id}_{i}'
      imagePath = f'{folderPath}/survivor-{animationName}_{weaponName}_{i}.png'
      image = pygame.image.load(imagePath).convert_alpha()
      self.animationFrames[frameId] = image.copy()

      for i in range(frame):
        self.animationsFrameData.append(frameId)

    self.animations[frame_id] = self.animationsFrameData
    self.startingFrames[frame_id] = startFrame

  def nextFrame(self):
    self.frame += 1
    frameIds = self.animations[self.animation]

    if self.frame >= len(frameIds):
      self.frame = 0

    nextFrameId = frameIds[self.frame]

    nextFrame = self.animationFrames[nextFrameId]
    self.originalImage = pygame.transform.scale(
      nextFrame,
      getSize(nextFrame, self.imageScale)
    )

  def die(self):
    """
    die Sets dead attr to True and prite won't be rendered anymore
    """

    self.dead = True

  def draw(self):
    """
    draw Will draw the sprite on the screen. If drawColliderBorders is enabled
    will also draw sprites rect and collider.

    Args:
        surface (pygame.Surface): [description]
    """

    if self.drawCollider:
      pygame.draw.rect(window, (0, 255, 0), self.rect, 4)
      pygame.draw.rect(window, (255, 0, 0), self.collider.move(self.rect.topleft), 4)
    if self.camera is not None:
      self.rect.x, self.rect.y = self.startPosition[0] - self.camera.offset.x, self.startPosition[1] - self.camera.offset.y
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
