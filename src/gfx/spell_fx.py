from pdcglobal import *
from gfx import GFX

class BallFX(GFX):
    def __init__(self, color1, color2, s_pos, t_pos, radius=1):
        GFX.__init__(self)
        self.f_image = []
        surf = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        pygame.draw.circle(surf, color1, (16, 16), 2, 2)
        self.f_image.append(surf)
        surf = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        pygame.draw.circle(surf, color2, (16, 16), 2, 2)
        self.f_image.append(surf)
        surf = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        pygame.draw.circle(surf, color1, (16, 16), 2, 2)
        self.f_image.append(surf)
        self.color1 = color1
        self.color2 = color2
        self.c = 0
        self.image = self.f_image[self.c]
        self.__pos_gen = self.__pos(s_pos, t_pos)
        self.redraw = False
        self.radius = radius
        self.cur_radius = 0
        self.explode = False
        self.finish = False
        self.lastpos = None
    def __pos(self, s_pos, t_pos):
        s_real = s_pos[0] * TILESIZE - self.game.camera.x * TILESIZE, s_pos[1] * TILESIZE - self.game.camera.y * TILESIZE
        t_real = t_pos[0] * TILESIZE - self.game.camera.x * TILESIZE, t_pos[1] * TILESIZE - self.game.camera.y * TILESIZE
        all = line(s_real[0], s_real[1], t_real[0], t_real[1])[::6]
        for pos in all:
            yield pos

    def get_surf(self):
        return self.image
    
    def pos(self):
        if not self.explode:
            try:
                pos = self.__pos_gen.next()
                self.lastpos = pos
                return pos
            except:
                self.explode = True
                #self.redraw = True
                return self.lastpos
        else:
            if not self.finish:
                return self.lastpos[0]+self.xoff,self.lastpos[1]+self.yoff
            else:
                return None
            
    def tick(self):
        #self.c += 1
        #if self.c >= len(RayFX.f_image): 
        #    self.c = 0
        if not self.explode:
            self.c = random.randint(0, len(self.f_image) - 1)    
            self.image = self.f_image[self.c]
        else:
            #size = self.cur_radius
            max_size = int((self.radius + 0.5) * TILESIZE)
            
            self.image = pygame.Surface((max_size*2, max_size*2), pygame.SRCALPHA, 32)
            if d(100) > 20:
                color = self.color1
            else:
                color = self.color2
            
            width=4
            if  int(self.cur_radius)<width:
                width= int(self.cur_radius)
            pygame.draw.circle(self.image, color, (max_size, max_size),  int(self.cur_radius), width)
            
            self.cur_radius += 4
            
            #size = (float(self.cur_radius) + 0.5) * TILESIZE
            self.xoff=-TILESIZE*self.radius
            self.yoff=-TILESIZE*self.radius
            if self.cur_radius >= max_size:
                self.finish = True
class RayFX(GFX):
    def __init__(self, color1, color2, s_pos, t_pos):
        GFX.__init__(self)
        self.f_image = []
        surf = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        pygame.draw.circle(surf, color1, (15, 10), 2, 2)
        pygame.draw.circle(surf, color2, (10, 15), 2, 2)
        pygame.draw.circle(surf, color1, (20, 15), 2, 2)
        self.f_image.append(surf)
        surf = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        pygame.draw.circle(surf, color2, (15, 10), 2, 2)
        pygame.draw.circle(surf, color1, (10, 15), 2, 2)
        pygame.draw.circle(surf, color1, (20, 15), 2, 2)
        self.f_image.append(surf)
        surf = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        pygame.draw.circle(surf, color1, (15, 10), 2, 2)
        pygame.draw.circle(surf, color1, (10, 15), 2, 2)
        pygame.draw.circle(surf, color2, (20, 15), 2, 2)
        self.f_image.append(surf)
            
        self.c = 0
        self.image = self.f_image[self.c]
        self.__pos_gen = self.__pos(s_pos, t_pos)
        self.redraw = False
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
        #self.c += 1
        #if self.c >= len(RayFX.f_image): 
        #    self.c = 0
        self.c = random.randint(0, len(self.f_image) - 1)    
        self.image = self.f_image[self.c]

