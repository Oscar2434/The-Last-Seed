import constants
import pygame
import os

class Objeto:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        grass_path = os.path.join("assets", "images", "objects", "grass3.png")
        self.grass_image = pygame.image.load(grass_path).convert()
        self.grass_image = pygame.transform.scale(
            self.grass_image, (constants.GRASS, constants.GRASS)
        )

        tree_img = pygame.image.load(
            os.path.join("assets", "images", "objects", "treeC.png")
        ).convert_alpha()
        tree_img = pygame.transform.scale(
            tree_img, (constants.TREES, constants.TREES)
        )

        self.obstacles = []
        posiciones = [
            (140, 120),
            (560, 120),
            (350, 260),
        ]
        for x, y in posiciones:
            o = Objeto(x, y, tree_img)
            o.rect = o.rect.inflate(-20, -20)
            self.obstacles.append(o)

        self.bote_img = pygame.image.load(
            os.path.join("assets", "images", "effects", "bote.png")
        ).convert_alpha()

       
        self.bote_img = pygame.transform.scale(self.bote_img, (45, 45))

        # Subido 
        bx = width // 2 - 22
        by = height // 2 - 75   

        self.bote = Objeto(bx, by, self.bote_img)
       

    def draw(self, screen):
        for y in range(0, self.height, constants.GRASS):
            for x in range(0, self.width, constants.GRASS):
                screen.blit(self.grass_image, (x, y))

        for o in self.obstacles:
            o.draw(screen)

        self.bote.draw(screen)

    def zona_libre(self, rect):
        for o in self.obstacles:
            if rect.colliderect(o.rect):
                return False
        if rect.colliderect(self.bote.rect):
            return False
        return True
