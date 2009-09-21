from pdcresource import *
from pdcglobal import *
from magic import Spell
from gfx import *

class ColdSpell(Spell):
    def __init__(self):
        Spell.__init__(self)
        self.color = BLUE
        self.type = ST_GENERIC
        
class FrostRay(ColdSpell):
    def __init__(self):
        ColdSpell.__init__(self)
        self.phys_cost = 5
        self.mind_cost = 30
        self.name = 'Frost Ray'
        self.infotext = 'Damage Foes with cold'

    def target_choosen(self, pos):
        target = self.get_ray_target(self.caster.pos(), pos)
        if target == None:
            self.game.shout('Your spell fizzles')
        else:
            fx = RayFX(WHITE, BLUE, self.caster.pos(), target.pos())
            self.game.drawGFX(fx)
            amount = d(self.caster.mind / 20) + self.caster.mind / 10 + 2 
            self.game.do_damage(target, amount, D_COLD, self.caster)
            self.game.shout('%s freezed %s' % (self.caster.name, target.name))
        
