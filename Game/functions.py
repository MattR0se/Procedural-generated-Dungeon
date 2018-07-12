import pygame as pg
import numpy as np
from os import path
import traceback

import settings as st
import sprites as spr


def collideMove(self, others):
    #move horizontally based on direction and speed
    self.rect.x += self.dir[0] * self.vel
    block_hit_list = pg.sprite.spritecollide(self, others, False)
    for block in block_hit_list:
        #if we hit something, reset our position so both hitboxes 
        #touch on either side
        if self.dir[0] == 1:
            self.rect.right = block.rect.left
        else:
            self.rect.left = block.rect.right
    #move vertically based on direction and speed
    self.rect.y += self.dir[1] * self.vel
    block_hit_list = pg.sprite.spritecollide(self, others, False)
    for block in block_hit_list:
        #if we hit something, reset our position so both hitboxes 
        #touch on the top/bottom
        if self.dir[1] == 1:
            self.rect.bottom = block.rect.top
        else:
            self.rect.top = block.rect.bottom


def screenWrap(player, dungeon):
    #checks if the player goes outside the screen
    #if they do, set their new position based on where they went
    index = dungeon.room_index
    
    new_pos = np.copy(player.rect.topleft)
    if player.rect.right < 0:
        new_pos[0]  = st.WIDTH - player.bb_width
        index[1] -= 1
    if player.rect.left > st.WIDTH:
        new_pos[0] = - player.bb_width
        index[1] += 1
    if player.rect.bottom < 0:
        new_pos[1] = st.HEIGHT
        index[0] -= 1
    if player.rect.top > st.HEIGHT:
        new_pos[1] = - player.bb_height 
        index[0] += 1
    try:
        return dungeon.room_map[index[0]][index[1]], new_pos
    except Exception:
        traceback.print_exc()
        #if there is no matching room, return some default value
        return -1, ([100,100])


def transitRoom(game, group, dungeon, room_number):
    #deletes all instances in the group and adds new ones
    #based on the room data matching the given room number
    
    for i in range(len(dungeon.room_map)):
        for j in range(len(dungeon.room_map)):
            if dungeon.room_map[i][j] == room_number:
                index = [i, j]
                dungeon.room_index = index
    data = dungeon.rooms[index[0]][index[1]].layout
    try:
        group.empty()
        for i in range(len(data)):
            for j in range(len(data[i])):
                if data[i][j] == 1:
                    group.add(spr.Wall(game, (j * st.TILESIZE, i * st.TILESIZE), 
                                        (st.TILESIZE, st.TILESIZE)))
        return group
    except Exception:
        #if something goes wrong, return an empty group
        traceback.print_exc()
        return group
    

def img_list_from_strip(filename, width, height, startpos, number):
    directory = path.dirname(__file__)
    file = path.join(directory, filename)
    try:
        img = pg.image.load(file).convert_alpha()
    except Exception:
        traceback.print_exc()
        return
    img_set = []
    for i in range(startpos, (startpos + number)):
        rect = ((i * width, 0), (width, height))
        subimg = pg.transform.scale(img.subsurface(rect), 
                                    (st.TILESIZE, st.TILESIZE))
        img_set.append(subimg)
    return img_set


def tileImageScale(filename, size_w=st.TILESIZE, size_h=st.TILESIZE, scale=1, 
                   alpha=False):
    directory = path.dirname(__file__)
    file = path.join(directory, filename)
    try:
        img = pg.image.load(file).convert()
        if alpha:
            color = img.get_at((0,0))
            img.set_colorkey(color)
    except Exception:
        traceback.print_exc()
        return
    
    width, height = img.get_width(), img.get_height()
    tiles_hor = width // size_w
    tiles_vert = height // size_h
    wh_ratio = size_w / size_h
    tileset = []
    for i in range(tiles_vert):
        for j in range(tiles_hor):
            rect = (size_w * j, size_h * i, size_w, size_h)
            subimg = img.subsurface(rect)
            tileset.append(pg.transform.scale(
                    subimg, (int(st.TILESIZE * scale * wh_ratio), 
                             int(st.TILESIZE * scale))))
    return tileset


def tileRoom(game, tileset, index):
    image = pg.Surface((st.WIDTH, st.HEIGHT))
    data = game.dungeon.rooms[index[0]][index[1]].tiles
    for i in range(len(data)):
        for j in range(len(data[i])):
            x = j * st.TILESIZE
            y = i * st.TILESIZE
            try:
                image.blit(tileset[data[i][j]], (x, y))
            except Exception:
                traceback.print_exc()
    return image


def compare(seq, string):
    # checks if string contains exactly the letters in seq, but the order 
    # is not relevant
    if len(seq) != len(string):
        return False

    for s in string:
        #print(s)
        if s not in seq:
            return False
    return True