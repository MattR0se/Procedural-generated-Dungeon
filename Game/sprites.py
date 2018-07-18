import pygame as pg

import functions as fn
import settings as st

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game,  pos):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        # images for animation
        self.image_strip = fn.img_list_from_strip('knight_strip.png', 16, 16,
                                                    0, 8)
        self.walk_frames_l = [self.image_strip[6], self.image_strip[7]]
        self.walk_frames_r = [self.image_strip[2], self.image_strip[3]]
        self.walk_frames_u = [self.image_strip[4], self.image_strip[5]]
        self.walk_frames_d = [self.image_strip[0], self.image_strip[1]]
        self.image = self.walk_frames_d[0]
        
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.hit_rect = st.PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)      
        self.dir = vec(0, 0)
        self.walking = False
        self.last_update = 0
        self.current_frame = 0
        self.vel = st.PLAYER_SPEED
        
        
    def get_keys(self):
        self.vel = vec(0, 0)
        self.dir = vec(0, 0)
        
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -st.PLAYER_SPEED
            self.dir.x = -1
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = st.PLAYER_SPEED
            self.dir.x = 1
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -st.PLAYER_SPEED
            self.dir.y = -1
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = st.PLAYER_SPEED
            self.dir.y = 1
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel.x *= 0.7071
            self.vel.y *= 0.7071     
    
    
    def update(self, others):
        self.get_keys()
        self.animate()
        
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel
        self.hit_rect.centerx = self.pos.x
        fn.collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        fn.collide_with_walls(self, self.game.walls, 'y')
        
        # position the hitrect at the bottom of the image
        self.rect.midbottom = self.hit_rect.midbottom
        
        
    def draw(self):
        self.game.screen.blit(self.image, self.rect.topleft)
        

    def animate(self):
        now = pg.time.get_ticks()
        
        if self.vel.length_squared() != 0:
            self.walking = True
        else:
            self.walking = False

        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(
                                      self.walk_frames_l)
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                elif self.vel.x < 0:
                    self.image = self.walk_frames_l[self.current_frame]
                if self.vel.y > 0:
                    self.image = self.walk_frames_d[self.current_frame]
                elif self.vel.y < 0:
                    self.image = self.walk_frames_u[self.current_frame]


        
class Wall(pg.sprite.Sprite):
    def __init__(self, game, pos, size):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.bb_width, self.bb_height = size
        self.rect = pg.Rect(pos, (self.bb_width, self.bb_height))
   
    
    def draw(self):
        self.game.screen.blit(self.image, self.rect.topleft)