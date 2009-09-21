import copy
from pdcglobal import *
from effect import Effect
import dungeon

class FloatingEyeGazeEffect(Effect):
    def __init__(self, host, owner):
        dur = d(10)
        Effect.__init__(self, dur, host, owner)
        weaponinfotext = 'Stuns the enemy'
        
    def tick(self):
        self.host.timer += 1000
        if self.host == self.host.game.player:
            self.host.game.shout('You are stunned by the Floating Eye`s gaze!')
        else:
            self.host.game.shout('%s is stunned by the Floating Eye`s gaze!' % (self.host.name))
        
        Effect.tick(self)

class AcidSplatterEffect(Effect):
    notrigger=[]
    def __init__(self, host, owner):
        dur = 1
        Effect.__init__(self, dur, host, owner)
        actors = owner.game.get_all_srd_actors(owner.pos())
        for act in actors:
            Effect.__init__(self, dur, act, owner)
        weaponinfotext = 'Splatters the enemy'
        
        
    def tick(self):
        self.host.game.do_damage(self.host, d(3), D_ACID, self.owner)
        if self.host == self.host.game.player:
            self.host.game.shout('You are splashed by acid!')
        else:
            self.host.game.shout('%s is splashed by acid!' % (self.host.name))
        Effect.tick(self)
        
class FrostEffect(Effect):
    def __init__(self, host, owner):
        dur = 1
        Effect.__init__(self, dur, host, owner)
        weaponinfotext = 'Freezes the enemy'
        
    def tick(self):
        self.host.game.do_damage(self.host, d(3), D_COLD, self.owner)
        if self.host == self.host.game.player:
            self.host.game.shout('You are freezing!')
        else:
            self.host.game.shout('%s is freezing!' % (self.host.name))
        Effect.tick(self)
        
class HeatEffect(Effect):
    def __init__(self, host, owner):
        dur = 1
        Effect.__init__(self, dur, host, owner)
        weaponinfotext = 'Burns the enemy'
        
    def tick(self):
        self.host.game.do_damage(self.host, d(3), D_FIRE, self.owner)
        if self.host == self.host.game.player:
            self.host.game.shout('You are getting burned!')
        else:
            self.host.game.shout('%s is getting burned!' % (self.host.name))
        Effect.tick(self)
        
class SplitEffect(Effect):
    notrigger=[]
    def __init__(self, host, owner):
        dur = 1
        Effect.__init__(self, dur, host, owner)
        weaponinfotext = 'You should not read this'
        
    def tick(self):
        new_pos = self.host.game.get_free_adj(self.owner.pos())
        if new_pos != None:
            self.owner.game.shout('%s splits in half!' % (self.owner.name))
            new = dungeon.Populator.create_creature(self.owner.pop_name, self.owner.filename)
            new.set_pos(new_pos)
            new.game.add_actor(new)
            self.owner.health = self.owner.health / 2 + 1
            self.owner.cur_health = self.owner.cur_health / 2 + 1
            new.health = self.owner.health
            new.cur_health = self.owner.cur_health
            new.xp_value = self.owner.xp_value / 3 + 2
        Effect.tick(self)

class DazzleEffect(Effect):
    def __init__(self, host, owner):
        dur = d(4)
        Effect.__init__(self, dur, host, owner)
        weaponinfotext = 'Blinds the enemy'
        
    def tick(self):
        self.host.dazzled = True
        if self.host == self.host.game.player:
            self.host.game.shout('You are blinded!')
        else:
            self.host.game.shout('%s is blinded!' % (self.host.name))
        Effect.tick(self)
