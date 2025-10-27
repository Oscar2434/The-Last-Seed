# Tamaño de ventana
WIDTH, HEIGHT = 780, 480

# Tamaños (Anchos y altos)
PERSONAJE = 60 
TREE_SIZE = 80
LUMBERJACK_SIZE = 50
GRASS = 64 
TREES = 64 
ROCK = 23 

# Animaciones Personaje
SPRITES = 3
DOWN = 0 
RIGHT = 2 
UP = 3
MOVE_DOWN = 3 
MOVE_RIGHT = 4 
MOVE_UP = 3
F_SIZE = 64
DELAY_FPS = 100 

# Animaciones Incendiario (antes leñador)
LUMBERJACK_DOWN = 0
LUMBERJACK_LEFT = 1
LUMBERJACK_RIGHT = 2
LUMBERJACK_UP = 3
LUMBERJACK_F_SIZE = 32   # tamaño de cada frame en spritesheet
LUMBERJACK_DELAY_FPS = 130
LUMBERJACK_ATTACK_LEFT = 4
LUMBERJACK_ATTACK_RIGHT = 5

# Recurso - Agua (cubeta)
WATER_SIZE = 40    # tamaño visual en pantalla
WATER_F_SIZE = 64      # tamaño real del frame en spritesheet
WATER_FRAMES = 10      # columnas
WATER_ANIM_DELAY = 120

# Fuego
FIRE_SIZE = 70      # tamaño visual en pantalla
FIRE_F_SIZE = 64       # tamaño real del frame en spritesheet
FIRE_FRAMES = 5        # columnas
FIRE_ANIM_DELAY = 120

# Colores 
WHITE = (255, 255, 255) 
BLUE = (0, 0, 255) 
GREEN = (0, 255, 0) 
BROWN = (139, 69, 19)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Juego - Árbol y enemigos
TREE_HEALTH = 280
ENEMY_DAMAGE = 2
ENEMY_SPEED = 1
RESOURCE_HEAL = 20
LEVEL_TIME = 60  # segundos

# Configuraciones de niveles
LEVEL1_CONFIG = {
    "easy": {
        "max_enemies": 5,   # Máximo 5 enemigos en pantalla
        "spawn_delay": 300  # Spawn cada 5 segundos 
    },
    "hard": {
        "max_enemies": 8,   # Máximo 8 enemigos
        "spawn_delay": 240  # Spawn cada 4 segundos
    }
}
