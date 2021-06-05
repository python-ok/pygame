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
        player_img = pygame.image.load(os.path.join(res_folder, "plane1.png")).convert_alpha()
        
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

     #发射子弹       
    def shoot(self):
        #新生一枚子弹， 在飞机的头部
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        all_bullets.add(bullet)
    
#定义一个游戏精灵类-怪物
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        #怪物图片设置
        Mod_img = pygame.image.load(os.path.join(res_folder, "stone1.png")).convert_alpha()
        self.image = pygame.transform.scale(Mod_img,(50,50))
        self.rect = self.image.get_rect()

        #每个怪物精灵初始位置和向下的速度都是随机的
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(1, 8)
     
    def update(self):
        #怪物始终是向下坠落的
        self.rect.y += self.speedy
        
        #如果一个怪物坠落出了屏幕， 则重置它的位置和速度（重生了！）
        if self.rect.top > HEIGHT+10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(1, 8)
    
#定义一个游戏精灵类-子弹
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y): #创建子弹对象是需要指定起始坐标， 其实就是飞机的坐标
        pygame.sprite.Sprite.__init__(self)
        
        #子弹图片设置
        butllet_img = pygame.image.load(os.path.join(res_folder, "bullet1.png")).convert_alpha()
        self.image = pygame.transform.scale(butllet_img,(10,20))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        
        #子弹总是向上飞
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
  
        #如果一个子弹飞出了屏幕， 它就会消失
        if self.rect.bottom < 0:
            self.kill()


#创建一个精灵组，所有的精灵（飞机和怪物）都加入到这个组统一管理（统一更新和绘制， update/draw）
all_sprites = pygame.sprite.Group()

#创建一个飞机精灵对象
player = Player()

#将飞机加入到精灵组中
all_sprites.add(player)

#为了AABB碰撞检测，需要将怪物单独放到一个精灵组中
all_mobs = pygame.sprite.Group()

#创建一个子弹精灵组
all_bullets = pygame.sprite.Group()


#产生10个怪物精灵,并加入精灵组中
for i in range(10):
    m = Mob()
    all_sprites.add(m)
    all_mobs.add(m)
    
running = True

#游戏的主循环，每一帧按照是否退出->更新->绘制->反转显示的流程重复进行
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        #用户按空格键时，发射子弹
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
        
    #更新所有的飞机和怪物的位置
    all_sprites.update()
    
    #AABB碰撞检测，检测飞机是否与怪物碰撞，是1对多， 最后一个参数如果是True表示碰撞后，怪物将消失
    hits = pygame.sprite.spritecollide(player, all_mobs, False)
    if hits:
        running = False
        continue
    
    #AABB碰撞检测，检测子弹是否与怪物碰撞， 是多对多， 所用groupcollide，True， True 表示碰撞后子弹和怪物都消失
    hits = pygame.sprite.groupcollide(all_bullets, all_mobs, True, True)
    if hits:
        #为了保持怪物的数量， 碰撞后， 需要加入新的怪物
        m = Mob()
        all_sprites.add(m)
        all_mobs.add(m)
    
    
    #绘制背景
    screen.fill(BLACK)   
    
    #绘制所有的飞机和怪物
    all_sprites.draw(screen)
    
    #画面显示
    pygame.display.flip()
    
    #控制游戏按照指定的帧率刷新
    clock.tick(FPS)
    
#游戏退出，释放之前创建的模块和资源
pygame.quit()

