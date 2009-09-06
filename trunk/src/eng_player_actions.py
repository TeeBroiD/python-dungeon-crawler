from pdcglobal import *

class PlayerActions(object):
    def __init__(self, game):
        self.game = game
        
    def cast(self):
        spells = [spell for spell in self.game.player.spells]
        if len(spells) == 0:
            self.game.message_queue.insert(0, "You don't know any spells")
            return
        gen = get_chars()
        self.game._items_to_choose = {}
        for spell in spells:
            self.game._items_to_choose[gen.next()] = spell
        self.game.state = S_PLAYER_CAST
    def take_off(self):
        items =self.game.player.get_equipment()
        if len(items) == 0:
            self.game.message_queue.insert(0, "You have nothing to take off")
            return
        gen = get_chars()
        self.game._items_to_choose = {}
        for item in items:
            self.game._items_to_choose[gen.next()] = item
        self.game.state = S_PLAYER_TAKE_OFF
    def drop(self):
        items = [item for item in self.game.player.items]
        if len(items) == 0:
            self.game.message_queue.insert(0, "You have nothing to drop")
            return
        gen = get_chars()
        self.game._items_to_choose = {}
        for item in items:
            self.game._items_to_choose[gen.next()] = item
        self.game.state = S_PLAYER_DROP
    def equip(self):
        items = [item for item in self.game.player.items if item.flags & IF_EQUIPABLE]
        if len(items) == 0:
            self.game.message_queue.insert(0, "You have nothing to equip")
            return
        gen = get_chars()
        self.game._items_to_choose = {}
        for item in items:
            self.game._items_to_choose[gen.next()] = item
        self.game.state = S_PLAYER_EQUIP    
    def pick_up(self):
        items = self.game.get_items_at(self.game.player.pos())
        if len(items) == 0:
            self.game.message_queue.insert(0, "There's nothing to pickup")
            return
        if len(items) == 1:
            self.game.player.pick_up(items[0])
            self.game.message_queue.insert(0, 'You picked up a %s' % (items[0].name))
            return
        gen = get_chars()
        self.game._items_to_choose = {}
        for item in items:
            self.game._items_to_choose[gen.next()] = item
            
        self.game.state = S_PLAYER_PICK_UP
    def downstairs(self):
        x, y = self.game.player.pos()
        if self.game.map.map_array[y][x][MT_FLAGS] & F_SC_DOWN:
            self.game.random_map()
        else:
            self.game.message_queue.insert(0, "You can't go downstairs here")
    def upstairs(self):
        x, y = self.game.player.pos()
        if self.game.map.map_array[y][x][MT_FLAGS] & F_SC_UP:
            self.game.random_map()
        else:
            self.game.message_queue.insert(0, "You can't go upstairs here")