from key_mapping import *
from pdcresource import *
from pdcglobal import *
from actor import Actor
from ai import AI

class SimpleAI(AI):
    def __init__(self, actor):
        AI.__init__(self, actor)
        
    def act(self):
        self.move_randomly()
