from pdcresource import *
from pdcglobal import *

class Spell(object):
    
    game = None
    
    def __init(self):
        self.phys_cost = 10
        self.mind_cost = 25
        self.name = 'generic'
        self.infotext = 'nothing'
        self.color = WHITE
        self.type = ST_GENERIC

    def get_ray_target(self, cpos, tpos):
        if cpos != tpos:
            poss = line(cpos[0], cpos[1], tpos[0], tpos[1])
            poss.pop(0)
            for pos in poss:
                actor = self.game.get_actor_at(pos)
                if actor != None:
                    return actor
        else:
            return self.caster
        return None
     
    def cast(self, caster):
        self.caster = caster
        self.game.wait_for_target(self.target_choosen)
    
    def info(self):
        l = ['PHY: %i MND: %i' % (self.phys_cost, self.mind_cost)]
        if isinstance(self.infotext,str):
            l.append(self.infotext)
        else:
            for line in self.infotext:
                l.append(line)
        return l
