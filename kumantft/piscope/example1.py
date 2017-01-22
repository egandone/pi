import os
import pygame
import time
import random
from piscope import *

os.putenv('SDL_FBDEV', '/dev/fb1')
scope = Piscope()
pygame.mouse.set_visible(False)
#scope.test()

font = pygame.font.Font(None, 25)
label_surface = font.render('version - %s' % ('1.0.0'), True, (255,255,255))
(labelX, labelY) = (scope.size()[0]/2 - label_surface.get_width()/2, scope.size()[1]/2 - label_surface.get_height()/2)
scope.screen.blit(label_surface, (labelX,labelY))
pygame.display.update()
time.sleep(5)

for y in range(0, scope.size()[1]+1, 32):
	for x in range(0, scope.size()[0]+1, 48):
		label_surface = font.render('(%d,%d)' % (x,y), True, (255,255,255))
		if y < scope.size()[1]/2:
			labelX = scope.size()[0] - label_surface.get_width()
			labelY = scope.size()[1] - label_surface.get_height()
		else:
			labelX = 0
			labelY = 0
		X_surface = font.render('+', True, (255,255,255))
		XposX = x - X_surface.get_width() / 2
		XposY = y - X_surface.get_height() / 2
		scope.clear()
		scope.screen.blit(X_surface, (XposX,XposY))
		scope.screen.blit(label_surface, (labelX,labelY))
		pygame.display.update()
		time.sleep(1)
