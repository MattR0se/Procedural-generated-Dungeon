# Procedural Dungeon Generation - room(s) for improvement

This is my first attempt to write an algorithm for a procedural generated dungeon. Now, procedural in this context just means "random with rules", and the rules are not nearly as sophisticated in a game like Minecraft or Terraria, for example.

My goal was to put some even-sized rooms into a fixed 2D grid, and they should all be connected to each other. I put this code together in roughly a week, and build it on top of an older game "engine" of mine, so some things are super convoluted and need to be refactored at some point, but this was only done to test if the algorithm translates to an actual game.

I made two videos to show how this code looks right now. The first is a visualisation of the actual dungeon generation, the second one is the rudimentary "game" that puts some crudely drawn tiles in each room and lets you (the blue square) traverse the dungeon. Oh, and it also has a mini map, which is pretty much the same as the first example, only scaled to be in the corner of the screen.

https://youtu.be/-qDMl8qPB0I

https://youtu.be/cOoYRCCjxXI

Also, here are the codes, one for the visualisation example and one for the game:

https://github.com/MattR0se/Procedural-generated-Dungeon/tree/master/Demo

https://github.com/MattR0se/Procedural-generated-Dungeon/tree/master/Game

Since the code is pretty huge by now, and my in-code comments are probably not that helpful, I will now go over my process of building this system. The code is found in the second link.

I started with the Room and Dungeon classes, which are in the rooms.py file. A Dungeon is pretty much a collection of rooms. It stores their position and their other attributs (doors, type). The Dungeon is what is randomized every time at the beginning of the game (this is, when you call the build() method). The Room objects themselves are containers for the layout (objects, tiles) of each room. Currently, this is just the data where the doors are, and everything else is the same, but I will add more variety in the future.

## The Room

Every Room is initialized with a string called 'doors', which is any combination of 'NSWE', the 4 cardinal directions. It also has a type, but at this point there are only 'default' and 'start', but I could see adding 'boss', 'merchant' and the likes.
```python
class Room():
    def __init__(self, game, doors, type_='default'):
        self.game = game
        self.doors = doors
        self.type = type_
        self.w = st.WIDTH // st.TILESIZE
        self.h = st.HEIGHT // st.TILESIZE
```

After that, I set the room's image. Right now, this is only used for a mini map in the corner of the screen.

```python
for key in self.game.room_image_dict:
    if fn.compare(self.doors, key):
        self.image = self.game.room_image_dict[key]
```

This looks complicated, but what the compare() method does is compare two strings regardless of the order of their letters. For example, compare('NWS', 'SWN') would return True. This way I don't have to worry about the order of the doors string. The Room has one method called 'tileRoom()'. Here, both the layout for the objects and the tiles are created as two-dimensional arrays (because this is python, 'list of lists' would be more precise, but I hope you get the idea. Right now, the first and last column are all 1s, which stand for wall tiles, and the floor are 0s. Notice that the outer loop is for the columns and the inner loop is for the rows, which is something I always confuse and it is a point where errors happen frequently, especially if you want to combine this with (x, y) coordinates and vectors, where it is the other way round...

After the walls, the doors are put into the room's grid. I look for the 4 letters that represent the directions and if they are in the room's doors variable, a door is put in that particular spot. And that's it for now with the Room object.

As for the Dungeon object, it it initialized with a size (that restrains how big your Dungeon can possibly be and what shape it has), a room pool (every possible room object), a 'rooms' that is again a 2D grid for the rooms, initially with only 'None' in it, and a 'room_map' that stores an unique ID for every room. Now, this is probably not needed after I refactored the code, but for now it is necessary to check if there is a room transition and what the next room is after that.

Then, the starting room is created. In this example, it is a room with 4 exits and located in the middle of the grid, but it could also have any given position and number of exists. I believe this is how it's done in The Binding of Isaac, whereas in Zelda, the entrance would be at the bottom of the dungeon's grid.

