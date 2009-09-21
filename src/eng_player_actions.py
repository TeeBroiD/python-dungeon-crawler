from pdcglobal import *

class PlayerActions(object):
    def __init__(self, game):
        self.game = game
    
    def cursor(self):
        self.game.cursor.set_pos(self.game.player.pos())
        self.game.state = S_PLAYER_CURSOR
    def stats(self):
        gen = get_chars()
        self.game._items_to_choose = {}
        for stat in self.game.stats:
            self.game._items_to_choose[gen.next()] = stat
        self.game.state = S_PLAYER_STATS
    
    def throw_fired(self,pos):
        self.game.player.throw(self.game.item_to_throw,pos)
        self.game.item_to_throw=None
        
    def throw_fire(self):
        self.game.cursor.set_pos(self.game.player.pos())
        self.game.state = S_PLAYER_CURSOR
        self.game.wait_for_target(self.throw_fired)
    
    def fire(self):
        weapon = self.game.player.weapon
        ammo = self.game.player.ammo
        if weapon == None or not weapon.flags & IF_RANGED:
            self.game.shout('You are not wielding a Range-Weapon')
            return
        if ammo == None:
            self.game.shout('You have no ammonition ready')
            return
        if not ammo_fits_weapon(ammo,weapon): 
          #((ammo.flags & IF_ARROW and weapon.flags & IF_FIRES_ARROW) or 
          #      (ammo.flags & IF_BOLT and weapon.flags & IF_FIRES_BOLT)): 
            self.game.shout('Ammonition doesn`t fit to Weapon')
            return
        
        self.game.cursor.set_pos(self.game.player.pos())
        self.game.state = S_PLAYER_CURSOR
        self.game.wait_for_target(self.fired)
        
    def fired(self,pos):
        self.game.player.fire(pos)
        
    def cast(self):
        spells = [spell for spell in self.game.player.spells]
        if len(spells) == 0:
            self.game.shout("You don't know any spells")
            return
        gen = get_chars()
        self.game._items_to_choose = {}
        for spell in spells:
            self.game._items_to_choose[gen.next()] = spell
        self.game.state = S_PLAYER_CAST
    def identify(self):
        items = []
        equipm = self.game.player.get_equipment().extend(self.game.player.items)
        for item in [item for item in self.game.player.items if item.special and not item.flags & IF_IDENTIFIED]:
            items.append(item) 
        if len(items) == 0:
            self.game.shout("You have nothing to identify")
            return
        gen = get_chars()
        self.game._items_to_choose = {}
        for item in items:
            self.game._items_to_choose[item.get_ps()] = item
        self.game.state = S_PLAYER_IDENTIFY
    def read(self):
        items = [item for item in self.game.player.items if item.flags & IF_READABLE]
        if len(items) == 0:
            self.game.shout("You have nothing to read")
            return
        gen = get_chars()
        self.game._items_to_choose = {}
        for item in items:
            self.game._items_to_choose[item.get_ps()] = item
        self.game.state = S_PLAYER_READ
    def drink(self):
        items = [item for item in self.game.player.items if item.flags & IF_DRINKABLE]
        if len(items) == 0:
            self.game.shout("You have nothing to drink")
            return
        gen = get_chars()
        self.game._items_to_choose = {}
        for item in items:
            self.game._items_to_choose[item.get_ps()] = item
        self.game.state = S_PLAYER_DRINK
    def take_off(self):
        items = self.game.player.get_equipment()
        if len(items) == 0:
            self.game.shout("You have nothing to take off")
            return
        gen = get_chars()
        self.game._items_to_choose = {}
        for item in items:
            self.game._items_to_choose[item.get_ps()] = item
        self.game.state = S_PLAYER_TAKE_OFF
    
    def throw(self):
        items = [item for item in self.game.player.items if not item.equipped]
        if self.game.player.weapon != None:
            items.append(self.game.player.weapon)
        if len(items) == 0:
            self.game.shout("You have nothing to throw")
            return
        gen = get_chars()
        self.game._items_to_choose = {}
        for item in items:
            self.game._items_to_choose[item.get_ps()] = item
        self.game.state = S_PLAYER_CHOOSE_THROW
    
    def drop(self):
        items = [item for item in self.game.player.items if not item.equipped]
        if len(items) == 0:
            self.game.shout("You have nothing to drop")
            return
        gen = get_chars()
        self.game._items_to_choose = {}
        for item in items:
            self.game._items_to_choose[item.get_ps()] = item
        self.game.state = S_PLAYER_DROP
    def equip(self):
        items = [item for item in self.game.player.items if item.flags & IF_EQUIPABLE and not item.equipped]
        if len(items) == 0:
            self.game.shout("You have nothing to equip")
            return
        gen = get_chars()
        self.game._items_to_choose = {}
        for item in items:
            self.game._items_to_choose[item.get_ps()] = item
        self.game.state = S_PLAYER_EQUIP    
    def pick_up(self):
        items = self.game.get_items_at(self.game.player.pos())
        if len(items) == 0:
            self.game.shout("There's nothing to pickup")
            return
        if len(items) == 1:
            self.game.player.pick_up(items[0])
            return
        gen = get_chars()
        self.game._items_to_choose = {}
        for item in items:
            self.game._items_to_choose[item.get_ps()] = item
            
        self.game.state = S_PLAYER_PICK_UP
    def downstairs(self):
        x, y = self.game.player.pos()
        if self.game.map.map_array[y][x][MT_FLAGS] & F_SC_DOWN:
            self.game.change_map(True)
        else:
            self.game.shout("You can't go downstairs here")
    def upstairs(self):
        x, y = self.game.player.pos()
        if self.game.map.map_array[y][x][MT_FLAGS] & F_SC_UP:
            self.game.change_map(False)
        else:
            self.game.shout("You can't go upstairs here")

