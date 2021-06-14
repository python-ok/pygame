import pygame
import random
import os
from settings import *


class Bonus(pygame.sprite.Sprite):
    def __init__(self, game, center, bonus_type):
        pygame.sprite.Sprite.__init__(self)
        
        self.game_handle = game
        #不同类型的bonus（加血，加命，加导弹，加炸弹，增强火力等）
        self.bonus_type = bonus_type
        self.bonus_image = self.game_handle.bonus_image_group[self.bonus_type]
        
        self.image = pygame.transform.scale(self.bonus_image,(BONUS_SIZE_W,BONUS_SIZE_H))

        self.rect = self.image.get_rect()
       
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
        self.speedy = BONUS_SPEED
        
        game.all_sprites_group.add(self)
        game.all_bonus_group.add(self)
        
    def bonus_take_effect(self):
        if self.bonus_type == BONUS_ADD_BLOOD:
            self.game_handle.plane.shield = PLANE_SHIELD
        elif self.bonus_type == BONUS_ADD_LIVE:
            if self.game_handle.plane_lives < PLANE_MAX_LIVES:
                self.game_handle.plane_lives += 1
        elif self.bonus_type == BONUS_ADD_POWER: #额外增加两杆枪
            
                self.game_handle.power_start_time = pygame.time.get_ticks()
                self.game_handle.power_account = 3
                
                
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
        

class Explosion(pygame.sprite.Sprite):
    def __init__(self, game, center1, center2, exp_image_group):
        pygame.sprite.Sprite.__init__(self)
        self.game_handle = game
        
        self.exp_image_group = exp_image_group
        
        self.image = pygame.transform.scale(self.exp_image_group[0],(EXP_SIZE_W,EXP_SIZE_H))

        self.rect = self.image.get_rect()
        center = ((center1[0]+center2[0])/2, (center1[1]+center2[1])/2)
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = EXPLOSION_FPS
        
        game.all_sprites_group.add(self)
        
    def update(self):
        now = pygame.time.get_ticks()
        if  now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.exp_image_group):
                self.kill()
            else:    
                #逐帧展示整个爆炸组图片
                center = self.rect.center
                self.image = pygame.transform.scale(self.exp_image_group[self.frame],(EXP_SIZE_W,EXP_SIZE_H))
                self.rect = self.image.get_rect()
                self.rect.center = center
                
                
        
class Plane(pygame.sprite.Sprite):
    def __init__(self,game):
        pygame.sprite.Sprite.__init__(self)

        self.game_handle = game
        
        plane_img = random.choice(game.plane_img_group)
        
        
        self.image = pygame.transform.scale(plane_img,(PLANE_SIZE_W,PLANE_SIZE_H))
        
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width/2) 
        
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
                
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
            
        self.speedx = 0
        self.shield = PLANE_SHIELD
        self.last_shoot = pygame.time.get_ticks()
        self.shoot_time = PLANE_SHOOT_TIME
        game.all_sprites_group.add(self)
    
    def update(self):
     
        self.speedx = 0
        
        
        keystate = pygame.key.get_pressed()
        #长按键， 实现持续移动和自动发射
        if keystate[pygame.K_LEFT]:
            self.speedx += -PLANE_SPEED
        if keystate[pygame.K_RIGHT]:
            self.speedx += +PLANE_SPEED
        if keystate[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            #控制子弹发射的频率
            if now - self.last_shoot > self.shoot_time:
                self.last_shoot = now
                self.shoot()
            
        self.rect.x += self.speedx
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    
    def shoot(self):
        
        bullet = Bullet(self.rect.centerx, self.rect.top, self.game_handle)
        if self.game_handle.power_account == 3:
            bullet = Bullet((self.rect.centerx+self.rect.left)/2, self.rect.top, self.game_handle)
            bullet = Bullet((self.rect.centerx+self.rect.right)/2, self.rect.top, self.game_handle)

       # self.game_handle.all_sprites_group.add(bullet)
       # self.game_handle.all_bulletes_group.add(bullet)
                
        self.game_handle.shoot_sound[0].play()
    

class Mob(pygame.sprite.Sprite):
    def __init__(self,game):
        pygame.sprite.Sprite.__init__(self)
        
        self.game_handle = game
        Mod_img = random.choice(self.game_handle.stone_img_group)

        size=random.randrange(MOB_RADIUS_SIZE_MIN, MOB_RADIUS_SIZE_MAX)
        self.org_image = pygame.transform.scale(Mod_img,(size,size))
        self.image = self.org_image.copy()
        self.rect = self.image.get_rect()
        

        self.rot = 0
        self.rot_speed = random.randrange(-MOB_ROTATE_SPEED, +MOB_ROTATE_SPEED)

        self.last_update = pygame.time.get_ticks()

        
        self.radius = int(self.rect.width/2) 
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(MOB_ORG_POS_MIN_Y,MOB_ORG_POS_MAX_Y)
        self.speedy = random.randrange(MOB_SPEED_Y_MIN, MOB_SPEED_Y_MAX)
        self.speedx = random.randrange(-MOB_SPEED_X, MOB_SPEED_X)
     
        
        #加入sprite group 的功能放在各个sprite初始化模块中
        game.all_sprites_group.add(self)
        game.all_mobs_group.add(self)

    
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > MOB_ROTATE_TICK:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.org_image, self.rot)
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            
            
    def update(self):
    
        self.rotate()
        
        self.rect.y += self.speedy
        
        self.rect.x += self.speedx
        
        if self.rect.top > HEIGHT+10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(MOB_ORG_POS_MIN_Y,MOB_ORG_POS_MAX_Y)
            self.speedy = random.randrange(MOB_SPEED_Y_MIN, MOB_SPEED_Y_MAX)
    

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y,game): 
        pygame.sprite.Sprite.__init__(self)
        self.game_handle = game
        
        butllet_img = self.game_handle.bullet_img_group[0]
        self.image = pygame.transform.scale(butllet_img,(BULLET_SIZE_W,BULLET_SIZE_H))
        self.rect = self.image.get_rect()
      
        self.rect.bottom = y
        self.rect.centerx = x
        
        self.speedy = -BULLET_SPEED
        game.all_sprites_group.add(self)
        game.all_bulletes_group.add(self)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

