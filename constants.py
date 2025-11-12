# Tamaño de ventana
WIDTH, HEIGHT = 780, 480

# Tamaños (Anchos y altos)
PERSONAJE = 60 
TREE_SIZE = 100
LUMBERJACK_SIZE = 50
GRASS = 64 
TREES = 64 
ROCK = 23 

# Tamaños adicionales de árboles
TREE_SMALL = 48    
TREE_MEDIUM = 64       
TREE_LARGE = 80     
TREE_HUGE = 120        

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
LUMBERJACK_F_SIZE = 32   
LUMBERJACK_DELAY_FPS = 130
LUMBERJACK_ATTACK_LEFT = 4
LUMBERJACK_ATTACK_RIGHT = 5

# Recurso - Agua (cubeta)
WATER_SIZE = 40   
WATER_F_SIZE = 64     
WATER_FRAMES = 10      
WATER_ANIM_DELAY = 120

# Fuego
FIRE_SIZE = 60    
FIRE_F_SIZE = 64       
FIRE_FRAMES = 5       
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
# --- CONFIGURACIÓN DE DIFICULTADES ---
DIFFICULTY_SETTINGS = {
    "normal": {
        "ENEMY_SPEED": 1,
        "ENEMY_DAMAGE": 2,
        "LEVEL_TIME": 90,
        "max_enemies": 5,
        "spawn_delay": 300
    },
    "avanzado": {
        "ENEMY_SPEED": 2,
        "ENEMY_DAMAGE": 6,
        "LEVEL_TIME": 60,
        "max_enemies": 8,
        "spawn_delay": 240
    }
}
