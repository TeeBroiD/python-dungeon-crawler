# -*- coding: iso-8859-15 -*-
import pygame,sys,os

def load_image(name):
      try:
	  image = pygame.image.load(name)
      except pygame.error, message:
	  print 'Cannot load image:', name
	  raise SystemExit, message

      image = image.convert_alpha()
      image.set_alpha(255, pygame.RLEACCEL)
      
      return image
pygame.init()
screen=pygame.display.set_mode((1024,768))
screen.fill((100,100,100))
img = load_image(sys.argv[1])

ts=32

font=pygame.font.SysFont('Sans', 12)

_, _, w, h = img.get_rect()
n=0
for y in range(0, h / ts):
    for x in range(0, w / ts):
	no=font.render(str(n),True,(255,255,255))
	img.blit(no,(x*ts+5,y*ts+5))
	n+=1

img=pygame.transform.smoothscale(img,(1024,768))

screen.blit(img,(0,0))
pygame.display.flip()
abort=False
while not abort:
  for e in pygame.event.get():
    abort= e.type== pygame.QUIT