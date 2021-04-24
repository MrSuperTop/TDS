import pygame

# * Settings
# windowSize = (1920 / 2, 1080 / 2)
windowSize = (1280, 720)
windowCenter = (windowSize[0] / 2, windowSize[1] / 2)

FPS = 60
drawColliderBorders = True
weaponChangeDelay = 0.1  # ~ Time in second which sets how often you can change the weapon
bulletSpeed = 15

# * Constants
buttonsColor = (41, 121, 255)
buttonsTextColor = (255, 255, 255)
colors = {
  'white': (255, 255, 255),
}

startText = 'Добро пожаловать в TDS'

# * Variables
window = pygame.display.set_mode(list(windowSize))
