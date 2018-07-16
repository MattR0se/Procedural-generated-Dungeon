import pygame as pg
import numpy as np

import functions as fn
import settings as st

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game,  pos):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.dir = np.array([0, 0])
        self.vel = 2 * st.GLOBAL_SCALE
        self.bb_width = st.TILESIZE - int(st.TILESIZE * 0.2)
        self.bb_height = st.TILESIZE - int(st.TILESIZE * 0.2)
        self.rect = pg.Rect(pos, (self.bb_width, self.bb_height))

        self.color = (100, 100, 255)
        self.image = pg.Surface([self.bb_width, self.bb_height])
        self.image.fill(self.color)
    
    
    def update(self, others):
        pressed = pg.key.get_pressed()
        move_up = pressed[pg.K_UP]
        move_down = pressed[pg.K_DOWN]
        move_left = pressed[pg.K_LEFT]
        move_right = pressed[pg.K_RIGHT]
        self.dir = np.array([move_right - move_left, move_down - move_up])
        fn.collideMove(self, others)
        
        
    def draw(self):
        self.game.screen.blit(self.image, self.rect.topleft)
 
    
        
class Wall(pg.sprite.Sprite):
    def __init__(self, game, pos, size):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.dir = np.array([0, 0])
        self.vel = 0
        self.bb_width, self.bb_height = size
        self.rect = pg.Rect(pos, (self.bb_width, self.bb_height))

        self.color = (255, 100, 100)
        self.image = pg.Surface([self.bb_width, self.bb_height])
        self.image.fill(self.color)
    
    
    def draw(self):
        self.game.screen.blit(self.image, self.rect.topleft)