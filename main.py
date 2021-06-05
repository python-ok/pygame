import pygame
import random

WIDTH = 360
HEIGHT = 480
FPS = 30

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
running = True


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        
    def update(self):
        self.rect.x += 5
        if self.rect.x >= WIDTH:
            self.rect.x = 0
    

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
            
    all_sprites.update()
    
    screen.fill(BLACK)   
    all_sprites.draw(screen)
 
    pygame.display.flip()
    
    clock.tick(FPS)
    

pygame.quit()

