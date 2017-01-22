import os
import pygame

class Piscope(object):
	screen = None;

	def __init__(self):
		disp_no = os.getenv("DISPLAY")
		if disp_no:
			print("I'm running under X display = {0}". format(disp_no))

		drivers = ["fbcon", "directfb", "svgalib"]
		found = False
		for driver in drivers:
			if not os.getenv('SDL_VIDEODRIVER'):
				os.putenv('SDL_VIDEODRIVER', driver)

			try:
				pygame.display.init()
			except:
				print("Driver: {0} failed".format(driver))
				continue

			found = True
			break

		size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
		print("Framebuffer size: %d x %d" % (size[0], size[1]))
		self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
		self.screen.fill((0,0,0))
		pygame.font.init()
		pygame.display.update()

	def __del__(self):
		"Destructor to make sure pygame shuts down, etc."

	def test(self):
		red = (255, 0, 0)
		self.screen.fill(red)
		pygame.display.update()

	def clear(self):
		self.screen.fill((0,0,0))
		
	def size(self):
		size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
		return size
