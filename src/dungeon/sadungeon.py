from pdcglobal import *
from map import *
from populator import *


class SADungeon(object):
    game = None
    def __init__(self):
        self.levels = 0
        self.name = 'Generic Dungeon'

    def get_map(self, level):
        pass
        
class DungeonsOfGogadan(SADungeon):
    def __init__(self):
        SADungeon.__init__(self)
        self.levels = 15
        self.name = 'Dungeons of Gogadan'
        
    def __floor_1_2(self, level):
        map = Map.Random(True, True, level, DG_BSD, 40, 40, 4)
        self.game.map = map
       # Populator.fill_map_with_creatures(map, 'test', 15, 25)
        
        Populator.fill_map_with_items(map, 'basic_weapons', 0, 3, 0)
        Populator.fill_map_with_items(map, 'basic_stuff', 0, 4, 0)
        #Populator.fill_map_with_items(map, 'basic_books', 0, 2, 99)
        ##Populator.fill_map_with_items(map, 'basic_potions', 0, 2, 99)
        ##Populator.fill_map_with_creatures(map, 'easy_swarms', 0, 2)
        Populator.fill_map_with_creatures(map, 'test', 5, 7)
        #Populator.fill_map_with_creatures(map, 'easy_other', 2, 5)
        #Populator.fill_map_with_creatures(map, 'easy_jelly', 0, 3)
        ##Populator.fill_map_with_creatures(map, 'easy_golems', 0, 5)
        return map
    
    def __floor_3_4(self, level):
        map = Map.Random(True, True, level, DG_BSD, 40, 40, 4)
        self.game.map = map
        Populator.fill_map_with_items(map, 'basic_weapons', 1, 3, 12)
        Populator.fill_map_with_items(map, 'basic_stuff', 0, 2, 12)
        Populator.fill_map_with_items(map, 'basic_books', 0, 1, 99)
        Populator.fill_map_with_items(map, 'basic_potions', 1, 4, 99)
        Populator.fill_map_with_creatures(map, 'easy_swarms', 1, 2)
        Populator.fill_map_with_creatures(map, 'easy_other', 2, 5)
        Populator.fill_map_with_creatures(map, 'easy_jelly', 0, 2)
        Populator.fill_map_with_creatures(map, 'easy_golems', 1, 2)
        return map
    
    def __floor_5_6(self, level):
        map = Map.Random(True, True, level, DG_BSD, 60, 60, 5)
        self.game.map = map
        Populator.fill_map_with_items(map, 'basic_weapons', 1, 3, 12)
        Populator.fill_map_with_items(map, 'basic_stuff', 0, 2, 12)
        Populator.fill_map_with_items(map, 'basic_books', 0, 1, 99)
        Populator.fill_map_with_items(map, 'basic_potions', 1, 4, 99)
        Populator.fill_map_with_creatures(map, 'easy_swarms', 3, 5)
        Populator.fill_map_with_creatures(map, 'easy_other', 3, 5)
        Populator.fill_map_with_creatures(map, 'easy_jelly', 4, 5)
        Populator.fill_map_with_creatures(map, 'easy_golems', 7, 9)
        return map
     
    def get_map(self, level):
        if level < 3:
            return self.__floor_1_2(level)
        if level < 5:
            return self.__floor_3_4(level)
        if level < 7:
            return self.__floor_5_6(level)
