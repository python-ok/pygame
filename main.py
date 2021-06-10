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
        self.shoot_sound = []
        self.bg_music = []
        self.exp_sound = []
        
        self.load_data()
        
        self.all_sprites_group = 0
        self.all_mobs_group  = 0
        self.all_bulletes_group  = 0
        self.score = 0
        
        self.bg_img = random.choice(self.bg_img_group)
        self.bg_rect = self.bg_img.get_rect()


    def new(self):
        self.all_sprites_group = pygame.sprite.Group()
        self.all_mobs_group  = pygame.sprite.Group()
        self.all_bulletes_group  = pygame.sprite.Group()
        
        
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
    
    
    def quit(self):
        pygame.quit()
        #确保程序退出， 否则会报错“pygame.error: display Surface quit”
        sys.exit()
        
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.plane.shoot()

    def update(self):
        self.all_sprites_group.update()
    
        hits = pygame.sprite.spritecollide(self.plane, self.all_mobs_group, True, pygame.sprite.collide_circle)
        for hit in hits:
            #增加铠甲, 每次碰撞发生后，MOB需要消失(spritecollide 中设置True)，否则会持续产生碰撞，为了保证Mob的数量， 需要重新生成一个
           
            self.plane.shield -= hit.radius
            if self.plane.shield < 0:                   
                self.quit()
                
                
            Mob(self)

        hits = pygame.sprite.groupcollide(self.all_mobs_group, self.all_bulletes_group, True, True)
        for hit in hits:
            self.score += MOB_RADIUS_SIZE_MAX * 2 - hit.radius
            self.exp_sound[0].play()
            m = Mob(self)
    
    
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
    

