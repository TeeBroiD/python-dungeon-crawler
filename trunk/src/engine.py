import pygame
import random
import os
import sys
import gzip

try:
    import cPickle as pickle
except:
    import pickle

import gc
import dungeon
import magic
 
from pygame import *
from weakref import WeakKeyDictionary

from gfx import *
from ai import AI
from pdcglobal import *
from pdcresource import *
from key_mapping import *
from shadowcast import sc
from camera import Camera
from item import Item
from cursor import Cursor
from actor.races import races
from actor.classes import classkits
from actor.actor import Actor, Humanoid
from eng_player_actions import *
from eng_state_worker import *
from flame import *
import att
         
class Engine(object):
    
    __world_objects = WeakKeyDictionary()
    
    def __init__(self):
        self.__message_queue = []
        self.__cur_stat_surf = None
        self.map = None
        self.__actors = []
        self.__items = []
        self.__gfx = None
        self.__quit_loop = False
        self.__last_id = 0
        self.__id_gen = self.__gen_id()
        self.__actors_on_screen = []
        self.dungeon = dungeon.DungeonsOfGogadan()
        self.quit_mes = QUIT
        self.timer = 0
        self.world_time = 0
        
        self.stats = [att.Att('Strength', 'Important for Melee-Fighter', 20),
                      att.Att('Endurance', 'Important for Melee-Fighter'),
                      att.Att('Mind', 'Important for Spellcaster'),
                      att.Att('Health', 'How much can you take?', 45)]
                
        self.__load_fonts()
        self.__build_surf_cache()
        self.__set_game_instance()
        
        self.player_actions = PlayerActions(self)
        self.state_worker = StateWorker(self)
        self.camera = Camera(20, 26)
        self.state = S_RUN
        self.wait_for_target = None
        
        Debug.init_debug(self)
        Debug.debug('init pygame')

        pygame.init()
        self.screen = pygame.display.set_mode((1024, 768))
        self.__clock = pygame.time.Clock()
        
        self.cursor = Cursor(self)
                
        #self.player = Humanoid(True)
