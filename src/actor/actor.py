from ai import *
from key_mapping import *
from pdcresource import *
from pdcglobal import *
from item import *
from hit_zones import HitZones
from skills import Skills
import pygame

class Actor(object):
    
    tiles = None
    game = None
    
    def __init__(self, add):
        Debug.debug('Creating Actor')
        self.game.add_actor(self, add)
        self.name = 'Generic Actor'
        self.cur_surf = None
        self.img_body = None
        self.id = self.game.get_id()
        self.sc = None

        self.timer = 0
                
        self.x = 1
        self.y = 1
        
        self.morale = 75
        
        self.move_mode = MM_WALK 
        
        self.timer = 0
        self.ai = AI(self)
        
        self.gold = 0
        self.xp_value = 25
        self.xp = 0
        
        self.STR = r4d6()
        self.CON = r4d6()
        self.DEX = r4d6()
        self.SIZ = r2d6()
        self.INT = r2d6()
        self.POW = r4d6()
        self.CHA = r4d6()
        self.MOVE = 4
        self.calc_stats()
        
        self.check_tiles()
     
        self.items = []
        self.spells = []

        self.av_fx = []
        self.dv_fx = []
        self.running_fx = []
        
        self.ch_drop_corpse = 33
        
        self.classkit = None
        self.dazzled = False
        
        self.armor = []
        self.weapon = None
        self.ammo = None
        self.unarmed_weapon = item_types.Unarmed(False)
        self.unconscious = False
        self.prone = False
        
    def calc_stats(self):
        self.CA = get_combat_actions(self.DEX)
        self.cur_CA = self.CA
        self.RA = self.CA
        self.cur_RA = self.RA
        self.DM = get_damage_mod(self.STR + self.SIZ)
        self.MP = self.POW
        self.SR = (self.INT + self.DEX) / 2
        self.HP = HitZones(self)
        self.hit_zones = HitZones(self)
        self.useless_zones = set()
        self.major_wounds = {}      
        self.skills = Skills(self)

    def get_STR(self):
        return self.STR    
    def get_CON(self):
        return self.CON
    def get_DEX(self):
        return self.DEX
    def get_SIZ(self):
        return self.SIZ
    def get_INT(self):
        return self.INT
    def get_POW(self):
        return self.POW
    def get_CHA(self):
        return self.CHA
    def get_DM(self):
        return self.DM
    def get_CA(self):
        return self.cur_CA
    def get_RA(self):
        return self.cur_RA
    def get_MOVE(self):
        return self.MOVE
    
    def gain_xp(self, amount):
        """The Actor's XP increases by the given amount"""
        self.xp += amount

    def get_av_fx(self):
        """Returns all Effects the Actor can trigger when attacking"""
        fx = [f for f in self.av_fx]
        for item in self.get_equipment():
            for f in item.av_fx:
                fx.append(f)
        return fx

    def get_dv_fx(self):
        """Returns all Effects the Actor can trigger when being attacked"""
        fx = [f for f in self.dv_fx]
        for item in self.get_equipment():
            for f in item.dv_fx:
                fx.append(f)
        return fx

    def redraw(self):
        """Clears the Surface so the image of the Actor will be redrawn"""
        self.cur_surf = None

    def clear_surfaces(self):
        """Set's all Surfaces to None to prevent Surface.Quit-Errors after unpickling"""
        for item in self.items:
            item.clear_surfaces()
        self.cur_surf = None
        Actor.tiles = None

    def go_prone(self, instantly=False):
        self.prone = True
        if not instantly:
            self.timer += 100 - self.get_MOVE() * 2

    def fall_unconscious(self):
        self.unconscious = True

    def serious_wound(self, zone):
        c, m, s, l = getattr(self.HP, zone)
        self.game.shout('%s has a serious wounded %s' % (self.name, s))

        for _ in xrange(d(4)):
            self.timer += 100 - self.get_MOVE() * 2

        
        if zone == 'R_Arm':
            item = self.weapon
            if item != None:
                self.take_off(item, instantly=True)
                self.drop(item, instantly=True)
        
        if zone == 'L_Arm':
            item = self.weapon
            if item != None and item.H2:
                self.take_off(item, instantly=True)
                self.drop(item, instantly=True)
            for item in self.get_equipment():
                if item.type == IF_SHIELD:
                    self.take_off(item, instantly=True)
                    self.drop(item, instantly=True)
                    break
        
        if zone in ('L_Leg', 'R_Leg'):
            self.go_prone(instantly=True)
        
        if zone in ('Abdomen', 'Chest', 'Head'):
            if d(100) > self.skills.Resilence:
                 self.fall_unconscious()
        
        self.useless_zones.add(zone)
    
    def major_wound(self, zone):
        c, m, s, l = getattr(self.HP, zone)
        self.game.shout('%s has a major wounded %s' % (self.name, s))
        
        if zone in ('R_Arm', 'L_Arm', 'L_Leg', 'R_Leg'):
            if d(100) > self.skills.Resilence:
                 self.fall_unconscious()
            self.go_prone(instantly=True)
            self.serious_wound(zone)
            self.major_wounds[zone] = self.CON + self.POW
            
        if zone in ('Abdomen', 'Chest', 'Head'):
            if d(100) > self.skills.Resilence:
                self.die()
            if d(100) > self.skills.Resilence:
                self.fall_unconscious()
            self.major_wounds[zone] = (self.CON + self.POW) / 2
            
        self.useless_zones.add(zone)
    
    def minor_wound(self,zone):
        c, m, s, l = getattr(self.HP, zone)
        self.game.shout('%s has a minor wounded %s' % (self.name, s))
        self.timer += 100 - self.get_MOVE() * 2
    
    def do_damage(self, dam, zone, type):
        """The Actor suffers the given amount of Damage"""
        if self.game.player == self:
            self.game.redraw_stats()

        cur_hp, max_hp, zone_desc, zone_flag = getattr(self.HP, zone)
        
        armors = [item for item in self.get_equipment() if item.locations & zone_flag]
        if len(armors) > 0:
            armors.sort(cmp=lambda x, y:y.AP - x.AP)
            dam = max(dam - armors[0].AP, 0)
            Debug.debug('%s reduces damage' % (armors[0].name))
            if dam == 0: return 0
            
        cur_hp -= dam
        setattr(self.HP, zone, (cur_hp, max_hp, zone_desc, zone_flag))
        
        if cur_hp == 0:
            self.minor_wound(zone)
        elif cur_hp < 0 and cur_hp > -max_hp:
            self.serious_wound(zone)
        elif cur_hp < 0:    
            self.major_wound(zone)

        return dam

    def read(self, item):
        """The Actor reads the given Item"""
        self.timer += 100 - self.get_INT() * 2
        item.read(item, self)

    def drink(self, item):
        """The Actor drinks the given Item"""
        self.items.remove(item)
        self.game.free_symbol(item.player_symbol)
        item.player_symbol = None
        self.game.del_item(item)
        self.timer += 100
        item.drink(item, self)
        
    def equip(self, item):
        if item.type == I_ARMOR:
            self.armor.append(item)        
        if item.type == I_WEAPON:
            if self.weapon != None:
                self.weapon.equipped = False
            self.weapon = item
              
        if item.type == I_AMMO:
            if self.ammo != None:
                self.ammo.equipped = False
            self.ammo = item
            
        self.timer += 200 - self.get_DEX() * 2
        Debug.debug('%s equipped %s' % (self.name, item.get_name()))
        item.equipped = True
        self.redraw()
        return True

    def take_off(self, item, instantly=False):
        if not instantly:
            self.timer += 200 - self.get_DEX() * 2
        item.equipped = False
        if item.type == I_ARMOR:
            self.armor.remove(item)
        if item.type == I_WEAPON:
            self.weapon = None
        if item.type == I_AMMO:
            self.ammo = None
        self.redraw()
        Debug.debug('%s took off %s' % (self.name, item.get_name()))
    
    def drop(self, item, instantly=False):
        self.items.remove(item)
        self.game.add_item(item)
        item.picked_up = False
        if not instantly:
            self.timer += max(50 - self.DEX * 2, 0)
        self.game.free_symbol(item.player_symbol)
        item.player_symbol = None
    
    def throw(self, item, pos):
        item.equipped = False
        item.picked_up = False
        self.game.add_item(item)
        if item == self.weapon:
            self.weapon = None
            self.redraw()
        self.items.remove(item)
        self.game.throw_item(self, item, pos)
    
    def fire(self, pos):
        self.timer += 100 * (5 - self.get_CA())
        if not self.ammo.used():
            self.items.remove(self.ammo)
            self.game.del_item(self.ammo)
        self.game.range_attack(self, pos)
        
    def cast(self, spell):
        if self.cur_endurance < spell.phys_cost: return False
        if self.mind < spell.mind_cost: return False
        self.cur_endurance -= spell.phys_cost
        self.cur_mind -= spell.mind_cost
        self.timer += 100 * (5 - self.get_CA())
        return spell.cast(self)
    
    def get_equipment(self):
        return [item for item in self.items if item.equipped]
    
    def pick_up(self, item):
        self.timer += max(100 - self.DEX * 2, 0)
        symbol = item.get_ps()
        if item.type == I_GOLD:
            self.gold += item.amount
            self.game.free_symbol(symbol)
        else:
            stacked = False
            if item.amount > 0:
                l = []
                l.extend(self.get_equipment())
                l.extend(self.items)
                for i in l:
                    if item.pop_name == i.pop_name:
                        i.amount += item.amount
                        stacked = True
                        self.game.free_symbol(symbol)
                        break
            if not stacked:
                self.items.append(item)
                if self == self.game.player:
                    #item.player_symbol = self.game.get_symbol()
                    self.game.shout('You picked up a %s' % (item.get_name()))
                else:
                    self.game.free_symbol(symbol)
                    
        self.game.del_item(item)
        item.picked_up = True
        Debug.debug('%s picked up %s' % (self.name, item.get_name()))

    def check_tiles(self):
        if Actor.tiles == None:
            Actor.tiles = Res('dc-mon.png', TILESIZE)
    
    def die(self, text=None):
        self.game.del_actor(self)
        if d(100) < self.ch_drop_corpse:
            self.__drop_corpse()
        for item in self.get_equipment():
            self.take_off(item)
            self.drop(item)
        for item in self.items:
            self.drop(item)
        if self.gold > 0:
            self.game.create_gold(self.gold, self.pos())
        if text == None:
            self.game.shout('%s dies' % (self.name))
        else:
            self.game.shout('%s dies of %s' % (self.name, text))
        if self.game.player == self:
            self.game.game_over()
        
        
    def __drop_corpse(self):
        Corpse(self)
    
    def equip_melee(self):
        melee_weapons = []
        if self.slot.weapon.flags & IF_MELEE:
            melee_weapons.append(self.slot.weapon)
        for item in self.items:
            if item.flags & IF_MELEE:
                melee_weapons.append(item)
        if len(melee_weapons) > 0:
            #melee_weapons.sort(cmp=lambda x, y: y.av - x.av)
            weapon = melee_weapons[0]
            if weapon.type != I_VOID:
                self.equip(weapon)
            else:
                self.take_off(self.slot.weapon)
            
        
    def equip_range(self):
        range_weapons = []
            
        for item in self.items:
            if item.flags & IF_RANGED:
                range_weapons.append(item)
        
        ammos = []
        for item in self.items:
            if item.type == I_AMMO:
                ammos.append(item)

        for weapon in range_weapons:
            for ammo in ammos:
                    if ammo_fits_weapon(ammo, weapon):
                    #((ammo.flags & IF_ARROW and weapon.flags & IF_FIRES_ARROW) or 
                    #    (ammo.flags & IF_BOLT and weapon.flags & IF_FIRES_BOLT)):
                        if weapon.type != I_VOID:
                            self.equip(weapon)
                        else:
                            self.take_off(self.slot.weapon)
                        self.equip(ammo)
                        return

    def melee_equipped(self):
        weapon = self.weapon
        melee_weapons = []
        for item in self.items:
            if item.flags & IF_MELEE:
                melee_weapons.append(item)
        
        if weapon == None:
            if len(melee_weapons) > 0:
                return False
            else:
                return True
        
        if weapon.flags & IF_MELEE:
            return True
        
        return False
            
    def range_equipped(self):
        weapon = self.weapon
        if self.weapon == None: return False
        if weapon.flags & IF_RANGED:
            ammo = self.ammo
            if ammo == None: return False
            if ammo_fits_weapon(ammo, weapon):
                return True
        return False
        
    def ready_to_range(self):
        range_weapons = []
        
        for item in self.items:
            if item.flags & IF_RANGED:
                range_weapons.append(item)
        
        ammos = []
        if self.ammo != None:
            ammos.append(self.ammo)
            
        for item in self.items:
            if item.__class__.__name__ == 'Ammo':
                ammos.append(item)

        for weapon in range_weapons:
            for ammo in ammos:
                if ammo_fits_weapon(ammo, weapon): 
                #((ammo.flags & IF_ARROW and weapon.flags & IF_FIRES_ARROW) or 
                #    (ammo.flags & IF_BOLT and weapon.flags & IF_FIRES_BOLT)):
                    return True
        
        return False
    
    def get_body_tile(self):
        surf = pygame.Surface((TILESIZE, TILESIZE))#, pygame.SRCALPHA, 32) 
        surf.blit(self.tiles.get_subs(self.img_body), (0, 0))
        return surf
    
    def get_tile(self):
         
        self.check_tiles()
        
        surf = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA, 32)        
        
        surf.blit(self.tiles.get_subs(self.img_body), (0, 0))

        #if self.armor != None:
        #    surf.blit(self.armor.get_eq_img(), (TILESIZE / 4, 0))
        if self.weapon != None:
            surf.blit(self.weapon.get_eq_img(), self.weapon.blit_pos)
        
        for armor in self.armor:
            surf.blit(armor.get_eq_img(), armor.blit_pos)
            (TILESIZE / 2, 0)
        #surf.blit(self.slot.weapon.get_eq_img(), (0, 0))
        #surf.blit(self.slot.head.get_eq_img(), (TILESIZE / 4, 0))
        
        return surf

    def pos(self):
        return self.x, self.y
   
    def set_pos(self, pos):
        self.game.update_actor_pos(self, pos)
        self.x = pos[0]
        self.y = pos[1]
        [item.set_pos(self.pos()) for item in self.items]
        
    def tick(self):
        
        self.dazzled = False
        #self.useless_zones = set()
        #self.major_wounds = {} 
        for zone in self.useless_zones:
            if zone in ('Abdomen', 'Chest', 'Head'):
                if d(100) > self.skills.Resilence:
                    self.fall_unconscious()
        
        for zone in self.major_wounds.keys():
            if self.major_wounds[zone] == 0:
                self.die("bloodloss and internal injuries")
                break
            else:    
                if zone in ('Abdomen', 'Chest', 'Head'):
                    if d(100) > self.skills.Resilence:
                        self.die("bloodloss and internal injuries")
                        break
                    if d(100) > self.skills.Resilence:
                        self.fall_unconscious()
                else:
                    if d(100) > self.skills.Resilence:
                        self.fall_unconscious()
                
                self.major_wounds[zone] -= 1
            
        
        for e in self.running_fx:
            e.tick()
        
                    
    def act(self):
        self.cur_RA = self.RA
        if not self.unconscious:
            if self.ai != None:
                self.ai.act()
        else:
            self.move(MOVE_WAIT)
            self.game.shout('%s is unconscious' % (self.name))
                
    def opposite_dir(self, target):
        if hasattr(target, 'x'):
            tx = target.x
            ty = target.y
        else:
            tx = target[0]
            ty = target[1]
        
        if self.x > tx:
            if self.y == ty:
                move_d = MOVE_RIGHT
            elif self.y > ty:
                move_d = MOVE_DOWN_RIGHT
            else:
                move_d = MOVE_UP_RIGHT
        
        if self.x < tx:
            if self.y == ty:
                move_d = MOVE_LEFT
            elif self.y > ty:
                move_d = MOVE_DOWN_LEFT
            else:
                move_d = MOVE_UP_LEFT
                
        if self.x == tx:
            if self.y > ty:
                move_d = MOVE_DOWN
            else:
                move_d = MOVE_UP
        
        return move_d

    def locateDirection(self, target):    
        """Checks in what direction the target is"""

        if hasattr(target, 'x'):
            tx = target.x
            ty = target.y
        else:
            tx = target[0]
            ty = target[1]
        
        if self.x > tx:
            if self.y == ty:
                move_d = MOVE_LEFT
            elif self.y > ty:
                move_d = MOVE_UP_LEFT
            else:
                move_d = MOVE_DOWN_LEFT
        
        if self.x < tx:
            if self.y == ty:
                move_d = MOVE_RIGHT
            elif self.y > ty:
                move_d = MOVE_UP_RIGHT
            else:
                move_d = MOVE_DOWN_RIGHT
                
        if self.x == tx:
            if self.y > ty:
                move_d = MOVE_UP
            else:
                move_d = MOVE_DOWN
        
        return move_d

    def move(self, direction):
        if direction == MOVE_WAIT:
            self.timer += 100 - self.get_MOVE() * 2
            return True
        
        new_pos = get_new_pos(self.pos(), direction)
        
        result = self.game.is_move_valid(self, new_pos)
        
        if result == True:
            self.set_pos(new_pos)
            self.timer += 100 - self.get_MOVE() * 2
            return True
             
        if isinstance(result, Actor):
            if result != self:
                if result.id in self.ai.friends:
                    if self == self.game.player:
                        result.set_pos(self.pos())
                        self.set_pos(new_pos)
                        self.timer += 100 - self.get_MOVE() * 2
                        result.timer += 100 - result.get_MOVE() * 2
                        self.game.shout('You displaced %s' % (result.name))
                        self.sc.do_fov(self.x, self.y, 15)
                        return True
                    else:
                        return False                    
                self.game.attack(self, result)
                self.timer += 100 * (5 - self.get_CA())
                return result
        
        return False

class Humanoid(Actor):
    
    tiles = None

    def __init__(self, add):
        Actor.__init__(self, add)
        self.t = None
        self.check_tiles()
        self.img_body = 1, 0
        self.name = 'Player'

    def check_tiles(self):
        if Humanoid.tiles == None:
            Humanoid.tiles = Res('dc-pl.png', TILESIZE)
        
    def get_tile(self):
        self.check_tiles()
        return Actor.get_tile(self)
    
    def clear_surfaces(self):
        Actor.clear_surfaces(self)
        for item in self.items:
            item.clear_surfaces()
        self.cur_surf = None
        Humanoid.tiles = None
