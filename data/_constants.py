""" 상수를 모아놓은 곳. """

# IN-GAMES #

GAME_TITLE_NAME = "Powerful Ping-Pong"

FPS = 100
TILE_LENGTH = 40  # 타일 한 변의 길이

COLL_CHECK_EXCEPTION = ('Field', 'Skill')


#


""" WORDS """


SAVE, LOAD = 'save', 'load'
EASY, NORMAL, HARD = 'easy', 'normal', 'hard'
DEFALUT = 'default'

# Debug status: processing_time_gauge()
DANGER, WARNING = 'DANGER', 'WARNING'
CAUTION, NOTICE, SAFETY = 'CAUTION', 'NOTICE', 'SAFETY'  # 비표시 권장

# Logic operator
OR, AND, XOR, ALL = 'or', 'and', 'xor', 'all'

# Time
IN, OVER, UNDER, BETWEEN = 'in', 'over', 'under', 'between'

# Movements
UP, DOWN, LEFT, RIGHT, JUMP = 'up', 'down', 'left', 'right', 'jump'
STOP, VERT, HRZN, DIAG, FREE = 'stop', 'vert', 'hrzn', 'diag', 'free'

# Switch / Status / Precessing
ON, READY, ACTIVE, DONE, OFF = 'on', 'ready', 'active', 'done', 'off'
AVAILABLE, RUNNING, WAITING = 'available', 'running', 'waiting'
PUSH, UNPUSH = 'push', 'unpush'  # 문법적으로 어긋나나 직관성을 우선

# Rect / Position / Location
TOP, BOTTOM = 'top', 'bottom'  # +LEFT, +RIGHT
TOPLEFT, BOTTOMLEFT, TOPRIGHT, BOTTOMRIGHT = 'tl', 'bl', 'tr', 'br'
MIDTOP, MIDLEFT, MIDBOTTOM, MIDRIGHT = 'mt', 'ml', 'mb', 'mr'
CENTER, CENTERX, CENTERY = 'center', 'centerx', 'centery'

# Mouse
CLICK_LEFT_DOWN, CLICK_LEFT_UP = 'click_left_down', 'click_left_up'
CLICK_MIDDLE_DOWN, CLICK_MIDDLE_UP = 'click_middle_down', 'click_middle_up'
CLICK_RIGHT_DOWN, CLICK_RIGHT_UP = 'click_right_down', 'click_right_up'
WHEEL_UP, WHEEL_DOWN, NOTHING = 'wheel_up', 'wheel_down', 'nothing'  # +None


#


""" COLORS """

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)

SKYBLUE = (93, 148, 251)
