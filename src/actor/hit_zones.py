from pdcglobal import *

def leg(tot):
    tot += 4
    return tot / 5
def head(tot):
    tot += 4
    return tot / 5
def arm(tot):
    tot += 4
    v = tot / 5 - 1
    return max(v, 1)
def chest(tot):
    tot += 4
    return tot / 5 + 2
def abdomen(tot):
    tot += 4
    return tot / 5 + 1

class HitZones(object):
    def __init__(self, host):
        
        tot = host.SIZ + host.CON
        
        # cur/max
        zones = {'L_Leg': (leg(tot), leg(tot), 'left leg', L_LEGS),
                 'R_Leg' : (leg(tot), leg(tot), 'right leg', L_LEGS),
                 'L_Arm' : (arm(tot), arm(tot), 'left arm', L_ARMS),
                 'R_Arm' : (arm(tot), arm(tot), 'right arm', L_ARMS),
                 'Abdomen' : (abdomen(tot), abdomen(tot), 'abdomen', L_ABDOMEN),
                 'Chest' : (chest(tot), chest(tot), 'chest', L_CHEST),
                 'Head': (head(tot), head(tot), 'head', L_HEAD)}

        for zone in zones:
            self.__dict__[zone] = zones[zone]
        
        self.__dict__['zones'] = zones
        self.__dict__['host'] = host
    
    def get_random_zone(self):
        z = d(20)
        if z <= 3:
            return 'R_Leg'
        if z <= 6:
            return 'L_Leg'
        if z <= 9:
            return 'Abdomen'
        if z <= 12:
            return 'Chest'
        if z <= 15:
            return 'R_Arm'
        if z <= 18:
            return 'L_Arm'
        return 'Head'
    
    def __getstate__(self):
        return self.__dict__
  
    def __setstate__(self, state):
        for item in state:
            self.__dict__[item] = state[item]
    
    def __getattr__(self, attr):
        return self.__dict__[attr]

    def __setattr__(self, attr, value):
        self.__dict__[attr] = value
