# -*- coding: iso-8859-15 -*-
import random

VERTICAL = 0
HORIZONTAL = 1

class Room(object):
    def __init__(self, x, y, w, h):
        self.childs = None
        self.sibling = None
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rx = x + random.randint(1, 4)
        self.ry = y + random.randint(1, 4)
        
        self.rh = h - random.randint(1, 4)
        while self.rh - self.ry < 3:
            self.rh += 1
        
        self.rw = w - random.randint(1, 4)
        while self.rw - self.rx < 3:
            self.rw += 1
            
        self.split = None
        self.parent = None
        self.corridor = False
        
def split_room(room, vertical):
    #if room.parent != None:
    #    if room.parent.parent != None:
    #        if random.randint(0, 100) < 10:
    #            return
        
    if vertical:
        split_line = (room.w - room.x) / 2 + random.randint(-3, 3)
        room1 = Room(room.x, room.y, room.x + split_line, room.h)
        room2 = Room(room.x + split_line, room.y, room.w, room.h)
    else:
        split_line = (room.h - room.y) / 2 + random.randint(-3, 3)
        room1 = Room(room.x, room.y, room.w, room.y + split_line)
        room2 = Room(room.x, room.y + split_line, room.w, room.h)
    room.split = vertical
    room1.parent = room
    room2.parent = room
    
    room.childs = [room1, room2]
    room1.sibling = room2
    room2.sibling = room1

def split(room, count):
    rooms = [room]
    for _ in xrange(count):
        new = []
        for r in rooms:
            if r.parent != None:
                split = not r.parent.split
            else:
                split = random.choice((True, False))
            split_room(r, split)
            if r.childs != None:
                new.extend(r.childs)
        rooms = []
        rooms.extend(new)

def connect_rooms(rooms, map_array, sy='*'):
    for r in rooms:
        #if r==None: return
        #if r.parent==None:continue
        if r.corridor: continue
        vert = r.parent.split

        if vert:
            s = r.sibling
            mm1 = max(r.ry + 1, s.ry + 1)
            mm2 = min(r.rh - 1, s.rh - 1)
            
            if mm1 != mm2:
                y = random.randint(mm1, mm2)
            else:
                y = mm1
            if r.x < s.x: v = r.rx + 1; b = s.rx + 1
            else: v = s.rx + 1 ;b = r.rx + 1
            
            while map_array[y][v] == '.':
                v += 1
            
            while map_array[y][b - 1] == '.':
                b += 1
                
            for x in xrange(v, b - 1):
                map_array[y][x] = sy
            r.corridor = s.corridor = True
        else:
            s = r.sibling
            mm1 = max(r.rx + 1, s.rx + 1)
            mm2 = min(r.rw - 1, s.rw - 1)
            
            if mm1 != mm2:
                x = random.randint(mm1, mm2)
            else:
                x = mm1

            if r.y < s.y: v = r.ry; b = s.ry + 1
            else: v = s.ry ;b = r.ry + 1
            
            while map_array[v][x] == '.':
                v += 1
            
            while map_array[b - 1][x] == '.':
                b += 1
            
            for y in xrange(v, b - 1):
                map_array[y][x] = '*'
            r.corridor = s.corridor = True

def get_all_rooms(room):
    rooms = [room]
    finish = False

    while not finish:
        new = []
        finish = True
        for r in rooms:
            if r.childs != None:
                new.extend(r.childs)
                finish = False
            else:
                new.append(r)
        if not finish:
            rooms = []
            rooms.extend(new)
    return rooms

def create(room):
    rooms = get_all_rooms(room)
    map_array = []
    for _ in xrange(room.h):
        line = []
        for _ in xrange(room.w):
            line.append('.')
        map_array.append(line)
    
    for r in rooms:
        for y in xrange(r.ry, r.rh):
            for x in xrange(r.rx, r.rw):
                map_array[y][x] = '*'
    
    connect_rooms(rooms, map_array)
    parents = set()
    [parents.add(r.parent) for r in rooms]
#    
    while len(parents) > 1:
        connect_rooms(parents, map_array)
        new = set()
        for r in parents:
            if r.parent != None:
                new.add(r.parent)
        parents = new
        
    A = map_array
    N = []
    for y in range(room.h + 1):
        l = []
        for x in range(room.w + 1):
            l.append('.')
        N.append(l)
        
    for y in range(room.h + 1):
        for x in range(room.w + 1):
            if y == 0 or x == 0 or y == room.h - 1 or x == room.w - 1:
                N[y][x] = 1
            else:
                N[y][x] = A[y - 1][x - 1]
    map_array = N
        
    return map_array
    

#    
#    for line in map_array:
#        l = ''
#        for s in line:
#            l = l + str(s)
#        print l  


            
if __name__ == "__main__":
    r1 = Room(0, 0, 100, 50)
    split(r1,5)
    map_array=create(r1)
    for line in map_array:
        l = ''
        for s in line:
            l = l + str(s)
        print l  
    
    
  
