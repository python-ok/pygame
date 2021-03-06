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
        self.exp_img_group_4 = []
        self.bonus_image_group = []
        self.super_mob_img_group = []
        self.super_mob_last_occur = 0
        self.shoot_sound = []
        self.bg_music = []
        self.exp_sound = []
        
        self.load_data()
        
        self.all_sprites_group = 0
        self.all_mobs_group  = 0
        self.all_bulletes_group  = 0
        self.all_bonus_group = 0
        self.all_super_mobs_group = 0
        
        self.bonus_type = -1
        self.score = 0
        #缺省一条命， 一杆枪
        self.plane_lives = 1
   
        
        self.bg_img = random.choice(self.bg_img_group)
        self.bg_rect = self.bg_img.get_rect()


    def new(self):
        self.all_sprites_group = pygame.sprite.Group()
        self.all_mobs_group  = pygame.sprite.Group()
        self.all_bulletes_group  = pygame.sprite.Group()
     
        self.all_bonus_group  = pygame.sprite.Group()
        
        self.all_super_mobs_group = pygame.sprite.Group()
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
        
        for i in SUPER_MOB_IMG:
            self.super_mob_img_group.append(pygame.image.load(os.path.join(res_folder, i)).convert_alpha())
                
        
         
        #加载两组爆炸图片， 分别用于子弹击落坠石和坠石击中飞机
        for i in EXP_IMG_1:
            self.exp_img_group_1.append(pygame.image.load(os.path.join(res_folder, i)).convert_alpha())

        for i in EXP_IMG_2:
            self.exp_img_group_2.append(pygame.image.load(os.path.join(res_folder, i)).convert_alpha())

        for i in EXP_IMG_4:
            self.exp_img_group_4.append(pygame.image.load(os.path.join(res_folder, i)).convert_alpha())


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
    
        #飞机是否与坠石碰撞
        hits = pygame.sprite.spritecollide(self.plane, self.all_mobs_group, True, pygame.sprite.collide_circle)
        for hit in hits:           
            self.plane.shield -= hit.radius
            exp = Explosion(self, hit.rect.center, self.plane.rect.center, self.exp_img_group_1,hit.rect)
                        
            if self.plane.shield < 0:   
                self.plane_lives -= 1
                
                if self.plane_lives <= 0:
                    self.quit()
                else: #新的一条命是满血的
                    self.plane.shield = PLANE_SHIELD
            if hit.type == "common":
                Mob(self)
      
  
        hits = pygame.sprite.spritecollide(self.plane, self.all_bonus_group, True, pygame.sprite.collide_circle)
        for hit in hits:
            hit.bonus_take_effect()
        
        
        #合并Mob与super mob 处理
        hits = pygame.sprite.groupcollide(self.all_mobs_group, self.all_bulletes_group, False, True)
        for hit in hits:
            self.exp_sound[0].play()
            
            hit.shield -= BULLETE_DAMAGE
            if hit.shield <= 0:
                self.score += SUPER_MOB_SCORE
                if hit.type == "super":
                    Explosion(self, hit.rect.center, hit.rect.center, self.exp_img_group_4,hit.rect)
                else:
                    Explosion(self, hit.rect.center, hit.rect.center, self.exp_img_group_2,hit.rect)
                    
                hit.kill()
                if hit.type == "common":
                    Mob(self)
                 
                if random.random() > BONUS_POSSIBILITY:
                    self.bonus_type = random.choice(BONUS_TYPE)
                    bonus = Bonus(self, hit.rect.center, self.bonus_type)
        
        
        #每隔一段时间出现Super Mob
        now = pygame.time.get_ticks()            
        if now - self.super_mob_last_occur >= SUPER_MOB_TIME:
            self.super_mob_last_occur = now
            Super_Mob(self)
    
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
    

