import constants
import pygame
import os

class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        tree_path = os.path.join('assets', 'images', 'objects', 'tree.png')
        self.image = pygame.image.load(tree_path).convert_alpha() 
        self.image = pygame.transform.scale(self.image, (50, 30))  
        self.size = self.image.get_width()

    def draw(self, screen):
       screen.blit(self.image, (self.x, self.y))

class Rock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        rock_path = os.path.join('assets', 'images', 'objects', 'rock.png')
        self.image = pygame.image.load(rock_path).convert_alpha() 
        self.image = pygame.transform.scale(self.image, (constants.ROCK, constants.ROCK))  
        self.size = self.image.get_width()

    def draw(self, screen):
       screen.blit(self.image, (self.x, self.y))

class Bush:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        bush_path = os.path.join('assets', 'images', 'objects', 'bush.png')
        self.image = pygame.image.load(bush_path).convert_alpha() 
        self.image = pygame.transform.scale(self.image, (40, 20))  
        self.size = self.image.get_width()

    def draw(self, screen):
       screen.blit(self.image, (self.x, self.y))

class Wall:
    def __init__(self, x, y, wall_type="normal"):
        self.x = x
        self.y = y
        self.wall_type = wall_type
        
        # Elegir imagen según el tipo de pared
        if wall_type == "right":
            wall_path = os.path.join('assets', 'images', 'objects', 'izquierda.png')
        elif wall_type == "left":
            wall_path = os.path.join('assets', 'images', 'objects', 'derecha.png')
        else:
            wall_path = os.path.join('assets', 'images', 'objects', 'lave.png')
            
        self.image = pygame.image.load(wall_path).convert_alpha() 
        self.size = self.image.get_width()

    def draw(self, screen):
       screen.blit(self.image, (self.x, self.y))

class Resource:
    def __init__(self, x, y, resource_type):
        self.x = x
        self.y = y
        self.type = resource_type  # "composta", "agua", "semillas"
        self.collected = False
        self.size = 30  # Tamaño para colisiones
        
        # Cargar imagen según el tipo de recurso
        if resource_type == "composta":
            image_path = os.path.join('assets', 'images', 'objects', 'banana.png')
        elif resource_type == "agua":
            image_path = os.path.join('assets', 'images', 'objects', 'banana.png')
        elif resource_type == "semillas":
            image_path = os.path.join('assets', 'images', 'objects', 'banana.png')
        else:
            # Imagen por defecto si no existe
            image_path = os.path.join('assets', 'images', 'objects', 'banana.png')
            
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        except:
            # Crear un placeholder si la imagen no existe
            self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 0, 0), (self.size//2, self.size//2), self.size//2)

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, (self.x, self.y))
    
    def get_dialog_text(self):
        # Textos educativos para cada recurso
        dialogs = {
            "composta": "¡Excelente! La composta es abono orgánico que mejora \nel suelo y proporciona nutrientes esenciales \npara el crecimiento de las plantas.",
            "agua": "¡Perfecto! El agua es vital para la fotosíntesis \ny el transporte de nutrientes en las plantas. \n¡Mantén la hidratación adecuada!",
            "semillas": "¡Genial! Las semillas contienen el potencial \nde vida de nuevas plantas. Con los cuidados \ncorrectos, germinarán y crecerán fuertes."
        }
        return dialogs.get(self.type, "Este recurso ayuda a las plantas a crecer.")