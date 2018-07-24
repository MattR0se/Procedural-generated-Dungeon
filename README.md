# Procedural Dungeon Generation - room(s) for improvement

This is my first attempt to write an algorithm for a procedural generated dungeon. Now, procedural in this context just means "random with rules", and the rules are not nearly as sophisticated in a game like Minecraft or Terraria, for example.

My goal was to put some evenly sized rooms into a fixed 2D grid, and they should all be connected to each other. I put this code together in roughly a week, and build it on top of an older game "engine" of mine, so some things are still a bit convoluted and need to be refactored at some point, but this was only done to test if the algorithm translates to an actual game.

I made two videos to show how this code looks right now. The first is a visualisation of the actual dungeon generation, the second one is the rudimentary "game" that puts some crudely drawn tiles in each room and lets you traverse the dungeon. Oh, and it also has a mini map, which is pretty much the same as the first example, only scaled to be in the corner of the screen.

https://youtu.be/rGIoYSnXh-w

https://youtu.be/TvQE_tyT9_8

Also, here are the codes, one for the visualisation example and one for the game:

https://github.com/MattR0se/Procedural-generated-Dungeon/tree/master/Demo

https://github.com/MattR0se/Procedural-generated-Dungeon/tree/master/Game

Since the code is pretty huge by now, and my in-code comments are probably not that helpful, I will now go over my process of building this system. The code is found in the second link.

I started with the Room and Dungeon classes, which are in the rooms.py file. A Dungeon is pretty much a collection of rooms. It stores their position and their other attributs (doors, type). The Dungeon is what is randomized every time at the beginning of the game (this is, when you call the build() method). The Room objects themselves are containers for the layout (objects, tiles) of each room. Currently, this is just the data where the doors are, and everything else is the same, but I will add more variety in the future.


### The Dungeon

As for the Dungeon object, it it initialized with a size (that restrains how big your Dungeon can possibly be and what shape it has), a room pool (every possible room object), and a 'rooms' that is a 2D grid for the rooms, initially with only 'None' in it. Technically, this is rather a "list of lists", but you could also see it as a matrix. But I will refer to it as "grid" from now on.

```python
class Dungeon():
    def __init__(self, game, size):
        start = datetime.now()
        self.size = vec(size)
        self.game = game
        # variables for animation
        self.last_update = 0
        self.current_frame = 0
                  
        w = int(self.size.x)
        h = int(self.size.y)
        # empty dungeon
        self.rooms = [[None for i in range(w)] for j in range(h)]

        # starting room
        self.start = [h // 2, w // 2]
        self.rooms[self.start[0]][self.start[1]] = Room(self.game, 'NSWE', 
                                                        'start')
        self.room_index = self.start
        
        self.done = False
        
        self.build()
```

Then, the starting room is created. In this example, it is a room with 4 exits and located in the middle of the grid, but it could also have any given position and number of exists. I believe this is how it's done in The Binding of Isaac, whereas in Zelda, the entrance would be at the bottom of the dungeon's grid.

```python
# starting room
self.start = [h // 2, w // 2]
self.rooms[self.start[0]][self.start[1]] = Room(self.game, 'NSWE', 
                                                'start')
self.room_index = self.start
```
There is also the 'room_index', which stores the grid index of the room the player is currently in. 

Finally, 'build()' is called. Now, you could call this function from the Game() object instead if you wanted to instantiate the Dungeon only once but build a different maze multiple times. For example if you wanted to keep certain attributes the same, but randomize every time the player enters the dungeon. That's pretty much up to you.
self.done is just a boolean that checks if no room was placed during a loop, and if so, stays True. That's how I know the dungeon is finished.

