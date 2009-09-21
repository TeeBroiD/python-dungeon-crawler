from pdcresource import *
from pdcglobal import *
from magic import Spell

class GenericSpell(Spell):
    def __init__(self):
        Spell.__init__(self)
        self.color = GREEN
        self.type = ST_GENERIC
        
class LesserHaste(GenericSpell):
    def __init__(self):
        GenericSpell.__init__(self)
        self.phys_cost = 5
        self.mind_cost = 15
        self.name = 'Lesser Haste'
        self.infotext = 'Speed Up'
    
    
    def target_choosen(self, pos):
        target = self.game.get_actor_at(pos)
        if target == None:
            self.game.shout('Your spell fizzles')
        else:
            amount = d(self.caster.mind / 10) + 3
            if target.cur_speed > target.speed / 2:
                target.cur_speed -= amount
            self.game.shout('%s speeds up %s' % (self.caster.name, target.name))

        
class Identify(GenericSpell):
    def __init__(self):
        GenericSpell.__init__(self)
        self.phys_cost = 0
        self.mind_cost = 25
        self.name = 'Identify'
        self.infotext = 'Identify an Item'
    def cast(self, caster):
        self.caster = caster
        self.game.do_identify()
