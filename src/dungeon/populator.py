import os
import copy
import random
from ai import *
from item import *
from effects import *
from pdcglobal import *

class Populator(object):
    
    game = None
    
    def __init__(self):
        pass
    
    @staticmethod
    def fill_map_with_items(map, filename, min, max, magic):
        stuff = open(os.path.join('item', filename + '.pdcif'), 'r').read()
        stuff = stuff.split('\n')
       
        items = Populator.findAll(stuff)
        
        count = random.randint(min, max + 1)
        for _ in xrange(0, count):
            name = random.choice(items)
            item = Populator.__create_item(name, stuff, magic)
            item.set_pos(map.get_random_pos())
            item.filename = filename
            item.pop_name = name
            Populator.game.add_item(item, True)

    @staticmethod
    def create_item(name, filename, magic):
        stuff = open(os.path.join('item', filename + '.pdcif'), 'r').read()
        stuff = stuff.split('\n')
        item = Populator.__create_item(name, stuff, magic)
        item.filename = filename
        item.pop_name = name
        return item
            
    @staticmethod
    def create_creature(name, filename):
        creatures = open(os.path.join('npc', filename + '.pdccf'), 'r').read()
        creatures = creatures.split('\n')
        actor = Populator.__create_actor(name, creatures)
        actor.filename = filename
        actor.pop_name = name
        return actor
    
    @staticmethod
    def fill_map_with_creatures(map, filename, min, max):
        creatures = open(os.path.join('npc', filename + '.pdccf'), 'r').read()
        creatures = creatures.split('\n')
       
        actors = Populator.findAll(creatures)
        
        count = random.randint(min, max + 1)
        for _ in xrange(0, count):
            name = random.choice(actors)
            actor = Populator.__create_actor(name, creatures)
            actor.filename = filename
            actor.pop_name = name
            actor.set_pos(map.get_random_pos())
            Populator.game.add_actor(actor, True)
            if hasattr(actor, 'swarm'):
                sn, smin, smax, sfile = actor.swarm
                for _ in xrange(smin, smax):
                    pos = Populator.game.get_free_adj(actor.pos())
                    if pos == None:
                        break
                    Populator.game.add_actor(Populator.create_creature(name, sfile), True)

    @staticmethod
    def __create_item(name, stuff, magic):
        item = None
        
        sn = True
        br = False
        for index in xrange(0, len(stuff)):
            if not br:
                line = stuff[index]
                if line.strip() == '': continue
                if line[0] == '#':continue
                
                if sn:
                    if line[1:] == name:
                        #item = Item(False)
                        #item.flags = IF_IDENTIFIED
                        sn = False
                        continue
                else:
                    if line[0] == '*':
                        br = True
                        continue
                    
                    attr = line.split('=')[0]
                    value = line.split('=')[1]
                    
                    if attr == 'type':
                        item = globals()[value](False)
                        #item.type = globals()[value]
                        item.flags = IF_IDENTIFIED
                    elif attr == 'img':
                        pos = value.split(':')
                        n = random.randint(0, len(pos) - 1)
                        eq, eq2, dd = pos[n].split(',')
                        item.eq_img = int(eq), int(eq2)
                        item.dd_img = int(dd)
                    elif attr == 'damage':
                        no, r = value.split('D')
                        if '+' in r:
                            ey, add = r.split('+')
                        elif '-' in r:
                            ey, add = r.split('-')
                        else:
                            ey, add = r, 0
                        
                        item.damage = value, lambda : cd(int(no), int(ey)) + int(add)
                    elif attr == 'name':
                        item.full_name = item.name = value
                    elif attr == 'flags':
                        flags = value.split(':')
                        for flag in flags:
                            item.flags |= globals()[flag]
                    elif attr == 'av_fx':
                        value = random.choice(value.split(':'))
                        fx, ch = value.split(',')
                        item.av_fx.append((globals()[fx], int(ch)))
                    elif attr == 'dv_fx':
                        value = random.choice(value.split(':'))
                        fx, ch = value.split(',')
                        item.dv_fx.append((globals()[fx], int(ch)))
                    elif attr == 'iden':
                        value = int(value)
                        if value == 1:
                             if not item.flags & IF_IDENTIFIED:
                                item.flags ^= IF_IDENTIFIED
                    elif attr == 'pre' or attr == 'suf':
                        if d(100) <= magic:
                            item.special = True
                            if item.flags & IF_IDENTIFIED:
                                item.flags ^= IF_IDENTIFIED
                            p = random.choice(value.split(':'))
                            globals()[p](item)
                            if item.flags & IF_READABLE:
                                if 'Read' + p in globals():
                                    item.read = globals()['Read' + p]
                                else:
                                    item.read = ReadGenericBook
                            if item.flags & IF_DRINKABLE:
                                item.drink = globals()['Drink' + p]
                    elif attr == 'amount':
                        pos = value.split(':')
                        n = random.randint(0, len(pos) - 1)
                        min, max = pos[n].split(',')
                        item.amount += random.randint(int(min), int(max))
                        item.name = str(item.amount) + ' ' + item.name
                    elif attr == 'dt':
                        item.damage_type = globals()[value]
                    elif attr == 'info':
                        item.infotext = random.choice(value.split(':'))
                        #str/dex=11/9
                        #enc=1
                        #ap/hp=3/8
                    elif attr == 'str/dex':
                        st, dex = value.split('/')
                        item.STR = int(st)
                        item.DEX = int(dex)
                    elif attr == 'ap/hp':
                        ap, hp = value.split('/')
                        item.AP = int(ap)
                        item.HP = int(hp)
                    elif attr == 'enc':
                        item.ENC = int(value)
                    elif attr == 'load':
                        item.load = int(value)
                    elif attr == 'range':
                        item.range = int(value)
                        #skill=WT_AXE
                    elif attr == 'skill':
                        for skill in value.split(':'):
                            item.skills.append(globals()[skill])
                    elif attr == 'locations':
                        locs=value.split(',')
                        for loc in locs:
                            item.locations |= globals()[loc]
                    elif attr == 'ap':
                        item.AP=int(value)
                    elif attr == 'tsp':
                        item.TSP=int(value)
                    elif attr == 'blit_pos':
                        x,y=value.split(',')
                        item.blit_pos=int(x),int(y)
        return item
    
    @staticmethod
    def __create_actor(name, stuff):
        actor = None
        
        sn = True
        br = False
        for index in xrange(0, len(stuff)):
            if not br:
                line = stuff[index]
                if line.strip() == '': continue
                if line[0] == '#':continue
                
                if sn:
                    if line[1:] == name:
                        actor = Actor(False)
                        sn = False
                        continue
                else:
                    
                    if line[0] == '*':
                        br = True
                        continue
                    
                    attr = line.split('=')[0]
                    value = line.split('=')[1]
                    
                    if attr == 'image':
                        value = random.choice(value.split(':'))
                        actor.img_body = int(value), 0
                    elif attr == 'speed':
                        pos = value.split(':')
                        n = random.randint(0, len(pos) - 1)
                        actor.speed = actor.cur_speed = int(pos[n])
                    elif attr == 'strength':
                        pos = value.split(':')
                        n = random.randint(0, len(pos) - 1)
                        actor.strength = actor.cur_strength = int(pos[n])
                    elif attr == 'mind':
                        pos = value.split(':')
                        n = random.randint(0, len(pos) - 1)
                        actor.mind = actor.cur_mind = int(pos[n])
                    elif attr == 'endurance':
                        pos = value.split(':')
                        n = random.randint(0, len(pos) - 1)
                        actor.endurance = actor.cur_endurance = int(pos[n])
                    elif attr == 'ai':
                        ai_class = globals()[value]
                        actor.ai = ai_class(actor)
                    elif attr == 'name':
                        actor.name = value
                    elif attr == 'hp':
                        min, max = value.split(',')
                        actor.health = actor.cur_health = random.randint(int(min), int(max))  
                    elif attr == 'natural_av':
                        value = random.choice(value.split(':'))
                        actor.natural_av = int(value)
                    elif attr == 'natural_dv':
                        value = random.choice(value.split(':'))
                        actor.natural_dv = int(value)
                    elif attr == 'dv_fx':
                        value = random.choice(value.split(':'))
                        fx, ch = value.split(',')
                        actor.dv_fx.append((globals()[fx], int(ch)))
                    elif attr == 'av_fx':
                        value = random.choice(value.split(':'))
                        fx, ch = value.split(',')
                        actor.av_fx.append((globals()[fx], int(ch)))
                    elif attr == 'corpse':
                        actor.ch_drop_corpse = int(value)
                    elif attr == 'gold':
                        min, max = value.split(',')
                        actor.gold = random.randint(int(min), int(max) + 1)
                    elif attr == 'swarm':
                        n, min, max, file = value.split(',')
                        actor.swarm = n, int(min), int(max), file
                    elif attr == 'weapon':
                        value = random.choice(value.split(':'))
                        item, file, magic = value.split(',')
                        weap=Populator.create_item(item, file, magic)
                        actor.weapon = weap
                        actor.items.append(weap)
                    elif attr == 'items':
                        value = random.choice(value.split(':'))
                        item, file, magic = value.split(',')
                        actor.items.append(Populator.create_item(item, file, magic))
                    elif attr == 'xp_value':
                        actor.xp_value = int(value)
                    elif attr == 'morale':
                        actor.morale = int(random.choice(value.split(':')))
        return actor
    
    @staticmethod
    def findAll(stuff):
        actors = []
        for line in stuff:
            if line.strip() == '': continue
            if line[0] == '*':
                actors.append(line[1:])
        return actors
