import pygame
import random

#显示界面的宽度，高度和刷新率
WIDTH = 360
HEIGHT = 480
FPS = 30

#初始化pygame
pygame.init()

#pygame声音模块初始化
pygame.mixer.init()

#创建显示界面并设置高度和宽度
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#设置显示界面的标题
pygame.display.set_caption("My Game")

#创建游戏时钟
clock = pygame.time.Clock()

#常用的颜色定义， （R，G，B）
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)

#定义一个游戏精灵类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #为游戏精灵指定一个图像对象，并设置大小
        self.image = pygame.Surface((50, 50))
        #填充颜色
        self.image.fill(GREEN)
        #设置精灵的外观尺寸，也就是图片的尺寸
        self.rect = self.image.get_rect()
        #设置精灵的中心位置，也就是显示屏幕的中心
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
     
    #当该精灵加入pygame.sprite.Group中后， 每次group的update会调用各个精灵的update函数
    def update(self):
        self.rect.x += 5
        if self.rect.x >= WIDTH:
            self.rect.x = 0
    

#创建一个精灵组对象， 游戏中所有的精灵都将加入到这个组中， 统一管理
all_sprites = pygame.sprite.Group()

#创建一个精灵对象
player = Player()

#将精灵对象加入到精灵组中
all_sprites.add(player)

running = True

#游戏的主循环，每一帧按照是否退出->更新->绘制->反转显示的流程重复进行
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
    
    #跟新所有的游戏精灵
    all_sprites.update()
    
    #绘制背景
    screen.fill(BLACK)   
    
    #绘制所有的精灵
    all_sprites.draw(screen)
    
    #画面显示
    pygame.display.flip()
    
    #控制游戏按照指定的帧率刷新
    clock.tick(FPS)
    
#游戏退出，释放之前创建的模块和资源
pygame.quit()

