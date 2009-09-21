class Att(object):
    game=None
    def __init__(self, name, info, cost=30):
        self.cost = cost
        self.name = name
        self.__info = info
    def info(self):
        return ['Current: %i'%(getattr(self.game.player,self.name.lower())),
        'Cost: %i XP'%(self.cost)]
