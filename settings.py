import os

game_folder = os.path.dirname(__file__)
res_folder = os.path.join(game_folder, "resources")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)

WIDTH = 480
HEIGHT = 600

FPS = 60

GAME_TITLE = "Star Wars"

FONT = "arial"
FONT_SIZE = 18
FONT_POS_X = WIDTH / 2
FONT_POS_Y = 10

MOB_COUNT = 10
MOB_RADIUS_SIZE_MIN = 30
MOB_RADIUS_SIZE_MAX = 60
MOB_ROTATE_SPEED = 8
MOB_ORG_POS_MIN_Y = -100
MOB_ORG_POS_MAX_Y = -40
MOB_SPEED_Y_MIN = 2 
MOB_SPEED_Y_MAX = 6
MOB_SPEED_X = 3
MOB_ROTATE_TICK = 100

game_folder = os.path.dirname(__file__)
res_folder = os.path.join(game_folder, "resources")


PLANE_IMG = ['plane1.png','plane2.png','plane3.png', 'plane4.png']
BULLETE_IMG = ['bullet1.png','bullet2.png','bullet3.png']
BG_IMG = ['bg1.jpg','bg2.jpg','bg3.jpg','bg4.jpg']
STONE_IMG = ['stone1.png','stone2.png','stone3.png','stone4.png','stone5.png']

#声音和音乐
EXP_SOUND = ['exp.wav'] 
BG_MUSIC = ['game.wav'] 
SHOOT_SOUND = ['shoot1.wav', 'shoot2.wav']

PLANE_SIZE_W = 70
PLANE_SIZE_H = 40
PLANE_SPEED = 8


BULLET_SIZE_W = 10
BULLET_SIZE_H = 20
BULLET_SPEED = 10