#        i = dungeon.Populator.create_item('Flail', 'basic_weapons', 2)
#        c = dungeon.Populator.create_item('Chainmail', 'basic_stuff', 2)
#        t = dungeon.Populator.create_item('Trousers', 'basic_stuff', 2)
#        self.player.items.append(i)
#        self.player.items.append(c)
#        self.player.items.append(t)
#        self.player.equip(i)
#        self.player.equip(c)
#        self.player.equip(t)
#        self.player.spells.append(magic.Regeneration())
#        self.player.spells.append(magic.FoulnessRay())
#        self.player.spells.append(magic.FrostRay())
#        self.player.spells.append(magic.Identify())
        self._items_to_choose = {}
        

    def re_init(self):
        Debug.debug('re_init')
        self.__quit_loop = False
        self.quit_mes = QUIT
                
        self.__load_fonts()
        self.__build_surf_cache()
        self.__set_game_instance()
        self.__clock = pygame.time.Clock()
        self.__id_gen = self.__gen_id()
        for act in self.__actors:
            self.__world_objects[act] = True
        for item in self.__items:
            self.__world_objects[item] = True
        self.__world_objects[self.map] = True
        self.__clear_surfaces()
        if hasattr(self, 'map'):
            self.redraw_map()
        
    def get_actor_at(self, pos):
        for actor in self.__actors:
            if actor.pos() == pos:
                return actor
        return None
    def get_all_srd_actors(self, pos, radius=1, null_pos=False):
        mo = []
        for x in xrange(-radius, radius + 1):
            for y in xrange(-radius, radius + 1):
                mo.append((x, y))
        
        if not null_pos:
            mo.remove((0, 0))
        
        poss = []
        for m in mo:
            poss.append((m[0] + pos[0], m[1] + pos[1]))
        
        actors = []
        for act in self.__actors:
            if act.pos() in poss:
                actors.append(act)
        return actors
    def get_free_adj(self, pos):
        new_pos = None
        mo = [(-1, -1), (-1, 0), (-1, 1),
              (1, -1), (1, 0), (1, 1),
              (0, -1), (0, 1)]

        random.shuffle(mo) 
        while new_pos == None and len(mo) > 0: 
            t = mo.pop()
            new_pos = pos[0] + t[0], pos[1] + t[1]
            
            if not self.map.map_array[new_pos[1]][new_pos[0]][MT_FLAGS] & F_WALKABLE:
                new_pos = None
            else:
                for actor in self.__actors:
                    if actor.pos() == new_pos:
                        new_pos = None
                        break
        
        return new_pos
    def get_sc_up_pos(self):
        y = 0
        x = 0
        pos = None
        for line in self.map.map_array:
            x = 0
            for t in line:
                if t == MAP_TILE_up:
                    pos = x, y
                x += 1
            y += 1
        return pos if pos != None else self.map.get_random_pos()
    def get_sc_down_pos(self):
        y = 0
        x = 0
        pos = None
        for line in self.map.map_array:
            x = 0
            for t in line:
                if t == MAP_TILE_down:
                    pos = x, y
                x += 1
            y += 1
        return pos if pos != None else self.map.get_random_pos()
    def shout(self, text):
        self.__message_queue.insert(0, text)
    def change_map(self, down=True):
        
        if self.map == None:
            level = 1 
        elif down:
            level = self.map.level + 1
            self.__save_map()
        else:
            level = self.map.level - 1
            self.__save_map()

        if self.__load_map(level):
            return
        if level == 0:
            self.game_over()    
        
        self.__actors = []
        self.__actors.append(self.player)
        self.__items = []
        self.map = self.dungeon.get_map(level)
        
        self.sc = sc(self.map.map_array)
        if down:
            pos = self.get_sc_up_pos()
        else:
            pos = self.get_sc_down_pos()
        self.player.set_pos(pos)
            
        r = self.camera.adjust(self.player.pos())
        while r:
            r = self.camera.adjust(self.player.pos())
    
    def create_character(self):
        c_res = Res('dc-pl.png', TILESIZE)
        g = 'female', 'male'
        gender = 1
        race = 0
        classkit = 0
        OK = False
        name = ''
        title = 'He'
        title2 = 'His'
        story = ['This is the incredible story of our hero',
               'Long time ago, there was a hero named',
               'There once was a time, long ago, when']
        
        s = random.choice(story)
        
        while not OK:
            self.screen.fill(BLACK)
            
            self.__render_text(self.screen, 'Build your character:', WHITE, ((35, 30)), 'big')
            
            self.screen.blit(self.__surf_cache['mes_block2'], (60, 65))
            
            
            img = pygame.transform.smoothscale(c_res.get(races[race][1 + gender]), (TILESIZE * 2, TILESIZE * 2))
            self.screen.blit(img , (75, 100))
            
            
            self.__render_text(self.screen, name, WHITE, ((73, 170)))
            
            y = 100
            self.__render_text(self.screen, s, WHITE, ((145, y)))
            self.__render_text(self.screen, name, GREEN, ((395, y)))
            y += 20
            self.__render_text(self.screen, 'the' , WHITE, ((145, y)))
            self.__render_text(self.screen, g[gender] + ' ' + races[race][0] + ' ' + classkits[classkit][0] + '.', GREEN, ((167, y)))
            y += 20
            self.__render_text(self.screen, title + ' ' + races[race][3].desc, WHITE, ((145, y)))
            y += 20
            self.__render_text(self.screen, classkits[classkit][1].desc.replace('$$$', title.lower()).replace('%%%', title2.lower()), WHITE, ((145, y)))
            
            
            self.__render_text(self.screen, 'Type in your name', WHITE, ((600, 100)))
            self.__render_text(self.screen, 'press F1 / F2 to change race', WHITE, ((600, 120)))
            self.__render_text(self.screen, 'press F3 / F4 to change class', WHITE, ((600, 140)))
            self.__render_text(self.screen, 'press F5 to change gender', WHITE, ((600, 160)))
            self.__render_text(self.screen, 'press Enter to start', WHITE, ((600, 180)))
            
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_F5:
                        if gender == 1:
                            gender -= 1
                            title = 'She'
                            title2 = 'Her'
                        else:
                            gender += 1
                            title = 'He'
                            title2 = 'His'
                    if e.key == pygame.K_F3:
                        classkit += 1
                        if classkit >= len(classkits):
                            classkit = 0
                    elif e.key == pygame.K_F4:
                        classkit -= 1
                        if classkit < 0:
                            classkit = len(classkits) - 1
                    
                    elif e.key == pygame.K_F1:
                        race += 1
                        if race >= len(races):
                            race = 0
                    elif e.key == pygame.K_F2:
                        race -= 1
                        if race < 0:
                            race = len(races) - 1
                            
                    elif e.key == pygame.K_RETURN:
                        self.player = races[race][3](True, gender)
                        self.player.classkit = classkits[classkit][1](self.player)
                        self.player.clear_surfaces()
                        OK = True
                    elif e.key == pygame.K_BACKSPACE:
                        if len(name) > 0:
                            name = name[:-1]
                    else:
                        kn = pygame.key.name(e.key)
                        if kn in 'abcdefghijklmnopqrstuvwxyz' and len(name) < 10:
                            if len(name) > 0:
                                name += pygame.key.name(e.key)
                            else:
                                name += pygame.key.name(e.key).upper()
 
        
        
    
    def start(self, ts):
        
        if ts:
            self.create_character()
            self.change_map()
            
        Debug.debug('starting mainloop')
        return self._main_loop()
    
    def is_move_valid(self, actor, old_pos, new_pos, move_mode):
        if new_pos[0] < 0 or new_pos[1] < 0 or new_pos[0] >= self.map.width or new_pos[1] >= self.map.height:
            return False   
        for act in self.__actors:
            if actor != act and act.pos() == new_pos:
                return act
            
        valid = self.map.is_move_valid(old_pos, new_pos, move_mode)
        if valid:
            if actor == self.player: 
                self.map.cur_surf = None    
                items = self.get_items_at(new_pos)
                if len(items) == 1:
                    self.shout('You see a %s' % (items[0].get_name()))
                if len(items) > 1:
                     self.shout('You see several items here')
        return valid
    
    def get_range_target(self, cpos, tpos):
        return self.get_actor_at(tpos)
