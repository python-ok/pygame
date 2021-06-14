import os

#游戏目录
game_folder = os.path.dirname(__file__)
res_folder = os.path.join(game_folder, "resources")

#常用颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
WIDTH = 480
HEIGHT = 600

FPS = 60
GAME_TITLE = "Star Wars"

#字体
FONT = "arial"
FONT_SIZE = 18
FONT_POS_X = WIDTH / 2
FONT_POS_Y = 10

#坠石
MOB_COUNT = 10
MOB_RADIUS_SIZE_MIN = 30
MOB_RADIUS_SIZE_MAX = 60
MOB_ROTATE_SPEED = 8
MOB_ORG_POS_MIN_Y = -100
MOB_ORG_POS_MAX_Y = -40
MOB_SPEED_Y_MIN = 2 
MOB_SPEED_Y_MAX = 6
MOB_SPEED_X = 3
MOB_ROTATE_TICK = 20


#各种图片
PLANE_IMG = ['plane1.png','plane2.png','plane3.png', 'plane4.png', 'plane5.png', 'plane6.png']
BULLETE_IMG = ['bullet1.png','bullet2.png','bullet3.png']
BG_IMG = ['bg1.jpg','bg2.jpg','bg3.jpg','bg4.jpg']
STONE_IMG = ['stone1.png','stone2.png','stone3.png','stone4.png','stone5.png']
EXP_IMG_1 = ['ex1.png','ex2.png','ex3.png','ex4.png','ex5.png','ex6.png','ex7.png','ex8.png','ex9.png']
EXP_IMG_2 = ['exx1.png','exx2.png','exx3.png','exx4.png','exx5.png','exx6.png','exx7.png','exx8.png','exx9.png','exx10.png','exx11.png']
EXP_IMG_3 = ['exy01_01.png','exy01_02.png','exy01_03.png','exy01_04.png','exy01_05.png','exy01_06.png','exy01_07.png','exy01_08.png']

#声音和音乐
EXP_SOUND = ['exp.wav'] 
BG_MUSIC = ['game.wav'] 
SHOOT_SOUND = ['shoot1.wav', 'shoot2.wav']

#战斗机
PLANE_SIZE_W = 100
PLANE_SIZE_H = 60
PLANE_SPEED = 8
PLANE_SHIELD = MOB_RADIUS_SIZE_MAX * 3
PLANE_SHOOT_TIME = 100

#子弹
BULLET_SIZE_W = 10
BULLET_SIZE_H = 20
BULLET_SPEED = 10

#血量展示
BAR_HEIGHT = 40
BAR_LENGTH = 100
BAR_FILL_COLOR = GREEN
BAR_OUTLINE_COLOR = WHITE
BAR_OUTLINE_WIDTH = 2
BAR_POS_X = 5
BAR_POS_Y = 5


#爆炸的FPS和爆炸图片展示尺寸
EXPLOSION_FPS = 50
EXP_SIZE_W = 50
EXP_SIZE_H = 50

BONUS_ADD_BLOOD = 0
BONUS_ADD_LIVE = 1
BONUS_ADD_POWER = 2

BONUS_TYPE = [BONUS_ADD_BLOOD, BONUS_ADD_LIVE, BONUS_ADD_POWER]
BONUS_IMG = ['bonus-1.png', 'bonus-2.png', 'bonus-3.png']
BONUS_SPEED = 10
BONUS_SIZE_W = 40
BONUS_SIZE_H = 40
BONUS_POSSIBILITY = 0.97

#火力增强时间为10000毫秒，也就是10秒
BONUS_POWER_TIME = 10000

PLANE_MAX_LIVES = 3
ICON_SIZE_W = 40
ICON_SIZE_H = 30


