from actor import Humanoid   
from pdcglobal import d
from magic import *

class Human(Humanoid):
    desc = 'was versatile and talented at every topic.'
    def __init__(self, add, gender=0):
        Humanoid.__init__(self, add)
        self.img_body = 0 + gender, 0
        self.MOVE = 4
        
class Alb(Humanoid):
    desc = 'was a quick and wiry person.'
    def __init__(self, add, gender=0):
        Humanoid.__init__(self, add)
        self.img_body = 10 + gender, 0
        self.MOVE = 5
        
class Naga(Humanoid):
    desc = 'was less talented in melee-weapons, but gifted in magic.'
    def __init__(self, add, gender=0):
        Humanoid.__init__(self, add)
        spell = random.choice([FrostRay, HeatRay, LesserHealing, Regeneration, Identify])
        self.spells.append(spell())
        self.MOVE = 3
        del self.slot.__dict__['trousers']
        del self.slot.slots['trousers']
        del self.slot.__dict__['boots']
        del self.slot.slots['boots']
        
races = (('Human', 0, 1, Human),
         ('Naga', 16, 17, Naga),
         ('Alb', 10, 11, Alb))

