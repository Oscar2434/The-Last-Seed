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

class CentralTree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = "central_tree"  # ✅ AGREGAR ESTA LÍNEA
        
        # Cargar imagen del árbol central
        tree_path = os.path.join('assets', 'images', 'objects', 'treeC.png')
        try:
            self.image = pygame.image.load(tree_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (80, 80))
        except:
            # Placeholder si no existe la imagen
            self.image = pygame.Surface((80, 80), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (0, 100, 0), (0, 0, 80, 80))
        
        self.size = self.image.get_width()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Wall:
    def __init__(self, x, y, wall_type="normal", scale=None):
        self.x = x
        self.y = y
        self.wall_type = wall_type
        
        # Usar escala de constants si no se proporciona
        if scale is None:
            self.scale = constants.WALL_SCALE
        else:
            self.scale = scale
        
        # Elegir imagen según el tipo de pared
        if wall_type == "right":
            wall_path = os.path.join('assets', 'images', 'objects', 'pendiente.png')
        elif wall_type == "left":
            wall_path = os.path.join('assets', 'images', 'objects', 'sin_final.png')
        else:
            wall_path = os.path.join('assets', 'images', 'objects', 'arbusto largo.png')
            
        # Cargar y escalar imagen
        self.original_image = pygame.image.load(wall_path).convert_alpha()
        original_width = self.original_image.get_width()
        original_height = self.original_image.get_height()
        
        new_width = int(original_width * self.scale)
        new_height = int(original_height * self.scale)
        
        self.image = pygame.transform.scale(self.original_image, (new_width, new_height))
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
            image_path = os.path.join('assets', 'images', 'Items', 'banana.png')
        elif resource_type == "semillas":
            image_path = os.path.join('assets', 'images', 'Items', 'huevo.png')
        else:
            # Imagen por defecto si no existe
            image_path = os.path.join('assets', 'images', 'Items', 'banana.png')

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
            "composta": "¡Excelente! La cascara de platano es un buen abono orgánico para las plantas. \nProporciona nutrientes esenciales para el crecimiento de las plantas.",
            "semillas": "¡Excelente! La cáscara de huevo es rica en calcio y otros minerales que\nbenefician el suelo y las plantas."
        }
        return dialogs.get(self.type, "Este recurso ayuda a las plantas a crecer.")