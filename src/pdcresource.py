import pygame
import os

# parts:
# 0 -> full image
# 1 -> left half
# 2 -> right half
# 3 -> upper half
# 4 -> lower half
# 5 -> upper left corner
# 6 -> upper right corner
# 7 -> lower left corner
# 8 -> lower right corner


class Res:
    def __init__(self, name, tilesize):
        self.res = self.load_image(name)
        _, _, w, h = self.res.get_rect()
        self.tiles = []
        for y in range(0, h / tilesize):
            for x in range(0, w / tilesize):
                tile = pygame.Surface((tilesize, tilesize), depth=self.res)
                chop_rect = (x * tilesize, y * tilesize, tilesize, tilesize)
                tile.blit(self.res, (0, 0), chop_rect)
                self.tiles.append(tile)
                
    def get(self, no):
        return self.tiles[no]
    
    def get_subs(self, (no_part)):
        if no_part == None: return pygame.Surface((0,0))
        no, part = no_part
        img = self.get(no)
        if part == 0: return img
        _, _, w, h = img.get_rect() 
        
        if part == 1:
            sub = pygame.Surface((w / 2, h), depth=img)
            sub.blit(img, (0, 0), (0, 0, w / 2, h))
        if part == 2:
            sub = pygame.Surface((w / 2, h), depth=img)
            sub.blit(img, (0, 0), (w / 2, 0, w / 2, h))
        if part == 3:
            sub = pygame.Surface((w, h / 2), depth=img)
            sub.blit(img, (0, 0), (0, 0, w, h / 2))
        if part == 4:
            sub = pygame.Surface((w, h / 2), depth=img)
            sub.blit(img, (0, 0), (0, h / 2, w, h / 2))

        if part == 5:
            sub = pygame.Surface((w / 2, h / 2), depth=img)
            sub.blit(img, (0, 0), (0, 0, w / 2, h / 2))
        if part == 6:
            sub = pygame.Surface((w / 2, h / 2), depth=img)
            sub.blit(img, (0, 0), (w / 2, 0, w / 2, h / 2))
        if part == 7:
            sub = pygame.Surface((w / 2, h / 2), depth=img)
            sub.blit(img, (0, 0), (0, h / 2, w / 2, h / 2))
        if part == 8:
            sub = pygame.Surface((w / 2, h / 2), depth=img)
            sub.blit(img, (0, 0), (w / 2, h / 2, w / 2, h / 2))
                                    
        return sub    
        
        
    
    def load_image(self, name):
        try:
            image = pygame.image.load(os.path.join('gfx', name))
        except pygame.error, message:
            print 'Cannot load image:', name
            raise SystemExit, message

        image = image.convert_alpha()
        image.set_alpha(255, pygame.RLEACCEL)
        
        return image
