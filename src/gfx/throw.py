from gfx import GFX
from pdcglobal import *
from pdcresource import *

class ThrowFX(GFX):
    
    rescache=None
    
    def __init__(self, dir, s_pos,t_pos,item):
        GFX.__init__(self)
        
        self.image=item.get_dd_img()

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