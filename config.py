import pygame

# * Settings
windowSize = (1200, 720)
FPS = 60
drawColliderBorders = True
weaponChangeDelay = 0.5  # ~ Time in second which sets how often you can change the weapon
weaponShootingDelay = 0.1

# * Constants
colors = {
  'white': (255, 255, 255)
}

# * Variables
window = pygame.display.set_mode(list(windowSize))
