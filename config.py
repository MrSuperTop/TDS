import pygame

# * Settings
windowSize = (1920, 1080)
windowCenter = (windowSize[0] / 2, windowSize[1] / 2)

FPS = 60
drawColliderBorders = True
weaponChangeDelay = 0.1  # ~ Time in second which sets how often you can change the weapon
bulletSpeed = 15

# * Constants
colors = {
  'white': (255, 255, 255)
}

startText = 'Добро пожаловать в TDS'

# * Variables
window = pygame.display.set_mode(list(windowSize))
