from pdcglobal import *
from pdcresource import Res
#from dmap import *
from cg import cave_gen
import bsd
import sys
import random
import copy
testmap = [
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 9, 9, 9, 9, 9, 9, 9, 9],
         [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 9],
         [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 9],
         [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 9, 9, 9, 9, 9, 9, 9, 9],
         [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 9],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 9],
         [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 9],
         [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 9],
         [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 9],
         [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 9],
         [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 9],
         [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 9],
         [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 9],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 9, 9, 9, 9, 9, 9, 9]]


class Map(object):
    
    tiles = None
    game = None
    
    def __init__(self, MapArray, level=1):
        self.game.add_to_world_objects(self)
        self.map_array = []

        for line in MapArray:
            new_line = []
            for tile in line:
                nt = (mt for mt in MAP_TILE_LIST if mt[MT_INDEX] == tile).next()
                new_line.append(copy.copy(nt))
            self.map_array.append(new_line)    
        
        self.height = len(MapArray)
        self.width = len(MapArray[0])
        self.cur_surf = None
        self.level = level
        Debug.debug('Map is ' + str(self.width) + 'x' + str(self.height))

    def check_tiles(self):
        if Map.tiles == None:
            Map.tiles = Res('dc-dngn.png', TILESIZE)

    def clear_surfaces(self):
        Map.Tiles = None
        self.cur_surf = None
        
    @staticmethod
    def Random(up=True, down=True, level=1, type=DG_BSD, w=80, h=40, s=5):
#        startx = 90
#        starty = 100
#        somename = dMap()
#        #size 50 x 50, a low (10) chance of making new rooms with a 50% chance new rooms will be corridors, and a maximum of 20 rooms.
#        somename.makeMap(startx, starty, 10, 40, 35)
#        array = [] 
#        for y in range(0, starty):
#            line = []
#            for x in range(0, startx):
#                if somename.mapArr[y][x] == 0: #floor
#                    line.append(0)
#                if somename.mapArr[y][x] == 1: #void
#                    line.append(9)
#                if somename.mapArr[y][x] == 2: #wall
#                    line.append(1)
#                if somename.mapArr[y][x] == 3 or somename.mapArr[y][x] == 4 or somename.mapArr[y][x] == 5: #door
#                    line.append(2)
#            array.append(line)
        
        
        if type == DG_BSD:
        #LOOK AWAY!! BAD, BAD CODE!!
            i = 0
            array = None
            r1 = bsd.Room(0, 0, w, h)
            bsd.split(r1, s)
            while array == None and i < 20:
                i += 1
                try:
                    array = bsd.create(r1)
                except:
                    array = None
                    r1 = bsd.Room(0, 0, w, h)
                    bsd.split(r1, s)
            
            if array == None:
                raise 'Argh!! Bad code rising!'
    
            for y in xrange(len(array)):
                for x in xrange(len(array[0])):
                    if array[y][x] == '.':
                        array[y][x] = 1
                    if array[y][x] == '*':
                        array[y][x] = 0
                    
#        c=cave_gen(100,50,4)
#        c.fix()
#        array=c.A
#                        
#        for y in xrange(len(array)):
#            for x in xrange(len(array[0])):
#                if array[y][x] == 1:
#                    array[y][x] = 9
#                if array[y][x] == 0:
#                    array[y][x] = -1
                    
        map = Map(array, level)
        if down:
            x, y = map.get_random_pos()
            map.map_array[y][x] = MAP_TILE_down
        if up:
            x, y = map.get_random_pos()
            map.map_array[y][x] = MAP_TILE_up
 
        return map
    
    def get_random_pos(self):
        pos = None
        while pos == None:
            y = random.randint(0, self.height - 1)
            x = random.randint(0, self.width - 1)
            Debug.debug('get random pos: ' + str(x) + ' ' + str(y))
            if self.map_array[y][x][MT_FLAGS] & F_WALKABLE : pos = x, y
        return x, y
    
    def can_enter(self, pos, move_mode):
        
        target_tile = self.map_array[pos[1]][pos[0]]
        if target_tile[MT_FLAGS] & move_mode: return True
                
        return False
        
    def get_tile_at(self, x, y):
        self.check_tiles()
        #if self.map_array[y][x][MT_IMAGE] == 3:
        #    print 'sdasd'
        img = self.tiles.get(self.map_array[y][x][MT_IMAGE])
        return img
