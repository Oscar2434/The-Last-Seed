import pygame
import sys
import constants
from character import Character
from world import World

#Iniciar pygame 
pygame.init()

#Ventana
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("The last seed")


def main():
    clock = pygame.time.Clock()
    game_world = World(constants.WIDTH, constants.HEIGHT)
    game_character = Character(constants.WIDTH //2, constants.HEIGHT //2)

#Bucle
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
         pygame.quit()
         sys.exit()

      keys = pygame.key.get_pressed()
      if keys[pygame.K_LEFT]:
         game_character.move(dx=-5, dy=0)
      if keys[pygame.K_RIGHT]:
         game_character.move(dx=5, dy=0)
      if keys[pygame.K_UP]:
         game_character.move(dx=0, dy=-5)
      if keys[pygame.K_DOWN]:
         game_character.move(dx=0, dy=5)

      game_world.draw(screen)
      game_character.draw(screen)

      pygame.display.flip()
      clock.tick(60)

if __name__ == "__main__":
    main()