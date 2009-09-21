#!/usr/bin/env python
#
#       run_game.py
#       
#       Copyright 2009 Dominic Kexel <dk@evil-monkey-in-my-closet.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       Part of (or All) the graphic tiles used in this program is the public 
#       domain roguelike tileset "RLTiles".
#       Some of the tiles have been modified by me.
#       You can find the original tileset at:
#       http://rltiles.sf.net

import sys
import os
import gzip
import pygame

if '--profile' in sys.argv:
    import cProfile as profile

try:
    import cPickle as pickle
except:
    import pickle

try:
    import psyco
    psyco.full()
except:
    print "no psyco... maybe you should install it..."

sys.path.append(os.path.join('.', 'src'))

import engine
from pdcglobal import *

for file in os.listdir('.'):
    if file[0:3]=='MAP':
        os.remove(file)

pygame.init()
screen = pygame.display.set_mode((1024, 768))

ts=True

if not '--newgame' in sys.argv:
    if os.access('save.gz', os.F_OK):
        FILE = gzip.open('save.gz', 'r')
        game = pickle.load(FILE)
        game.screen = screen
        game.re_init()
        FILE.close()
        ts=False
    else:   
        game = engine.Engine()
else:
    game = engine.Engine()
    
s = game.start

if '--profile' in sys.argv:
    profile.run('quit_mes = s(ts)')
else:
    quit_mes = s(ts)

if quit_mes == SAVE:
    data = game 
    FILE = gzip.open('save.gz', 'w')
    pickle.dump(data, FILE, 2)
    FILE.close()
else:
    if os.access('save.gz', os.F_OK):
        os.remove('save.gz')
        


