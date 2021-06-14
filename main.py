import pygame
import random
import os,sys
from  sprites import *
from settings import *


class Game():
    def __init__(self):
        pygame.init()
       
        pygame.mixer.init()
        pygame.display.set_caption(GAME_TITLE)
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.font_name = pygame.font.match_font(FONT)
        
        self.stone_img_group = []
        self.bg_img_group = []
        self.bullet_img_group = []
        self.plane_img_group = []
        self.exp_img_group_1 = []
        self.exp_img_group_2 = []
        self.bonus_image_group = []
        
        self.shoot_sound = []
        self.bg_music = []
        self.exp_sound = []
        
        self.load_data()
        
        self.all_sprites_group = 0
        self.all_mobs_group  = 0
        self.all_bulletes_group  = 0
        self.all_bonus_group = 0
        
        self.bonus_type = -1
        self.score = 0
        #缺省一条命， 一杆枪
        self.plane_lives = 1
        self.power_account = 1
        self.power_start_time = 0
        
        self.bg_img = random.choice(self.bg_img_group)
        self.bg_rect = self.bg_img.get_rect()


    def new(self):
        self.all_sprites_group = pygame.sprite.Group()
        self.all_mobs_group  = pygame.sprite.Group()
        self.all_bulletes_group  = pygame.sprite.Group()
     
        self.all_bonus_group  = pygame.sprite.Group()
        
        
        self.plane = Plane(self)
        
        for i in range(MOB_COUNT):
            m = Mob(self)
    
    def load_data(self):
    
        for i in STONE_IMG:
            self.stone_img_group.append(pygame.image.load(os.path.join(res_folder,i)).convert_alpha())
     
        for i in BG_IMG:
            self.bg_img_group.append(pygame.image.load(os.path.join(res_folder, i)).convert())

        for i in BULLETE_IMG:
            self.bullet_img_group.append(pygame.image.load(os.path.join(res_folder, i)).convert_alpha())

        for i in PLANE_IMG:
            self.plane_img_group.append(pygame.image.load(os.path.join(res_folder, i)).convert_alpha())
  
        for i in BONUS_IMG:
            self.bonus_image_group.append(pygame.image.load(os.path.join(res_folder, i)).convert_alpha())
         
        #加载两组爆炸图片， 分别用于子弹击落坠石和坠石击中飞机
        for i in EXP_IMG_1:
            self.exp_img_group_1.append(pygame.image.load(os.path.join(res_folder, i)).convert_alpha())

        for i in EXP_IMG_2:
            self.exp_img_group_2.append(pygame.image.load(os.path.join(res_folder, i)).convert_alpha())

        for i in SHOOT_SOUND:
            self.shoot_sound.append(pygame.mixer.Sound(os.path.join(res_folder, i)))

        for i in EXP_SOUND:
            self.exp_sound.append(pygame.mixer.Sound(os.path.join(res_folder, i)))
                  
        for i in BG_MUSIC:
            self.bg_music.append(pygame.mixer.music.load(os.path.join(res_folder, i)))
            
        
    def draw_text(self, surf, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surf = font.render(text, True, WHITE)
        text_rect = text_surf.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surf, text_rect)
    
    def draw_plane_icons(self):
        icon_img = pygame.transform.scale(self.plane.image.copy(),(ICON_SIZE_W,ICON_SIZE_H))
        
        icon_rect = icon_img.get_rect()        
        for i in range(self.plane_lives):
            icon_rect.right = WIDTH - 5 - ICON_SIZE_W*i
            icon_rect.top =  5
            self.screen.blit(icon_img, icon_rect)
    
    def quit(self):
        pygame.quit()
        #确保程序退出， 否则会报错“pygame.error: display Surface quit”
        sys.exit()
        
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            

    def update(self):
        self.all_sprites_group.update()
    
        hits = pygame.sprite.spritecollide(self.plane, self.all_mobs_group, True, pygame.sprite.collide_circle)
        for hit in hits:
            #增加铠甲, 每次碰撞发生后，MOB需要消失(spritecollide 中设置True)，否则会持续产生碰撞，为了保证Mob的数量， 需要重新生成一个
           
            self.plane.shield -= hit.radius
            #如果击中，则产生爆炸效果,为了使碰撞效果更加真实， 将爆炸点设在两个物体（坠石与飞机）的中间或者接触点上， 而不是坠石的中心
            exp = Explosion(self, hit.rect.center, self.plane.rect.center, self.exp_img_group_1)
            
            if self.plane.shield < 0:   
                self.plane_lives -= 1
                
                if self.plane_lives <= 0:
                    self.quit()
                else: #新的一条命是满血的
                    self.plane.shield = PLANE_SHIELD
                
            Mob(self)

        hits = pygame.sprite.groupcollide(self.all_mobs_group, self.all_bulletes_group, True, True)
        for hit in hits:
            self.score += MOB_RADIUS_SIZE_MAX * 2 - hit.radius
            self.exp_sound[0].play()
            m = Mob(self)
            #如果击中，则产生爆炸效果        
           
            exp = Explosion(self, hit.rect.center, hit.rect.center, self.exp_img_group_2)
            
            if random.random() > BONUS_POSSIBILITY:
                self.bonus_type = random.choice(BONUS_TYPE)
                bonus = Bonus(self, hit.rect.center, self.bonus_type)
  
        hits = pygame.sprite.spritecollide(self.plane, self.all_bonus_group, True, pygame.sprite.collide_circle)
        for hit in hits:
            hit.bonus_take_effect()
        
        #这个无法放到bonus的update方法， 因为bonus对象会被kill掉
        if self.bonus_type == BONUS_ADD_POWER and self.power_account == 3:
            if pygame.time.get_ticks() - self.power_start_time > BONUS_POWER_TIME:
                self.power_account = 1
    
    def draw_shield_bar(self, x, y, blood):
        if blood < 0:
            blood = 0
        fill = (blood / PLANE_SHIELD) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(self.screen, BAR_FILL_COLOR, fill_rect)
        pygame.draw.rect(self.screen, BAR_OUTLINE_COLOR, outline_rect, BAR_OUTLINE_WIDTH)
        
    def draw(self):
       
        self.screen.blit(self.bg_img, self.bg_rect)
        
        self.all_sprites_group.draw(self.screen)

        self.draw_text(self.screen, str(self.score), FONT_SIZE, FONT_POS_X, FONT_POS_Y)
        self.draw_shield_bar(BAR_POS_X, BAR_POS_Y, self.plane.shield)
        
        self.draw_plane_icons()
        
        pygame.display.flip()
        
    def run(self):
    
        self.running = True
        pygame.mixer.music.play(loops = -1)
        
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            

    
if __name__ == '__main__':
    
    pg = Game()
    pg.new()
    pg.run()
    