#        if cpos != tpos:
#            poss = line(cpos[0], cpos[1], tpos[0], tpos[1])
#            poss.pop(0)
#            for pos in poss:
#                actor = self.get_actor_at(pos)
#                if actor != None:
#                    return actor
#        else:
#            return self.caster
#        return None
    
    def range_attack(self, attacker, target_pos):
        t_pos = target_pos
        s_pos = attacker.pos()
        victim = self.get_range_target(attacker.pos(), target_pos)
        
        if victim != None:
            t_pos = victim.pos()
                
        dir = attacker.locateDirection(t_pos)
        gfx = projectile.ProjectileFX(dir, s_pos, t_pos)
        self.drawGFX(gfx)
        
        #while self.__gfx != None:
        #    self._world_draw()
        
        if victim != None:
            self.attack(attacker, victim, True)
        
    def attack(self, attacker, victim, ranged=False):
        defence = victim.get_total_dv()
        attack = attacker.get_total_av()
        attack += d(100) + d(50)
        defence += 100 + d(100)
        Debug.debug('%s Attack: %i' % (attacker.name, attack))
        Debug.debug('%s Defense: %i' % (victim.name, defence))
        
        if victim == self.player:
            vi_adress = 'you'
        else:
            vi_adress = 'the ' + victim.name
        if attack >= defence:
            for fx in attacker.get_av_fx():
                if d(100) <= fx[1]:
                    Debug.debug('Applied effect %s to %s by %s' % (fx[0], victim, attacker))
                    f = fx[0](victim, attacker)
                    f.tick()
            
            for fx in victim.get_dv_fx():
                skip = False
                for nt in fx[0].notrigger:
                    if attacker.slot.weapon.flags & nt:
                        skip = True
                
                if not skip and d(100) <= fx[1]:
                    Debug.debug('Applied effect %s to %s by %s' % (fx[0], attacker, victim))
                    f = fx[0](attacker, victim)
                    f.tick()
            
            min = attacker.get_total_min_damage(ranged)
            max = attacker.get_total_max_damage(ranged)
            while max <= min:
                max += 1
            damage = random.randint(min, max)
            
            en_shield = victim.cur_endurance / 20
            damage -= en_shield
            if damage < 1:
                damage = 1
            
            victim.lose_endurance(en_shield)
            
            Debug.debug('Hit for %i damage!' % (damage))
            killed = self.do_damage(victim, damage, attacker.slot.weapon.damage_type, attacker)
            if attacker == self.player:
                at_adress = 'You hit'
            else:
                at_adress = 'The ' + attacker.name + ' hits'
            self.shout('%s %s for %i damage.' % (at_adress, vi_adress, damage))
            if killed:
                if attacker == self.player:
                    at_adress = 'You killed'
                else:
                    at_adress = 'The ' + attacker.name + ' killed'
                self.shout('%s %s' % (at_adress, vi_adress))
        else:
            if attacker == self.player:
                at_adress = 'You miss'
            else:
                at_adress = attacker.name + ' misses'
            
            self.shout('%s %s.' % (at_adress, vi_adress))
            Debug.debug('Miss!')
            
        attacker.lose_endurance(1,True)
        victim.lose_endurance(1,True)
    def do_damage(self, act, dam, type=D_GENERIC, source=None):
        deadly = act.do_damage(dam, type)
        if deadly and source != None:
            source.gain_xp(act.xp_value)
            
        
    def get_items_at(self, pos):
        return [item for item in self.__items if item.pos() == pos]
    def game_over(self):
        print 'You failed'
        self.__quit_loop = True
        self.__actors = []
    
    def redraw_map(self):
        self.map.cur_surf = None
    def redraw_stats(self):
        self.__cur_stat_surf = None
    
    def add_to_world_objects(self, obj):
        self.__world_objects[obj] = True
    def add_actor(self, actor, add=True):
        if add: self.__actors.append(actor)
        self.__world_objects[actor] = True
    def add_item(self, item, add=True):
        if add: self.__items.append(item)
        self.__world_objects[item] = True
    def del_actor(self, actor):
        if actor in self.__actors:
            self.__actors.remove(actor)
        if actor in self.__actors_on_screen:
            self.__actors_on_screen.remove(actor)
    def del_item(self, item):
        if item in self.__items:
            self.__items.remove(item)
    def get_id(self):
        return self.__id_gen.next()
    
    def drawGFX(self, gfx):
        self.__gfx = gfx
        self.state = S_GFX
        
        # good or bad??
        while self.__gfx != None:
            self._world_draw()
    
    def target_choosen(self, pos):
        self.player.fire(pos)
    
    def _main_loop(self):
        while not self.__quit_loop:
            self.__clock.tick(40)
            self._world_move()
            self._world_draw()
            self._world_input()
