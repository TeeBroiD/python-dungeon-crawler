from pdcglobal import *
from effect import Effect
from dv_effects import DazzleEffect

class StunEffect(Effect):
    def __init__(self, host, owner):
        dur = d(3)
        Effect.__init__(self, dur, host, owner)
        weaponinfotext = 'Stuns the enemy'
        
    def tick(self):
        self.host.timer += self.host.speed * d(3)
        if self.host == self.host.game.player:
            self.host.game.shout('You are stunned')
        else:
            self.host.game.shout('%s is stunned' % (self.host.name))
        
        Effect.tick(self)

class BleedEffect(Effect):
    def __init__(self, host, owner):
        dur = d(10)
        Effect.__init__(self, dur, host, owner)
        weaponinfotext = 'Makes the enemy bleed'
        
    def tick(self):
        self.host.game.do_damage(self.host, d(3), D_GENERIC, self.owner)
        if self.host == self.host.game.player:
            self.host.game.shout('You are bleeding')
        else:
            self.host.game.shout('%s bleeds' % (self.host.name))
        Effect.tick(self)

class BugPoisonEffect(Effect):
    def __init__(self, host, owner):
        dur = d(25)
        Effect.__init__(self, dur, host, owner)
        weaponinfotext = 'Poisons the enemy'
        
    def tick(self):
        if d(100) < 5:
            self.host.timer += self.host.speed * d(5)
            if self.host == self.host.game.player:
                self.host.game.shout('You suddenly fell asleep')
            else:
                self.host.game.shout('%s suddenly fells asleep' % (self.host.name))
        Effect.tick(self)

class YumuraPoisonEffect(Effect):
    def __init__(self, host, owner):
        dur = d(10)
        Effect.__init__(self, dur, host, owner)
        weaponinfotext = 'Poisons the enemy'
        
    def tick(self):
        self.host.game.do_damage(self.host, d(3), D_POISON, self.owner)
        notice = False
        if d(100) < 10:
            StunEffect(self.host, self.owner)
            notice = True
        if d(100) < 10:
            DazzleEffect(self.host, self.owner)
            notice = True
        if d(100) < 10:
            self.host.game.do_damage(self.host, d(3), D_POISON, self.owner)
            notice = True
        if d(100) < 2:
            self.host.game.do_damage(self.host, d(25), D_POISON, self.owner)
            notice = True
        if notice:
            if self.host == self.host.game.player:
                self.host.game.shout('You are poisoned')
            else:
                self.host.game.shout('%s is poisoned' % (self.host.name))
        Effect.tick(self)

class KillerbeePoisonEffect(Effect):
    def __init__(self, host, owner):
        dur = d(10)
        Effect.__init__(self, dur, host, owner)
        weaponinfotext = 'Poisons the enemy'
        
    def tick(self):
        self.host.game.do_damage(self.host, d(3), D_POISON, self.owner)
        if d(100) < 35:
            StunEffect(self.host, self.owner)
        if d(100) < 35:
            DazzleEffect(self.host, self.owner)
        if self.host == self.host.game.player:
            self.host.game.shout('You are poisoned')
        else:
            self.host.game.shout('%s is poisoned' % (self.host.name))
        Effect.tick(self)
        
class StrokingEffect(Effect):
    def __init__(self, host, owner):
        dur = 1
        Effect.__init__(self, dur, host, owner)
        weaponinfotext = 'Strokes the enemy'
        
    def tick(self):
        if self.host == self.host.game.player:
            self.host.game.shout('You are getting stroked by %s' % (self.owner.name))
        else:
            self.host.game.shout('%s is getting stroked' % (self.host.name))
        Effect.tick(self)
