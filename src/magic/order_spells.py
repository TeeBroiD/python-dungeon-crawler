from pdcresource import *
from pdcglobal import *
from magic import Spell
from effects import generic_effects
class OrderSpell(Spell):
    def __init__(self):
        Spell.__init__(self)
        self.color = WHITE
        self.type = ST_ORDER

class Regeneration(OrderSpell):
    def __init__(self):
        OrderSpell.__init__(self)
        self.phys_cost = 25
        self.mind_cost = 65
        self.name = 'Regeneraton'
        self.infotext = 'Target regenerates'
    
    def target_choosen(self, pos):
        target = self.game.get_actor_at(pos)
        if target == None:
            self.game.shout('Your spell fizzles')
        else:
            self.game.shout('%s regenerate %s' % (self.caster.name, target.name))
            r = generic_effects.RegenerationEffect(target, self.caster)
            r.tick()
  

class LesserHealing(OrderSpell):
    def __init__(self):
        OrderSpell.__init__(self)
        self.phys_cost = 5
        self.mind_cost = 25
        self.name = 'Lesser Healing'
        self.infotext = 'Cures small wounds'
    
    def target_choosen(self, pos):
        target = self.game.get_actor_at(pos)
        if target == None:
            self.game.shout('Your spell fizzles')
        else:
            amount = d(self.caster.mind / 10) + 3
            if target.cur_health + amount > target.health:
                amount = target.health - target.cur_health
            self.game.do_damage(target, -amount)
            self.game.shout('%s healed %s' % (self.caster.name, target.name))

        
class Healing(OrderSpell):
    def __init__(self):
        OrderSpell.__init__(self)
        self.phys_cost = 10
        self.mind_cost = 55
        self.name = 'Healing'
        self.infotext = 'Cures wounds'
        
    def target_choosen(self, pos):
        target = self.game.get_actor_at(pos)
        if target == None:
            self.game.shout('Your spell fizzles')
        else:
            amount = d(self.caster.mind / 10) + d(self.caster.mind / 10) + 5
            self.game.do_damage(target, -amount)
            self.game.shout('%s healed %s' % (self.caster.name, target.name))

