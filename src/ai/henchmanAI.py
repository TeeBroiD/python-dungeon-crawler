from key_mapping import MOVE_WAIT
from actor import Actor
from ai import AI
from pdcglobal import * 

class HenchmanAI(AI):
    def __init__(self, actor):
        AI.__init__(self, actor)
        #self.friends.append(self.game.player.id)
        
    def act(self):
        
        foes = self.get_all_foes_in_sight()
        foes.sort(cmp=lambda x,y: int(get_dis(x.pos(),self.actor.pos())*100) - \
                  int(get_dis(y.pos(),self.actor.pos())*100) )
                
        if len(foes)>0:
            
            foe = foes[0]
            #Debug.debug('henchman: %s' % (foe))
                            
            if (self.is_morale_down() or self.to_close_to_foe(foe)) and self.can_move_away_from_foe(foe):
                self.move_away_from_foe(foe)
            elif (self.is_morale_up() and self.too_far_from_foe(foe)) and self.can_move_toward_foe(foe):
                self.move_toward_foe(foe)
            elif self.can_attack_foe(foe):
                self.attack_foe(foe)
            else:
                self.stand_still()
        else:    
            if len(self.friends) > 0:
                self.move_toward_foe(self.game.get_actor_by_id(list(self.friends)[0]))
            else:
                self.stand_still()
        
        if self.actor.timer==0:
            print 'ouch'
            self.stand_still()
            
