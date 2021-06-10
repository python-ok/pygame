import pygame
import random
import os
from settings import *

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
     
    
    def update(self):
    
        
        self.speedx = 0
                
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx += -PLANE_SPEED
        if keystate[pygame.K_RIGHT]:
            self.speedx += +PLANE_SPEED
            
        self.rect.x += self.speedx
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, self.game_handle)
        self.game_handle.all_sprites_group.add(bullet)
        self.game_handle.all_bulletes_group.add(bullet)
        
        #播放音效
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

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

