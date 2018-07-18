import pygame as pg
import traceback
#from os import path
from random import choice

import settings as st
import sprites as spr
import functions as fn
import rooms

vec = pg.math.Vector2

class Game():
    def __init__(self):
        # initialise game window etc.
        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.mixer.init()
        pg.init()

        self.screen = pg.display.set_mode((st.WIDTH, st.HEIGHT))
        
        self.clock = pg.time.Clock()
        self.running = True
        
        # booleans for drawing the hit rects and other debug stuff
        self.draw_debug = False
        self.slowmotion = False
        
        self.load_data()


    def load_data(self):      
        self.room_images = fn.img_list_from_strip('rooms_strip_4.png', 
                                                  16, 16, 0, 18)
        self.room_image_dict = {
                'NSWE': self.room_images[0],
                'NS': self.room_images[1],
                'WE': self.room_images[2],
                'N': self.room_images[3],
                'S': self.room_images[4],
                'W': self.room_images[5],
                'E': self.room_images[6],
                'SW': self.room_images[7],
                'SE': self.room_images[8],
                'NE': self.room_images[9],
                'NW': self.room_images[10],
                'NWE': self.room_images[13],
                'SWE': self.room_images[14],
                'NSE': self.room_images[15],
                'NSW': self.room_images[16]
                }
        
        self.tileset_names = ['tileset.png', 'tileset_sand.png', 
                              'tileset_green.png','tileset_red.png']
        
        self.tileset_list = [fn.tileImageScale(tileset, 16, 16,
                                scale=1) for tileset in self.tileset_names]
        
        
    def new(self):
        # start a new game
        # initialise sprite groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        
        # instantiate objects
        # MEMO: GET RID OF THIS ROOM NUMBER AND USE THE INDEX INSTEAD!
        self.dungeon = rooms.Dungeon(self, st.DUNGEON_SIZE)
        self.room_number = self.dungeon.room_map[self.dungeon.room_index[0]][
                                                 self.dungeon.room_index[1]]
        
        # pick a random tileset from all available tilesets
        self.tileset = choice(self.tileset_list)
        # create a background image from the tileset for the current room
        self.background = fn.tileRoom(self, self.tileset, self.dungeon.room_index)
        
        # spawn the player in the middle of the screen/room
        self.player = spr.Player(self, (st.WIDTH // 2, st.HEIGHT // 2))
        # spawn the wall objects (invisible)
        self.walls = fn.transitRoom(self, self.walls, self.dungeon, 
                                    self.room_number)
        
        self.run()


    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            if self.slowmotion:
                self.clock.tick(5)
            else:
                self.clock.tick(st.FPS)
            self.events()
            self.update()
            self.draw()


    def update(self):
        #pg.display.set_caption(str(self.player.hit_rect.center))
        pg.display.set_caption(st.TITLE)
        if self.slowmotion:
            pg.display.set_caption('slowmotion')
        
        # game loop update
        self.player.update(self.walls)
        # check for room transitions on screen exit (every frame)
        direction, new_room, new_pos = fn.screenWrap(self.player, self.dungeon)
        
        if new_room != self.room_number:
            self.room_number = new_room
            self.RoomTransition(new_pos, direction)


    def events(self):
        # game loop events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.screen.fill((0, 0, 0))
                    self.new()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_s:
                    self.slowmotion = not self.slowmotion


    def draw(self):
        self.screen.blit(self.background, (0, 0))

        self.player.draw()

        if self.dungeon.done:
            self.dungeon.blitRooms()

        if self.draw_debug:
            pg.draw.rect(self.screen, st.RED, self.player.hit_rect, 1)
            for wall in self.walls:
                pg.draw.rect(self.screen, st.RED, wall.rect, 1)  
                          
        pg.display.flip()
        
    
    def RoomTransition(self, new_pos, direction):
        # store the old background image temporarily
        old_background = self.background
        # build the new room
        self.background = fn.tileRoom(self, self.tileset, 
                                      self.dungeon.room_index)
        
        # move the player to the other side of the screen
        self.player.pos = new_pos
        self.player.rect.center = self.player.pos
        self.player.hit_rect.bottom = self.player.rect.bottom
        
        # scroll the new and old background
        # start positions for the new bg are based on the direction the
        # player is moving
        start_positions = {
                          'UP': vec(0, - st.HEIGHT),  
                          'DOWN': vec(0, st.HEIGHT),
                          'LEFT': vec(- st.WIDTH, 0),
                          'RIGHT': vec(st.WIDTH, 0)
                          }
        
        pos = start_positions[direction]
        # pos2 is the old bg's position that gets pushed out of the screen
        pos2 = vec(0, 0)
        
        while pos != (0, 0):
            # moves the 2 room backrounds until the new background is at (0,0)
            # the pos has to be restrained to prevent moving past (0,0) and 
            # stay forever in the loop
            scroll_speed = st.SCROLLSPEED
            if direction == 'UP':
                pos.y += scroll_speed
                pos2.y += scroll_speed
                pos.y = min(0, pos.y)
            elif direction == 'DOWN':
                pos.y -= scroll_speed
                pos2.y -= scroll_speed
                pos.y = max(0, pos.y)
            elif direction == 'LEFT':
                pos.x += scroll_speed
                pos2.x += scroll_speed
                pos.x = min(0, pos.x)
            elif direction == 'RIGHT':
                pos.x -= scroll_speed
                pos2.x -= scroll_speed
                pos.x = max(0, pos.x)
            
            self.screen.blit(self.background, pos)
            self.screen.blit(old_background, pos2)
            self.dungeon.blitRooms()
            #self.player.draw()

            pg.display.flip()
        
        # put wall objects in the room after transition
        self.walls = fn.transitRoom(self, self.walls, self.dungeon, 
                                    self.room_number)




g = Game()
try:
    while g.running:
        g.new()
except Exception:
    traceback.print_exc()
    pg.quit()

pg.quit()
