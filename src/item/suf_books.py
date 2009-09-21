from pdcglobal import *
from magic import *

def BookOfTOVU(item):
    pass

def BookOfRegeneration(item):
    item.full_name += ' of Regeneration'
    item.spell = Regeneration

def BookOfIdentify(item):
    item.full_name += ' of Identify'
    item.spell = Identify
    
def BookOfLesserHealing(item):
    item.full_name += ' of Lesser Healing'
    item.spell = LesserHealing
    
def BookOfHealing(item):        
    item.full_name += ' of Healing'
    item.spell = Healing
    
def BookOfFoulnessRay(item):        
    item.full_name += ' of Foulness-Ray'
    item.spell = FoulnessRay
    
def BookOfFrostRay(item):        
    item.full_name += ' of Frost-Ray'
    item.spell = FrostRay
    
def BookOfLesserHaste(item):        
    item.full_name += ' of Lesser Haste'
    item.spell=LesserHaste

def ReadBookOfTOVU(self,actor):
    actor.game.shout('Your read the Book of Vile Umbrages')
    
def ReadGenericBook(self, actor):
    learn_spell(self, actor)    
    
def learn_spell(book, actor):
    if not book.flags & IF_IDENTIFIED:
        book.flags ^= IF_IDENTIFIED
    s=book.spell()
    actor.timer += actor.cur_speed*3
    for spell in actor.spells:
        if isinstance(spell, book.spell):
            actor.game.shout('You already know the %s-Spell' % (s.name))
            return
    actor.spells.append(s)
    actor.game.shout('You learned the %s-Spell' % (s.name))
