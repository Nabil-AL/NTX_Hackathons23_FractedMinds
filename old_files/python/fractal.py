import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
running = True

min_re = min_im = -2.0
max_re = max_im = 2.0
max_iter = 100

# fill the screen with a color to wipe away anything from last frame
for i in range(screen.get_height()):
	for j in range(screen.get_width()):
		c = -0.8 + 0.2j
		z = (
			min_re + (j * (max_re - min_re) / screen.get_width())
			+ 1j * (min_im + (i * (max_im - min_im) / screen.get_height()))
		)
		for step in range(max_iter):
			if z.real * z.real + z.imag * z.imag > 4:
				screen.set_at((j, i), (255.0 * (max_iter - step) / max_iter,) * 3)
				break
			z = z * z + c
		else:
			screen.set_at((j, i), "lightblue")

while running:
	# poll for events
	# pygame.QUIT event means the user clicked X to close your window
	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			running = False

	# RENDER YOUR GAME HERE

	# flip() the display to put your work on screen
	pygame.display.flip()

	clock.tick(60)  # limits FPS to 60

pygame.quit()
