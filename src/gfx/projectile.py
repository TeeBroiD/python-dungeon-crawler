from gfx import GFX
from pdcglobal import *
from pdcresource import *

class ProjectileFX(GFX):
    
    rescache=None
    
    def __init__(self, dir, s_pos,t_pos,type='Arrow'):
        GFX.__init__(self)
        
        if ProjectileFX.rescache==None:
            ProjectileFX.rescache=Res('dc-item.png', TILESIZE)
        
        if type == 'Arrow':
            img = 73
        if dir == MOVE_UP:
            img = img
        if dir == MOVE_UP_RIGHT:
            img += 1
        if dir == MOVE_RIGHT:
            img += 2
        if dir == MOVE_DOWN_RIGHT:
            img += 3
        if dir == MOVE_DOWN:
            img += 4
        if dir == MOVE_DOWN_LEFT:
            img += 5
        if dir == MOVE_LEFT:
            img += 6
        if dir == MOVE_UP_LEFT:
            img += 7
            
        self.image=self.rescache.get(img)

        self.__pos_gen = self.__pos(s_pos, t_pos)
        self.redraw = True
        
    def __pos(self, s_pos, t_pos):
        s_real = s_pos[0] * TILESIZE - self.game.camera.x * TILESIZE, s_pos[1] * TILESIZE - self.game.camera.y * TILESIZE
        t_real = t_pos[0] * TILESIZE - self.game.camera.x * TILESIZE, t_pos[1] * TILESIZE - self.game.camera.y * TILESIZE
        all = line(s_real[0], s_real[1], t_real[0], t_real[1])[::6]
        for pos in all:
            yield pos

    def get_surf(self):
        return self.image
    
    def pos(self):
        try:
            pos = self.__pos_gen.next()
            return pos
        except:
            return None
    
    def tick(self):
        pass