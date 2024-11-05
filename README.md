# ExileRogues


Python mini game : 


main.py => handling all the main execution and Inputs

engine.py => handling user events , and rendering in console

procegen.py => generating our dungeon (random) + rectangles which are our rooms
	-> we check if intersects 
	-> we make a tunnel between rooms with a tcod.los.bresenham function.tolist()
	-> we also check the center of a room : x + y / 2
	-> we make generate the dungeon with our GameMap class and make rooms within
	-> we have to check if each room generated intersect the old one or not

inputhandlers.py => handling user input and sending an action back from that input

action.py -> perform user actions

Entity.py -> functions to deal with our player Entity such as move( x += dx , y += dy)

tile_types => making the type of tiles we want in our dungeon such as walls and floor



type structs : 
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # Unicode codepoint.
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)


# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", np.bool),  # True if this tile can be walked over.
        ("transparent", np.bool),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
    ]
)






Field of view

When walking in the dungeon there are 3 states a tile can be in 

Visible
Not visible
Not visible, but previously seen

we should draw visible and prev seens tiles
The not visible can be empty or grey dont care

We use a compute_fov() from tcod API which takes in the transparent tiles, the player position and the radius

Then we only render the tiles which are visible from the game_map object

self.game_map.explored |= self.game_map.visible 
	-> This adds in explored everything from visible + every it already had before