#            print self.clock.get_fps()
        self.std_font = None
        self.__clock = None
        self.__cur_stat_surf = None
        self.__last_id = self.__id_gen.next()
        self.__id_gen = None
        self.__clear_surfaces()
        return self.quit_mes
    def _world_input(self):
        for e in pygame.event.get():
            self.__quit_loop = e.type == pygame.QUIT 
            
            if e.type == pygame.KEYDOWN:
                
                if e.key == GAME_SAVE_QUIT:
                    self.__quit_loop = True
                    self.quit_mes = SAVE
                
                # --- cheat keys >>>
                if e.key == pygame.K_F1:
                    for line in self.map.map_array:
                        l = ''
                        for s in line:
                            l = l + str(s[0])
                        print l    
                
                if e.key == pygame.K_F2:
                    self.player.cur_health = 200
                    self.player.cur_endurance = 5000
                    self.player.cur_mind = 5000
                    self.player.cur_strength = 5000
                    
                if e.key == pygame.K_F3:
                    for item in self.__items:
                        print item.name, item.pos()

                if e.key == pygame.K_F4:                        
                    for act in self.__actors:
                        print act.name, act.timer
                              
                if e.key == pygame.K_F5:
                    for S in gc.get_referrers(Surface):
                        if isinstance(S, Surface):
                            print S

                    print gc.get_referrers(Surface)      
                # <<< cheat keys ---
                
                if not self.state == S_GFX:
                    self.__cur_stat_surf = None
                self.moved = True
                
                if e.key == ACTION_MEDITATE:
                    self.shout('You start to meditate')
                    self.player.timer += 5000
                
                if self.state == S_RUN:
                    if e.key in PLAYER_ACTIONS: 
                        self.player_actions.__getattribute__(PLAYER_ACTIONS[e.key])()

                elif self.state in STATE_WORKER:
                    self.state_worker.__getattribute__(STATE_WORKER[self.state])(e.key)

        if self.state == S_PLAYER_CURSOR:
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            for key in MOVES:
                if keys[key]:
                    pygame.time.wait(150)
                    if key == MOVE_WAIT:
                        pos = self.__actors_on_screen[0].pos()
                        if pos == self.cursor.pos():
                            self.__actors_on_screen.append(self.__actors_on_screen.pop(0))
                            pos = self.__actors_on_screen[0].pos()
                        self.cursor.set_pos(pos)
                        self.__actors_on_screen.append(self.__actors_on_screen.pop(0))
                    else:
                        self.cursor.move(key)

        if self.state == S_RUN:
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            [self.player.move(key) for key in MOVES if keys[key] and self.player.timer <= 0]
    def _world_move(self):
        if self.state == S_RUN:
            self.__actors.sort(sort_by_time) #actors with lowest timer first
            diff = self.__actors[0].timer
            self.timer += diff
            self.world_time += diff
            
            if self.timer > 1500:             #act-independent issues
                [act.tick() for act in self.__actors]
                self.timer -= 1500
                    
            for actor in self.__actors:
                if actor.timer > 0:
                    actor.timer -= diff
                else:
                    actor.act()
            
        elif self.state == S_GFX:
           if self.__gfx == None:
                self.state = S_RUN
    def _world_draw(self):

        if self.__gfx == None or self.__gfx.redraw:

            if self.camera.adjust(self.player.pos()):
                self.map.cur_surf = None
            self.screen.fill((0, 0, 0))
            if not self.player.dazzled:
                self.screen.blit(self.__get_map_surface(), (-self.camera.x * TILESIZE, -self.camera.y * TILESIZE))
            
                    
            if not self.player.dazzled:
                for item in self.__items: 
                    if not item.picked_up and (self.sc.lit(item.x, item.y) or self.player.x == item.x and self.player.y == item.y):
                        try:
                            self.screen.blit(self.__get_item_surface(item), (item.x * TILESIZE - self.camera.x * TILESIZE, item.y * TILESIZE - self.camera.y * TILESIZE))
                        except:
                            print sys.exc_info()
                            print item.name, item.pos(), 'is invalid!!!!'
            
            for act in self.__actors:
                if  act == self.player or self.sc.lit(act.x, act.y) and not self.player.dazzled:
                    try:
                        self.screen.blit(self.__get_actor_surface(act), (act.x * TILESIZE - self.camera.x * TILESIZE, act.y * TILESIZE - self.camera.y * TILESIZE))
                        if not act in self.__actors_on_screen:
                            self.__actors_on_screen.append(act)
                    except:
                        print sys.exc_info()
                        print act.name, act.pos(), 'is invalid!!!!'
                else:
                    if act in self.__actors_on_screen:
                        self.__actors_on_screen.remove(act)
                    
            if self.state == S_PLAYER_CURSOR:
                self.screen.blit(self.cursor.get_surf(), (self.cursor.x * TILESIZE - self.camera.x * TILESIZE, self.cursor.y * TILESIZE - self.camera.y * TILESIZE))
            
            self.screen.blit(self.__get_message_surface(), (0, 768 - 128))
            self.screen.blit(self.__get_statblock_surface(), (1024 - 192, 0))
    
        if self.__gfx != None:
            pos = self.__gfx.pos()
            if pos == None:
                self.__gfx = None
                self.__cur_stat_surf = None
            else:
                self.screen.blit(self.__gfx.get_surf(), pos)
                self.__gfx.tick()
            
        pygame.display.flip()

    def __get_map_surface(self):
        if self.map.cur_surf == None:
            self.sc.do_fov(self.player.x, self.player.y, self.player.cur_mind / 20 + 7)
            surf_map = pygame.Surface((self.map.width * TILESIZE, self.map.height * TILESIZE))
            cx, cy, cw, ch = self.camera.get_view_port()       
            for x in xrange(max(cx, 0), min(self.map.width, cw + 1)):

                for y in xrange(max(cy, 0), min(self.map.height, ch + 1)):
                    pos = (x, y) == self.player.pos() 
                    lit = self.sc.lit(x, y)
                    memo = self.map.map_array[y][x][MT_FLAGS] & F_MEMO
                    if pos or lit or memo:
                        blit_position = ((x) * TILESIZE, (y) * TILESIZE)
                        surf_map.blit(self.map.get_tile_at(x, y), blit_position)
                        
                        if not pos and not lit and memo:
                            surf_map.blit(self.__surf_cache['FOW'], blit_position)
                        
                        if not self.map.map_array[y][x][MT_FLAGS] & F_MEMO:
                            tile = self.map.map_array[y][x]
                            new_tile = tile[0], tile[1], tile[2] ^ F_MEMO
                            self.map.map_array[y][x] = new_tile

            self.map.cur_surf = surf_map
        
        return self.map.cur_surf
    def __get_actor_surface(self, act):
        if act.cur_surf == None:
            surf_act = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA, 32)
            surf_act.blit(act.get_tile(), (0, 0)) 
            act.cur_surf = surf_act
        return act.cur_surf
    def __get_item_surface(self, item):
        if item.cur_surf == None:
            surf_item = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA, 32)
            surf_item.blit(item.get_dd_img(), (0, 0)) 
            item.cur_surf = surf_item
        return item.cur_surf
    def __get_message_surface(self):
        surf = pygame.Surface((1024 - 192, 128))
        surf.blit(self.__surf_cache['mes_block'], (0, 0))
        y = 100
        for mes in self.__message_queue:
            self.__render_text(surf, mes, WHITE, (20, y))
            y -= 20
            if y < 10:
                break
        return surf
    def __get_statblock_surface(self):
        if self.__cur_stat_surf == None:
            surf = pygame.Surface((192, 768))
            surf.blit(self.__surf_cache['stat_block'], (0, 0))
            
            if self.state in (S_RUN, S_GFX):
                self.__draw_stat_block(surf)    

            if self.state in CHOOSE_STATES:
                self.__draw_item_choose(surf, CHOOSE_STATES[self.state])
            
            self.__cur_stat_surf = surf
            
        return self.__cur_stat_surf
    
    def __set_game_instance(self):
        dungeon.Map.game = self
        Actor.game = self
        Item.game = self
        AI.game = self
        Camera.game = self
        dungeon.Populator.game = self
        magic.Spell.game = self
        GFX.game = self
        att.Att.game = self
        dungeon.SADungeon.game = self
    def __draw_item_choose(self, surf, message):
        self.__render_text(surf, message, WHITE, (16, 20))
        y = 38
        abc = self._items_to_choose.keys()
        #abc.sort(sort_by_type)
        for key in abc:
            item = self._items_to_choose[key]
            color = WHITE
            if hasattr(item, 'special'):
                if item.special:
                    color = GREEN
            if hasattr(item, 'color'):
                color = item.color    
            if hasattr(item, 'get_name'):
                name = item.get_name()
            else:
                name = item.name
            
            self.__render_text(surf, '%s -' % (key), WHITE, (16, y))
            self.__render_text(surf, name, color, (32, y)); y += 18
            
            info = item.info()
            for line in info:
                self.__render_text(surf, line, color, (32, y)); y += 18
            
    def __draw_stat_block(self, surf):
        s48 = pygame.Surface.copy(self.__surf_cache['stat_48'])
        
        head = pygame.transform.smoothscale(self.player.slot.head.get_dd_img(), (48, 48))
        surf.blit(s48, (192 / 2 - 24, 16))
        surf.blit(head, (192 / 2 - 24, 16))
                
        shield = pygame.transform.smoothscale(self.player.slot.shield.get_dd_img(), (48, 48))
        surf.blit(s48, (192 / 2 + 32, 72))
        surf.blit(shield, (192 / 2 + 32, 72))
                
        weapon = pygame.transform.smoothscale(self.player.slot.weapon.get_dd_img(), (48, 48))
        surf.blit(s48, (192 / 2 - 80, 72))
        surf.blit(weapon, (192 / 2 - 80, 72))
        
        if hasattr(self.player.slot, 'trousers'):
            trousers = pygame.transform.smoothscale(self.player.slot.trousers.get_dd_img(), (48, 48))
            surf.blit(s48, (192 / 2 + 32, 126))
            surf.blit(trousers, (192 / 2 + 32, 126))
        
        ammo = pygame.transform.smoothscale(self.player.slot.ammo.get_dd_img(), (48, 48))
        surf.blit(s48, (192 / 2 - 80, 126))
        surf.blit(ammo, (192 / 2 - 80, 126))
        self.__render_text(surf, str(self.player.slot.ammo.amount), WHITE, (20, 128))
        
        armor = pygame.transform.smoothscale(self.player.slot.armor.get_dd_img(), (48, 48))
        surf.blit(s48, (192 / 2 - 24, 126))
        surf.blit(armor, (192 / 2 - 24, 126))
        
        cloak = pygame.transform.smoothscale(self.player.slot.cloak.get_dd_img(), (48, 48))
        surf.blit(s48, (192 / 2 - 24, 72))
        surf.blit(cloak, (192 / 2 - 24, 72))
        
        if hasattr(self.player.slot, 'boots'):
            boots = pygame.transform.smoothscale(self.player.slot.boots.get_dd_img(), (48, 48))
            surf.blit(s48, (192 / 2 - 24, 184))
            surf.blit(boots, (192 / 2 - 24, 184))
                    
        stats = [('Str: ', self.player.strength, self.player.cur_strength, self.player.strength_heal),
                 ('End: ', self.player.endurance, self.player.cur_endurance, self.player.endurance_heal),
                 ('Mnd: ', self.player.mind, self.player.cur_mind, self.player.mind_heal),
                 ('Spd: ', self.player.speed, self.player.cur_speed, self.player.speed_heal),
                 ('Hlt: ', self.player.health, self.player.cur_health, self.player.health_heal)]
        y = 235
        for line in stats:
            r = pygame.Surface((100, 2))
            r.fill(RED)
            surf.blit(r, (16, y + 20))
            size = float(line[2]) / float(line[1]) * 100
            if size > 0:
                g = pygame.Surface((size, 2))
                if size > 100:
                    g.fill(BLUE)
                else:
                    g.fill(GREEN)
                    
            surf.blit(g, (16, y + 20))
            self.__render_text(surf, str(line[0]).rjust(3, ' '), WHITE, (16, y)); 
            self.__render_text(surf, str(line[2]).rjust(3, ' '), GREEN, (55, y)); 
            self.__render_text(surf, '/', WHITE, (80, y));
            self.__render_text(surf, str(line[1]).rjust(3, ' '), WHITE, (95, y));
            d = ''
            for _ in xrange(line[3]):
                d += '+'
            self.__render_text(surf, d, GREEN, (120, y));
            y += 22
        
        #y+=18
        #self.__render_text(surf, 'Alignment:', WHITE, (16, y));y+=18
        
        #sp = self.player.align_co+3
        #a=''
        #for x in xrange(0,8):
        #    if x==sp:
        #        a+='+'
        #    else:
        #        a+='-'
        
        #self.__render_text(surf, 'Chaos', WHITE, (16, y));
        #self.__render_text(surf, a, WHITE, (64, y));
        #self.__render_text(surf, 'Order', WHITE, (120, y));
        
        
        stats = ['Attack: ', 'Defense: ', 'Damage: ']
        y = 430
        for line in stats:
            self.__render_text(surf, str(line), WHITE, (16, y)); y += 18
        
        weapon = self.player.slot.weapon
        ammo = self.player.slot.ammo
        
        if ((ammo.flags & IF_ARROW and weapon.flags & IF_FIRES_ARROW) or 
            (ammo.flags & IF_BOLT and weapon.flags & IF_FIRES_BOLT)): 
            ranged = True
        else:
            ranged = False
            
        stats = [self.player.get_total_av(), self.player.get_total_dv(),
                 str(self.player.get_total_min_damage(ranged)) + '-' + str(self.player.get_total_max_damage(ranged))]
        
        y = 430
        for line in stats:
            self.__render_text(surf, str(line), WHITE, (90, y)); y += 18
        
        self.__render_text(surf, 'Gold:', WHITE, (16, 500))
        self.__render_text(surf, str(self.player.gold), WHITE, (90, 500))

        self.__render_text(surf, 'XP:', WHITE, (16, 518))
        self.__render_text(surf, str(self.player.xp), WHITE, (90, 518))

        

        self.__render_text(surf, self.dungeon.name, WHITE, (16, 710))
        self.__render_text(surf, 'Level: %i' % (self.map.level), WHITE, (16, 728))
        
        
    def __render_text(self, surf, text, color, pos, font='std'):
        t = self.__font_cache[font].render('%s' % (text), True, color)
        ts = self.__font_cache[font].render('%s' % (text), True, BLACK)
        surf.blit(ts, (pos[0] + 1, pos[1] + 1))
        surf.blit(t, pos)
    def __load_fonts(self):
        #self.std_font = pygame.font.Font(os.path.join('font', 'jesaya.ttf'), 14)
        self.__font_cache = {'std':pygame.font.Font(os.path.join('font', 'alex.ttf'), 17),
                           'big':pygame.font.Font(os.path.join('font', 'alex.ttf'), 25)}
        
    def __save_map(self):
        self.__clear_surfaces()
        self.__actors.remove(self.player)
        data = self.map, self.__actors, self.__items , self.player.pos()
        if os.access('MAP%i.gz' % (self.map.level), os.F_OK):
             os.remove('MAP%i.gz' % (self.map.level))
        FILE = gzip.open('MAP%i.gz' % (self.map.level), 'w')
        pickle.dump(data, FILE, 2)
        FILE.close()
    def __load_map(self, level):
        if os.access('MAP%i.gz' % (level), os.F_OK):
            FILE = gzip.open('MAP%i.gz' % (level), 'r')
            self.map, self.__actors, self.__items, pos = pickle.load(FILE)
            
            self.__set_game_instance()
            FILE.close()
            self.player.set_pos(pos)
            r = self.camera.adjust(self.player.pos())
            while r:
                r = self.camera.adjust(self.player.pos())
            self.sc = sc(self.map.map_array)
            self.sc.do_fov(self.player.x, self.player.y, self.player.cur_mind / 20 + 5)
            self.__actors.append(self.player)
            for act in self.__actors:
                self.__world_objects[act] = True
            
            for item in self.__items:
                self.__world_objects[item] = True
                
            self.__world_objects[self.map] = True
            self.__clear_surfaces()
            
            self._world_draw()
            return True
        return False
        self.__quit_loop = True
        self.quit_mes = SAVE
    def __build_surf_cache(self):
        fow_surf = pygame.Surface((TILESIZE, TILESIZE))
        fow_surf.fill(BLACK)
        fow_surf.set_alpha(100)
        self.__surf_cache = {'FOW': fow_surf,
                             'stat_block': load_image('stat.png'),
                             'stat_48': load_image('48.png'),
                             'mes_block':load_image('mes_block.png'),
                             'mes_block2':load_image('mes_block2.png')}
    def __clear_surfaces(self):
        for obj in self.__world_objects.keys():
            obj.clear_surfaces()
        self.cursor.cursor_surf = None
    def __gen_id(self):
        for x in xrange(self.__last_id, 9999999):
            yield x

    
