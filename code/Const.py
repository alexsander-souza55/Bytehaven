WIDTH  = 800
HEIGHT = 450
FPS    = 60
TITLE  = "BYTEHAVEN — THE LOST CONTAINERS"

# Cores
BLACK   = (0,   0,   0)
WHITE   = (255, 255, 255)
CYAN    = (0,   245, 255)
PURPLE  = (136, 0,   255)
RED     = (204, 0,   0)
DARK_BG = (5,   5,   15)
GREEN   = (0,   255, 100)

# Física
GRAVITY       = 0.6
MAX_FALL      = 14

# Tiles
TILE  = 32

# Jogador
P_HP          = 300
P_SPEED       = 4
P_JUMP        = -13
P_SHOT_DELAY  = 15
P_SHOT_DMG    = 30
P_SHOT_SPEED  = 9
P_FRAME       = 48
P_SCALE       = 2
P_HURT_FRAMES = 40

# Inimigo 1 (Biker — patrulheiro)
E1_HP      = 80
E1_SPEED   = 2
E1_SCORE   = 100
E1_DMG     = 15
E1_FRAME   = 48
E1_SCALE   = 2

# Inimigo 2 (Punk — atirador)
E2_HP         = 60
E2_SPEED      = 1
E2_SCORE      = 125
E2_DMG        = 10
E2_SHOT_DELAY = 160
E2_SHOT_DMG   = 20
E2_SHOT_SPEED = 5
E2_FRAME      = 48
E2_SCALE      = 2

# Container coletável
CONT_W = 32
CONT_H = 48
CONTAINERS_PER_LEVEL = 3

# Velocidade de animação (frames entre atualizações)
ANIM_SPEED = 6

# Estados do jogo
ST_MENU    = "menu"
ST_LEVEL1  = "level1"
ST_LEVEL2  = "level2"
ST_VICTORY = "victory"
ST_LOSE    = "lose"

# Controles exibidos no menu
CONTROLS = [
    "A / D     —  Mover",
    "W / SPACE —  Pular",
    "CTRL      —  Atirar",
    "ESC       —  Menu",
]
