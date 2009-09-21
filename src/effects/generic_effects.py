from pdcglobal import *
from effect import Effect

class RegenerationEffect(Effect):
    def __init__(self, host, owner):
        dur = 10
        Effect.__init__(self, dur, host, owner)
    
    def tick(self):
        a = -d(4)
        if self.host.cur_health - a > self.host.health:
            a = self.host.cur_health - self.host.health
        self.host.game.do_damage(self.host, a, D_ORDER)
        if self.host == self.host.game.player:
            self.host.game.shout('You are regenerating')
        else:
            self.host.game.shout('%s is regenerating' % (self.host.name))
        Effect.tick(self)
