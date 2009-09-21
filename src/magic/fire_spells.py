from pdcresource import *
from pdcglobal import *
from magic import Spell
from gfx import *

class FireSpell(Spell):
    def __init__(self):
        Spell.__init__(self)
        self.color = RED
        self.type = ST_GENERIC
        
class FireBall(FireSpell):
    def __init__(self):
        FireSpell.__init__(self)
        self.phys_cost = 10
        self.mind_cost = 35
        self.name = 'Fireball'
        self.infotext = 'Causes a ball of Fire to explode'
    
    def target_choosen(self, pos):
        
        radius = 1 + (self.caster.mind - 100) / 50
        fx = BallFX(RED, YELLOW, self.caster.pos(), pos, radius)
        self.game.drawGFX(fx)
        actors = self.caster.game.get_all_srd_actors(pos,radius,True)
        for act in actors:
            amount = d(self.caster.mind / 20) + self.caster.mind / 20 + 2
            self.game.do_damage(act, amount, D_FIRE, self.caster)
            self.game.shout('%s burns %s' % (self.caster.name, act.name))
        
class HeatRay(FireSpell):
    def __init__(self):
        FireSpell.__init__(self)
        self.phys_cost = 10
        self.mind_cost = 30
        self.name = 'Heat Ray'
        self.infotext = 'Damage Foes with Fire'

    def target_choosen(self, pos):
        target = self.get_ray_target(self.caster.pos(), pos)
        if target == None:
            self.game.shout('Your spell fizzles')
        else:
            fx = RayFX(RED, YELLOW, self.caster.pos(), target.pos())
            self.game.drawGFX(fx)
            amount = d(self.caster.mind / 20) + self.caster.mind / 10 + 3 
            self.game.do_damage(target, amount, D_HEAT, self.caster)
            self.game.shout('%s burns %s' % (self.caster.name, target.name))       
#        target = self.get_ray_target(self.caster.pos(), pos)
#        if target == None:
#            self.game.shout('Your spell fizzles')
#        else:
#            fx = RayFX(WHITE,BLUE,self.caster.pos(),target.pos())
#            self.game.drawGFX(fx)
#            amount = d(self.caster.mind / 20) + self.caster.mind / 20
#            self.game.do_damage(target, amount, D_COLD,self.caster)
#            self.game.shout('%s freezed %s' % (self.caster.name, target.name))
