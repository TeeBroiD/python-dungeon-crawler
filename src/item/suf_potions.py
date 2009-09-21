import random
from pdcglobal import *
from effects import *

def PotionOfKillbeePoison(item):
    item.full_name += ' of Killerbee-Poison'
    item.weaponinfotext = 'Dangerous Poison'
def DrinkPotionOfKillbeePoison(self, actor):
    KillerbeePoisonEffect(actor,None)


def PotionOfYumuraPoison(item):
    item.full_name += ' of Yumura-Poison'
def DrinkPotionOfYumuraPoison(self, actor):
    YumuraPoisonEffect(actor,None)


def PotionOfRegeneration(item):
    item.full_name += ' of Killerbee-Poison'
def DrinkPotionOfRegeneration(self, actor):
    RegenerationEffect(actor,None)
    

def PotionOfEndurance(item):
    item.full_name += ' of Endurance'
def DrinkPotionOfEndurance(self, actor):
    actor.cur_endurance += d(10) + d(10)
    
    
def PotionOfMind(item):
    item.full_name += ' of Mind'
def DrinkPotionOfMind(self, actor):
    actor.cur_mind += d(10) + d(10)
        
        
def PotionOfSpellcaster(item):
    item.full_name += ' of Spellcasters'
def DrinkPotionOfSpellcaster(self, actor):
    actor.cur_endurance += d(10) + d(10)
    actor.cur_mind += d(10) + d(10)


def PotionOfHealing(item):
    item.full_name += ' of Healing'
def DrinkPotionOfHealing(self, actor):
    actor.cur_health += d(10)