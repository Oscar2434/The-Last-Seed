# Tamaño de ventana
WIDTH, HEIGHT = 780, 480
# Tamaños (Anchos y altos) 
WIDTH, HEIGHT = 780, 480
PERSONAJE = 60 
LUMBERJACK_SIZE = 50
GRASS = 64 
TREES = 64 
ROCK = 23 
#Animaciones 
SPRITES = 3
DOWN = 0 
RIGHT = 2 
UP = 3
MOVE_DOWN = 3 
MOVE_RIGHT = 4 
MOVE_UP = 3
F_SIZE = 64
DELAY_FPS = 100 
# Animaciones Leñador
LUMBERJACK_DOWN = 0
LUMBERJACK_LEFT = 1
LUMBERJACK_RIGHT = 2
LUMBERJACK_UP = 3
LUMBERJACK_F_SIZE = 32
LUMBERJACK_DELAY_FPS = 130
LUMBERJACK_ATTACK_LEFT = 4
LUMBERJACK_ATTACK_RIGHT = 5
#Colores 
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
