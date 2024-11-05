from __future__ import annotations
from typing import Iterator, List, Tuple, TYPE_CHECKING
import random
from game_map import GameMap
import tile_types

import tcod

if TYPE_CHECKING:
    from entity import Entity

class RectangularRoom:
    def __init__(self, x ,y , width, height):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        
    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y= int((self.y1 + self.y2) / 2)
        
        return center_x, center_y
    
    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1 , self.y2)
    
    def intersects(self, other: RectangularRoom) -> bool:
        """return True if room overlaps with another room"""
        return (self.x1 <= other.x2
                and self.x2 >= other.x1
                and self.y1 <= other.y2
                and self.y2 >= other.y2)

def tunnel_between(start: Tuple[int,int], end= Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2
    
    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x,y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y
    
def generate_dungeon(max_rooms: int, room_min_size:int, room_max_size:int, map_width:int, map_height:int, player:Entity) -> GameMap:
    """generate dungeon map"""
    dungeon = GameMap(map_width, map_height)
    
    rooms: List[RectangularRoom] = []
    
    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)
        
        x = random.randint(0, dungeon.width - room_width -1)
        y = random.randint(0, dungeon.height - room_height - 1)
        
        # RectangularRoom class makes rectangles easier to work with
        new_room = RectangularRoom(x, y , room_width, room_height)
        
        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue # This room intersects so go to next attempt;
        # If no interesction room is valid
        
        dungeon.tiles[new_room.inner] = tile_types.floor
        
        if len(rooms) == 0:
            player.x, player.y = new_room.center
        else:
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor
        
        rooms.append(new_room)    
        
    return dungeon