There is also the 'room_index', which is probably redundant since it stores the same information as the room_map's contents.

Finally, 'build()' is called. Now, you could call this function from the Game() object instead if you wanted to instantiate the Dungeon only once but build a different maze multiple times. for example if you wanted to keep certain attributes the same, but randomize every time the player enters the dungeon. That's pretty much up to you.

Now, the build method is where the magic happens, so to speak. There is a while loop that goes through the rooms grid and checks for every room's doors and if there is empty space. Right now, this loops (height * width) times because this is the maximum number of rooms that could be placed. But in reality, this number is smaller because multiple rooms are being placed at the same time.I could have been more thoughtful about this and I will probably have to change it when performance becomes an issue. For example, I could give the rooms with only one door a 'dead end' attribute and check them only if they don't have it, and when no room was created, the loop exits.

A little bit more in-depth: The code loops through each item in the rooms grid. Remember that there are only 'None's in the beginning, except for the starting room. So if the loop reaches this room, the 'if room:' is True because 'None' defaults to False.

Now, there are a bunch of if-clauses that check if that room.doors has a certain direction in it and also if there is a room next to it in that direction. For example, if room.doors has 'N' in it, it has to check north of that room. That would be rooms[i-1][j] because remember, the vertical component comes first in the grid (Imagine this as rooms[y][x]). If there is no room, there are two options: If i == 1, it means that the next room would be placed at the border, so no room with an 'N' door should be placed there. For this example, I chose only to place the 'S' room, but other possible rooms would be 'SE', 'SW' and 'SWE'.

Otherwise, it the Dungeon picks a room constellation randomly from a list. Now, this is the important part that defines the overall structure of your final dungeon. See that currently, for the 'N' direction there are three items 'NS' in it, two 'S' and one of each of the other possible choices. So, it is twice as likely to pick the 'NS' than any other door constellation. So, here you can play with the list and see what happens. For example, if you put one more 'NS' room in there, the branches become more streched. If you have only one 'NS' in there, the rooms will somewhat clump together.

This is done for all 4 directions. You could also make totally different room_pools for each direction, if you want the dungeon to branch out more to one direction, for example. This is really up to you.

The second method blitRooms() is just a visual representation of the generated dungeon and serves as a mini map. If you want to know more about that, leave a comment.

I also won't go much into detail about the sprites.py, functions.py and settings.py. In sprites, there are just the player and the wall sprite and all the player does is move and check for collisions with the wall sprite. Aside from the collision, functions also contains the room transition (which is a mess tbh) and some methods for loading images and make a background out of a tileset. Again, feel free to ask about them in the comments.

The settings contain some variables regarding the screen and tile size. I made it so that you can change the GLOBAL_SCALE variable and everything in the game keeps its proportions.

Alright, so it all comes together in the main.py (as you would probably expect). First, I load all the images for the rooms (which are used for the mini map) and different tilesets that have a similar layout, but different color, from which the game picks a random one. In new(), the Dungeon, the background and the sprites are put into the game. The transitioning between rooms happens in the update() method (and it should probably be its own method for clarity reasons). Again, the system with room numbers and room index is too convoluted and I have to clean it up, but it works for now.

So, feel free to play the game if you want. You can restart the game with the R key to get a fresh dungeon.

You can also change some variables in the settings.py (and try to crash the game, if you want ;) )

Things I need to improve:

- The way the loop in the dungeon generation works right now is that it leaves out the first and last iteration. That was just a lazy way to prevent index errors, but prevents putting the starting room along a border.

- Close doors that lead to nowhere: Right now, there is the chance of generating one-way doors, where one room has a door in a direction but the adjacent room doesn't. I would appreciate some ideas on that.

- A pathfinding algorithm. Now, that's a whole 'nother topic, but at least I want to know what the longest branch in a dungeon is to place the boss room there, for example.

Also, the game currently has a bug where it occationally puts the wrong room. This is not happening in the demo, so maybe this is a copy/paste bug...

Feel free to test the code and commentate!
