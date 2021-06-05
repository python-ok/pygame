import pygame
import random
import os

#获取游戏目录， 也就是本文件所在的目录
game_folder = os.path.dirname(__file__)

#获取游戏的资源目录，里面存在着图片，音频等资源
res_folder = os.path.join(game_folder, "resources")

#显示界面的宽度，高度和刷新率
WIDTH = 480
HEIGHT = 600

#较高的FPS会使物体移动的更加平滑
FPS = 60

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

#定义一个游戏精灵类-飞机
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        #加载飞机图片
        player_img = pygame.image.load(os.path.join(res_folder, "plane1.png")).convert()
        
        #设置图片的尺寸（原图片可能过大）
        self.image = pygame.transform.scale(player_img,(50,50))

        #设置飞机的外观尺寸，也就是图片的尺寸
        self.rect = self.image.get_rect()

        #设置飞机的位置， 底部中心
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        
        #设置初始速度为0，speedx表示横向的移动速度， 后面我们会增加纵向的移动
        self.speedx = 0
     
    #当该精灵加入pygame.sprite.Group中后， 每次group的update会调用各个精灵的update函数
    def update(self):
        self.speedx = 0
        #根据按键操作飞机的左右移动
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx += -8
        if keystate[pygame.K_RIGHT]:
            self.speedx += +8
            
        self.rect.x += self.speedx
        
        #确保飞机始终在屏幕显示范围内， 注意rect.x, rect.y, rect.left, rect.right, rect.bottom, rect.top, rect.centerx等
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    

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