```python
self.done = False
        
self.build()
```
Now, the build method is where the magic happens, so to speak. There is a while loop that goes through the rooms grid and checks for every room's doors and if there is empty space and if so, places a random room.
```python
 def build(self):  
        while self.done == False:
            self.done = True
            for i in range(1, len(self.rooms) - 1):
                for j in range(1, len(self.rooms[i]) - 1):
                    room = self.rooms[i][j]
                    if room:
                        if 'N' in room.doors and self.rooms[i - 1][j] == None:
                            if i == 1:
                                self.rooms[i - 1][j] = Room(self.game, 'S')
                            else:
                                # pick random door constellation
                                rng = choice(st.ROOMS['N'])
                                
                                # prevent one-sided doors
                                if 'N' in rng and self.rooms[i - 2][j]:
                                    rng = rng.replace('N', '')
                                if 'W' in rng and self.rooms[i - 1][j - 1]:
                                    rng = rng.replace('W', '')
                                if 'E' in rng and self.rooms[i - 1][j + 1]: 
                                    rng = rng.replace('E', '')
      
                                self.rooms[i - 1][j] = Room(self.game, rng)
                                
                            self.done = False
                        
                        if 'W' in room.doors and self.rooms[i][j - 1] == None:
                            if j == 1:
                                self.rooms[i][j - 1] = Room(self.game, 'E')
                            else:
                                rng = choice(st.ROOMS['W'])
                                
                                if 'N' in rng and self.rooms[i - 1][j - 1]:
                                    rng = rng.replace('N', '')
                                if 'W' in rng and self.rooms[i][j - 2]: 
                                    rng = rng.replace('W', '')
                                if 'S' in rng and self.rooms[i + 1][j - 1]: 
                                    rng = rng.replace('S', '')
                                
                                self.rooms[i][j - 1] = Room(self.game, rng)
                                
                            self.done = False
                        
                        if 'E' in room.doors and self.rooms[i][j + 1] == None:
                            if j == len(self.rooms) - 2:
                                 self.rooms[i][j + 1] = Room(self.game, 'W')
                            else:
                                rng = choice(st.ROOMS['E'])
                                
                                if 'N' in rng and self.rooms[i - 1][j + 1]:
                                    rng = rng.replace('N', '')
                                if 'E' in rng and self.rooms[i][j + 2]: 
                                    rng = rng.replace('E', '')
                                if 'S' in rng and self.rooms[i + 1][j + 1]: 
                                    rng = rng.replace('S', '')
                                
                                self.rooms[i][j + 1] = Room(self.game, rng)
                                
                            self.done = False                              
                        
                        if 'S' in room.doors and self.rooms[i + 1][j] == None:
                            if i == len(self.rooms) - 2:
                                pass
                                self.rooms[i + 1][j] = Room(self.game, 'N')
                            else:
                                rng = choice(st.ROOMS['S'])
                                
                                if 'W' in rng and self.rooms[i + 1][j - 1]:
                                    rng = rng.replace('W', '')
                                if 'E' in rng and self.rooms[i + 1][j + 1]: 
                                    rng = rng.replace('E', '')
                                if 'S' in rng and self.rooms[i + 2][j]: 
                                    rng = rng.replace('S', '')
                                
                                self.rooms[i + 1][j] = Room(self.game, rng)
                                
                            self.done = False

        self.closeDoors()
        self.floodFill()```
A little bit more in-depth: The code loops through each item in the rooms grid, except for the first and last rows and columns. Remember that there are only 'None's in the beginning, except for the starting room. So if the loop reaches this room, the 'if room:' is True because 'None' defaults to False.
```python
while self.done == False:
    self.done = True
    for i in range(1, len(self.rooms) - 1):
        for j in range(1, len(self.rooms[i]) - 1):
            room = self.rooms[i][j]
            if room: # if room is not None
```
Now, there are a bunch of if-clauses that check if that room.doors has a certain direction in it and also if there is a room next to it in that direction. For example, if room.doors has 'N' in it, it has to check north of that room. That would be rooms[i-1][j] because remember, the vertical component (rows) comes first in the grid (Imagine this as rooms[y][x]). If there is no room, there are two options: If i == 1, it means that the next room would be placed at the border, so no room with an 'N' door should be placed there. For this example, I chose only to place the 'S' room, but other possible rooms would be 'SE', 'SW' and 'SWE'.
```python
if 'N' in room.doors and self.rooms[i - 1][j] == None:
	if i == 1:
	self.rooms[i - 1][j] = Room(self.game, 'S')
                 else:
                  # pick random door constellation
	 rng = choice(st.ROOMS['N'])
```
Otherwise, it the Dungeon picks a room constellation randomly from a list. Now, this is the important part that defines the overall structure of your final dungeon. See that currently, for the 'N' direction there are four items 'NS' in it, three 'S' and one of each of the other possible choices. So, it is four times as likely to pick the 'NS' and three times as likely to pick 'S' than the other constellations. Here you can play with the list and see what happens. For example, if you put even more 'NS' room in there, the branches become more streched. If you have only one 'NS' in there, the rooms will somewhat clump together. If you add more 'S', the dungeon gets smaller. This is determined in the settings.py:
```python
ROOMS = {
        'N': ['NS', 'NS', 'NS', 'NS', 'S', 'S', 'S', 'WS', 'ES', 'SWE', 'NSW', 'NSE'],
        'W': ['WE', 'WE', 'WE', 'WE', 'E', 'E', 'E', 'ES', 'EN', 'SWE', 'NSE', 'NWE'],
        'E': ['WE', 'WE', 'WE', 'WE', 'W', 'W', 'W', 'WS', 'WN', 'SWE', 'NSW', 'NWE'],
        'S': ['NS', 'NS', 'NS', 'NS', 'N', 'N', 'N', 'WN', 'EN', 'NSE', 'NSW', 'NWE']
        }
```
This is done for all 4 directions. You could also make totally different room_pools for each direction, if you want the dungeon to branch out more to one direction, for example. This is really up to you.

