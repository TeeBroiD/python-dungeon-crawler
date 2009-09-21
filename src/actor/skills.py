class Skills(object):
    def __init__(self, host):
        
        skills = {'Flail':host.STR + host.DEX,
                'Flail2H':host.STR + host.DEX,
                'Sword':host.STR + host.DEX,
                'Sword2H':host.STR + host.DEX,
                'Axe':host.STR + host.DEX,
                'Axe2H':host.STR + host.DEX,
                'Polearm':host.STR + host.DEX,
                'Polearm2H':host.STR + host.DEX,
                'Hammer':host.STR + host.DEX,
                'Hammer2H':host.STR + host.DEX,
                'Rapier':host.STR + host.DEX,
                'Dagger':host.STR + host.DEX,
                'Spear':host.STR + host.DEX,
                'Bow':host.DEX,
                'Crossbow':host.DEX,
                'Sling':host.DEX,
                'Throwing':host.DEX,
                'Dodge':host.DEX+10-host.SIZ,
                'Resilence':host.CON+host.POW,
                'Unarmed':host.STR + host.DEX}
        
        for skill in skills:
            self.__dict__[skill] = skills[skill]
        
        self.__dict__['skills'] = skills
        self.__dict__['host'] = host
    
    def __getstate__(self):
        return self.__dict__
  
    def __setstate__(self, state):
        for item in state:
            self.__dict__[item] = state[item]
    
    def __getattr__(self, attr):
        return self.__dict__[attr]

    def __setattr__(self, attr, value):
        self.__dict__[attr] = value
