from pdcresource import Res
from pdcglobal import *
class Cursor(object):
    
    def __init__(self, game):
        self.game = game
        self.x = 0
        self.y = 0
        self.cursor_surf = None
        
    def get_surf(self):
        if self.cursor_surf == None:
            res = Res('cursor.png', TILESIZE)
            self.cursor_surf = res.get(0)
        return self.cursor_surf  

    def pos(self):
        return self.x, self.y

    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        
    def move(self, direction):
        new_pos = get_new_pos(self.pos(), direction)
        if not (self.game.player.sc.lit(new_pos[0], new_pos[1]) or new_pos == self.game.player.pos()): return
        actor = self.game.get_actor_at(new_pos)
        if actor != None:
            self.game.shout('You see a %s' % (actor.name))
        items = self.game.get_items_at(new_pos)
        if len(items) == 1:
            self.game.shout('You see a %s' % (items[0].get_name()))
        if len(items) > 1:
             self.game.shout('You see several items here')  
        self.set_pos(new_pos)