Now, before adding the Room object to the grid, a (still not perfect) check is made to prevent a door if there is already another room next to it. 
```python
 # prevent one-sided doors
    if 'N' in rng and self.rooms[i - 2][j]:
        rng = rng.replace('N', '')
    if 'W' in rng and self.rooms[i - 1][j - 1]:
        rng = rng.replace('W', '')
    if 'E' in rng and self.rooms[i - 1][j + 1]: 
        rng = rng.replace('E', '')

    self.rooms[i - 1][j] = Room(self.game, rng)

self.done = False
```
These if-statements go through each door in the new Room (that isn't the door it came from) and look one place in the grid further to see if there is a room. If so, delete the door from the doors string (by replacing it with ''). Now, you could change this and also check if the adjacent room has a corresponding door and if so, leave everything as is. This could potentially lead to circular paths in your Dungeon, and if that's what you want, go ahead.

Lastly, self.done is set to False after it was set to True at the beginning of the while loop. The idea here is that the dungeon building is expected to be done when no new rooms were built during an iteration.

At the end of self.build(), two functions are called: closeDoors() and floodFill(). 
```python
def closeDoors(self):
        for i in range(len(self.rooms)):
            for j in range(len(self.rooms[i])):
                room = self.rooms[i][j]
                if room:
                    if 'N' in room.doors and self.rooms[i - 1][j]:
                        if 'S' not in self.rooms[i - 1][j].doors:
                            room.doors = room.doors.replace('N', '')
  
                    if 'S' in room.doors and self.rooms[i + 1][j]:
                        if 'N' not in self.rooms[i + 1][j].doors:
                            room.doors = room.doors.replace('S', '')
                    
                    if 'W' in room.doors and self.rooms[i][j - 1]:
                        if 'E' not in self.rooms[i][j - 1].doors:
                            room.doors = room.doors.replace('W', '')
                            
                    if 'E' in room.doors and self.rooms[i][j + 1]:
                        if 'W' not in self.rooms[i][j + 1].doors:
                            room.doors = room.doors.replace('E', '')
                    
                    # re-build the rooms after changes
                    room.build()
                    # set the inner layout of the room
                    room.buildInterior()

```
This loops through the grid and if a room's door has no corresponding door in the next room, deletes it from the string. Now, I imagine this could have already been done in the build() method, but this works fine and right now, I don't really care about performance since this whole process takes around 10ms on my computer (which is really old by the way). 
At the end, the room needs to be rebuild because its doors changed. More about that later.

Next, I wrote a litte flood-fill alorithm, which is not used right now. What it does is that it assignes a value to each room based on how far the room is from the start. 
```python
def floodFill(self):
        cycle = 0
        starting_room = self.rooms[self.start[0]][self.start[1]]
        starting_room.dist = 0
        done = False
        while not done:
            done = True
            for i in range(1, len(self.rooms) - 1):
                for j in range(1, len(self.rooms[i]) - 1):
                    room = self.rooms[i][j]
                    
                    if room and room.dist == cycle:
                        if 'N' in room.doors and self.rooms[i - 1][j]:
                            if self.rooms[i - 1][j].dist == -1:
                                self.rooms[i - 1][j].dist = cycle + 1
                                done = False
                            
                        if 'S' in room.doors and self.rooms[i + 1][j]:
                            if self.rooms[i + 1][j].dist == -1:
                                self.rooms[i + 1][j].dist = cycle + 1
                                done = False
                        
                        if 'W' in room.doors and self.rooms[i][j - 1]:
                            if self.rooms[i][j - 1].dist == -1:
                                self.rooms[i][j - 1].dist = cycle + 1
                                done = False
                        
                        if 'E' in room.doors and self.rooms[i][j + 1]:
                            if self.rooms[i][j + 1].dist == -1:
                                self.rooms[i][j + 1].dist = cycle + 1
                                done = False
                        
            cycle += 1
```
Each room starts with dist == -1 when it is instantiated. First, the starting room gets the value of 0. Then, this code loops through each room and looks for the rooms with a dist equal to the current cycle. In the first iteration, this is 0, so it finds the starting room and assigns each adjacent room a 1. In the next iteration, it finds all the rooms with dist == 1 and assigns a 2 if they have a -1, aka not been visited yet. This repeats until no room gets assigned a new dist. 
This can be useful to asses a Dungeon's structure, for example if you want the max dist from the start a certain value. I will also use this to assign the boss room and also look where the player can and can't go if there are locked doors. 

The last method blitRooms() is just a visual representation of the generated dungeon and serves as a mini map. If you want to know more about that, leave a comment.
```python
def blitRooms(self):
    # blit a mini-map image onto the screen

    # room image size
    size = (int(3.5 * st.GLOBAL_SCALE), int(3.5 * st.GLOBAL_SCALE / 2))

    # mini map size
    w = self.size.x * size[0]
    h = st.GUI_HEIGHT - 2 * st.GUI_MARGIN
    margin = st.GUI_MARGIN

    self.map_img = pg.Surface((w, h), flags=pg.SRCALPHA)
    self.map_img.fill(st.BLACK)

    for i in range(len(self.rooms)):
        for j in range(len(self.rooms[i])):
            room = self.rooms[i][j]
            pos = (j * (w / self.size.x), i * (h / self.size.y))
            if room and room.visited:
                self.map_img.blit(pg.transform.scale(room.image,
                                  size), pos)
                if room.type == 'start':
                    # draw a square representing the starting room
                    self.map_img.blit(pg.transform.scale(
                            self.game.room_images[12], size), pos)
            else:
                self.map_img.blit(pg.transform.scale(
                        self.game.room_images[17], size), pos)

    # animated red square representing the player
    now = pg.time.get_ticks()
    pos2 = (self.room_index[1] * (w / self.size.x), 
            self.room_index[0] * (h / self.size.y))
    player_imgs = [pg.transform.scale(self.game.room_images[11], size),
                   pg.transform.scale(self.game.room_images[17], size)]

    if now - self.last_update > 500:
            self.last_update = now
            # change the image
            self.current_frame = (self.current_frame + 1) % len(player_imgs)
    self.map_img.blit(player_imgs[self.current_frame], pos2)

     self.game.inventory.image.blit(self.map_img, 
                                   (st.WIDTH - w - margin, 
                                    st.HEIGHT - st.GUI_HEIGHT + margin))
```

### The Room

Every Room is initialized with a string called 'doors', which is any combination of 'NSWE', the 4 cardinal directions. It also has a type, but at this point there are only 'default' and 'start', but I could see adding 'boss', 'merchant' and the likes.
```python
class Room():
    def __init__(self, game, doors, type_='default'):
        self.game = game
        self.doors = doors
        self.type = type_
        self.w = st.WIDTH // st.TILESIZE
        self.h = (st.HEIGHT - st.GUI_HEIGHT) // st.TILESIZE
        
        self.visited = True
        self.dist = -1
        
        self.build()
```
self.visited is a check if the player has been already in that room.
After that, I set the room's image. Right now, this is only used for a mini map in the corner of the screen.

```python
def build(self):       
    for key in self.game.room_image_dict:
        if fn.compare(self.doors, key):
            self.image = self.game.room_image_dict[key]

    self.tileRoom()
```

This looks complicated, but what the compare() method does is compare two strings regardless of the order of their letters. For example, compare('NWS', 'SWN') would return True. This way I don't have to worry about the order of the doors string. 

The Room has one method called 'tileRoom()'. Here, the layout (which stores information where the sprites are beinig placed) is created as a grid. Right now, the first and last column are all 1s, which stand for wall tiles, and the floor are 0s. Notice that the outer loop is for the columns and the inner loop is for the rows, which is something I always confuse and it is a point where errors happen frequently, especially if you combine this with (x, y) coordinates and vectors, where it is the other way round...
```python
self.layout = []
for i in range(self.h):
    self.layout.append([])
    if i == 0 :
        for j in range(self.w):
            self.layout[i].append(1)
        elif i == self.h - 1:
            for j in range(self.w):
                self.layout[i].append(1)           
        else:
            for j in range(self.w):
                if j == 0:
                    self.layout[i].append(1)
                elif j == self.w - 1:    
                    self.layout[i].append(1)
                else:
                    # in the room
                        self.layout[i].append(0) 
```

In the final code, there is also a grid for the tile data, but since this depends on the final game and how your rooms should look like, I left this out for clarity reasons.

After the walls, the doors are put into the room's grid. I look for the 4 letters that represent the directions and if they are in the room's doors variable, a door is put in that particular spot, which here are just two 0s that determine that np wall should be placed there. 
```python
# north
if 'N' in self.doors:
    self.layout[0][door_w] = 0
    self.layout[0][door_w - 1] = 0
    
# south
if 'S' in self.doors:
    self.layout[self.h - 1][door_w] = 0
    self.layout[self.h - 1][door_w - 1] = 0

# west
if 'W' in self.doors:
    self.layout[door_h][0] = 0
    self.layout[door_h - 1][0] = 0

# east
if 'E' in self.doors:
    self.layout[door_h][self.w - 1] = 0
    self.layout[door_h - 1][self.w - 1] = 0
```
And that's it for now with the Room object.


I also won't go much into detail about the sprites.py, functions.py and settings.py. In sprites, there are just the player and the wall sprite and all the player does is move and check for collisions with the wall sprite. Aside from the collision, functions also contains the room transition (which is a mess tbh) and some methods for loading images and make a background out of a tileset. Again, feel free to ask about them in the comments.

The settings contain some variables regarding the screen and tile size. I made it so that you can change the GLOBAL_SCALE variable and everything in the game keeps its proportions.

### The Game

Alright, so it all comes together in the main.py (as you would probably expect). First, I load all the images for the rooms (which are used for the mini map) and different tilesets that have a similar layout, but different color, from which the game picks a random one. 
```python
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
```
In new(), the Dungeon, the background and the sprites are put into the game. 
```python
def new(self):
    # start a new game
    # initialise sprite groups
    self.all_sprites = pg.sprite.Group()
    self.walls = pg.sprite.Group()
    self.gui = pg.sprite.Group()

    # instantiate dungeon
    self.dungeon = rooms.Dungeon(self, st.DUNGEON_SIZE)

    # pick a random tileset from all available tilesets
    self.tileset = choice(self.tileset_list)
    # create a background image from the tileset for the current room
    self.background = fn.tileRoom(self, self.tileset, self.dungeon.room_index)

    # spawn the player in the middle of the screen/room
    self.player = spr.Player(self, (st.WIDTH // 2, st.HEIGHT // 2))
    # spawn the wall objects (invisible)
    self.walls = fn.transitRoom(self, self.walls, self.dungeon)

    self.inventory = spr.Inventory(self)

    self.run()
```
The transitioning between rooms happens in the update() method. 

```python
def update(self):        
    # game loop update
    self.player.update(self.walls)

    # check for room transitions on screen exit (every frame)
    direction, new_room, new_pos = fn.screenWrap(self.player, self.dungeon)

    if new_room != self.dungeon.room_index:
        self.dungeon.room_index = new_room
        self.RoomTransition(new_pos, direction)
```

screenWrap checks if the player goes out of bounds and then determines which room is next:
```python
def screenWrap(player, dungeon):
    #checks if the player goes outside the screen
    #if they do, set their new position based on where they went
    index = list(dungeon.room_index)
    direction = ''
    new_pos = vec(player.hit_rect.center)

    if player.rect.left < 0:
        direction = 'LEFT'
        new_pos.x  = st.WIDTH - player.rect.width
        index[1] -= 1
    if player.rect.right > st.WIDTH:
        direction = 'RIGHT'
        new_pos.x = player.rect.width
        index[1] += 1
    if player.rect.top < st.GUI_HEIGHT:
        direction = 'UP'
        new_pos.y = st.HEIGHT - player.rect.height
        index[0] -= 1
    if player.rect.bottom > st.HEIGHT:
        direction = 'DOWN'
        new_pos.y = player.rect.height + st.GUI_HEIGHT
        index[0] += 1

    try:
        return direction, index, new_pos
    except Exception:
        traceback.print_exc()
```
This is really basic stuff so I won't go into detail here. The RoomTransition() in the main.py is a bit long since it does some graphical tricks:
```python
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
                      'UP': vec(0, - st.HEIGHT + st.GUI_HEIGHT),  
                      'DOWN': vec(0, st.HEIGHT + st.GUI_HEIGHT),
                      'LEFT': vec(- st.WIDTH, st.GUI_HEIGHT),
                      'RIGHT': vec(st.WIDTH, st.GUI_HEIGHT)
                      }

    pos = start_positions[direction]
    # pos2 is the old bg's position that gets pushed out of the screen
    pos2 = vec(0, st.GUI_HEIGHT)

    while pos != (0, st.GUI_HEIGHT):
        # moves the 2 room backrounds until the new background is at (0,0)
        # the pos has to be restrained to prevent moving past (0,0) and 
        # stay forever in the loop
        scroll_speed = st.SCROLLSPEED
        if direction == 'UP':
            pos.y += scroll_speed
            pos2.y += scroll_speed
            pos.y = min(st.GUI_HEIGHT, pos.y)
        elif direction == 'DOWN':
            pos.y -= scroll_speed
            pos2.y -= scroll_speed
            pos.y = max(st.GUI_HEIGHT, pos.y)
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
        self.drawGUI()
        #self.player.draw()

        pg.display.flip()

    # put wall objects in the room after transition
    self.walls = fn.transitRoom(self, self.walls, self.dungeon)

```
To understand this, you have to remember that each room is not bigger than the screen. This means that there is no camera or something similar, and only one room is loaded at a time. The illusion of going into a new room is just done by sliding both the image of the old room you're in and the new room's image in the opposite direction you are facing, while the player is put at the opposite edge of the screen. And that's everything that happens here:
```python
# store the old background image temporarily
old_background = self.background
# build the new room
self.background = fn.tileRoom(self, self.tileset, 
                              self.dungeon.room_index)

# move the player to the other side of the screen
self.player.pos = new_pos
self.player.rect.center = self.player.pos
self.player.hit_rect.bottom = self.player.rect.bottom
```
First, the current background is stored temporarly in a variable. Then, the new background is created with the tileRoom() function. The player is moved to the other side already before the transition, but you won't see that because the screen doesn't update inbetween.

After that, the start position (pos) of the new background image is set based on the direction the player went. It is basically always one screen away from the current room.
```python
 # scroll the new and old background
# start positions for the new bg are based on the direction the
# player is moving
start_positions = {
                  'UP': vec(0, - st.HEIGHT + st.GUI_HEIGHT),  
                  'DOWN': vec(0, st.HEIGHT + st.GUI_HEIGHT),
                  'LEFT': vec(- st.WIDTH, st.GUI_HEIGHT),
                  'RIGHT': vec(st.WIDTH, st.GUI_HEIGHT)
                  }

pos = start_positions[direction]
# pos2 is the old bg's position that gets pushed out of the screen
pos2 = vec(0, st.GUI_HEIGHT)

while pos != (0, st.GUI_HEIGHT):
    # moves the 2 room backrounds until the new background is at (0,0)
    # the pos has to be restrained to prevent moving past (0,0) and 
    # stay forever in the loop
    scroll_speed = st.SCROLLSPEED
    if direction == 'UP':
        pos.y += scroll_speed
        pos2.y += scroll_speed
        pos.y = min(st.GUI_HEIGHT, pos.y)
    elif direction == 'DOWN':
        pos.y -= scroll_speed
        pos2.y -= scroll_speed
        pos.y = max(st.GUI_HEIGHT, pos.y)
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
    self.drawGUI()

    pg.display.flip()

# put wall objects in the room after transition
self.walls = fn.transitRoom(self, self.walls, self.dungeon)
```
pos2 is the position of the old background which is always the top left corner of the game screen (below the user interface). 
The scrolling happens in the while loop. While the new background's position is not the target position (which is the topleft of the game screen), it scrolls the two images in the respective direction with a set speed. After one iteration, the screen updates so that you actually see the two images moving. 
After finishing, the walls (and possible other objects) are put into the room.



So, feel free to play the game if you want. You can restart the game with the R key to get a fresh dungeon.

You can also change some variables in the settings.py (and try to crash the game, if you want ;) )


Feel free to test the code and commentate!
