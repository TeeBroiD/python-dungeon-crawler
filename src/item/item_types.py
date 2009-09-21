from pdcglobal import *
from item import Item

class Armor(Item):
    def __init__(self, add):
        Item.__init__(self,add)
        self.type=I_ARMOR
        
class Cloak(Item):
    def __init__(self, add):
        Item.__init__(self,add)
        self.type=I_ARMOR
        
class Weapon(Item):
    def __init__(self, add):
        Item.__init__(self,add)
        self.type=I_WEAPON

class Unarmed(Item):
    def __init__(self, add):
        Item.__init__(self,add)
        self.type=I_WEAPON
        self.skills.append(WT_UNARMED)
        self.damage='1D3',lambda : cd(int(1), int(3))
        #item.damage = value, lambda : cd(int(no), int(ey)) + int(add)
class Shield(Item):
    def __init__(self, add):
        Item.__init__(self,add)
        self.type=I_SHIELD

class Boots(Item):
    def __init__(self, add):
        Item.__init__(self,add)
        self.type=I_BOOTS

class Helmet(Item):
    def __init__(self, add):
        Item.__init__(self,add)
        self.type=I_HELMET

class Trousers(Item):
    def __init__(self, add):
        Item.__init__(self,add)
        self.type=I_TROUSERS

class Ammo(Item):
    def __init__(self, add):
        Item.__init__(self,add)
        self.type=I_AMMO
        
class Gold(Item):
    def __init__(self, add):
        Item.__init__(self,add)
        self.type=I_GOLD

class Stuff(Item):
    def __init__(self, add):
        Item.__init__(self,add)
        self.type=I_STUFF

        

        

        
