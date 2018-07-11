import pygame as pg
import traceback
#import random as rnd
from os import path

import settings as st
import sprites as spr


class Game():
    def __init__(self):
        # initialise game window etc.
        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.mixer.init()
        pg.init()

        self.screen = pg.display.set_mode((st.WIDTH, st.HEIGHT))
        pg.display.set_caption(st.TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(st.FONT_NAME)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        
        self.room_images = spr.img_list_from_strip(path.join(img_folder, 
                                            'rooms_strip_opaque2.png'), 
                                             16, 16, 0, 18)
        self.room_image_dict = {    
                'NSWE': self.room_images[0],
                'NS': self.room_images[1],
                'WE': self.room_images[2],
                'N': self.room_images[3],
                'S': self.room_images[4],
                'W': self.room_images[5],
                'E': self.room_images[6],
                'WS': self.room_images[7],
                'ES': self.room_images[8],
                'NE': self.room_images[9],
                'NW': self.room_images[10],
                'NWE': self.room_images[13],
                'SWE': self.room_images[14],
                'NSE': self.room_images[15],
                'NSW': self.room_images[16]
                }

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.dungeon = spr.Dungeon(self, st.DUNGEON_SIZE)
        self.all_sprites.add(self.dungeon)
        
        self.run()


    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.clock.tick(st.FPS)
            self.events()
            self.update()
            self.draw()


    def update(self):
        # game loop update
        self.all_sprites.update()
        pass


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


    def draw(self):
        
        pg.display.flip()


g = Game()
try:
    while g.running:
        g.new()
except Exception:
    traceback.print_exc()
    pg.quit()

pg.quit()
