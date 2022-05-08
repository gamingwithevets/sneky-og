#import
import pygame
import random
import time
import sys
from decimal import *
from pygame import mixer

pygame.init()
# window
w, h = 800, 600
game = pygame.display.set_mode((w,h))
pygame.display.set_caption("Snake")

# size each cell
m = 20

# load image
imgHead_r = pygame.transform.scale(pygame.image.load('head_r.png'),(m,m))
imgHead_l = pygame.transform.scale(pygame.image.load('head_l.png'),(m,m))
imgHead_u = pygame.transform.scale(pygame.image.load('head_u.png'),(m,m))
imgHead_d = pygame.transform.scale(pygame.image.load('head_d.png'),(m,m))
imgHead_die = pygame.transform.scale(pygame.image.load('head_die.png'),(m,m))

# load sound
#mixer.music.load('mainmenu.ogg')
#mixer.music.play(-1)

# PERCENTAGE of the alpha layer
alpha_percentage = 20


# 0: unhook snake speed from framerate
# 1: tie snake speed to framerate (uses a set FPS)
delta_type = 0

# FPS for delta type 1
FPS = 100

# color
white = (255,255,255)
green = (0,255,0)
gray = (128,128,128)
red = (255,0,0)
yellow = (255,255,0)
black = (0,0,0)



# list apple
appleList = 0

if appleList == 1:
	apple_List = []
	apple_List.insert(0,apple)

# border
border_x = 20
border_y = 60

# feature
snake_bump = 1

def game_over():
	alpharec_drawn = False
	while True:
		over_font = pygame.font.SysFont(None, 30)
		over_text = over_font.render("Game over! Press Space to replay - Press Escape to exit", True, black)
		over_rect = over_text.get_rect()
		over_rect.midtop = (w//2 , h//2)

		display = pygame.Surface((w - border_x - 20, h - border_y - 20))
		display.set_alpha(int(255 / 100 * alpha_percentage))
		display.fill(black)
		if alpharec_drawn == False:
			game.blit(display, (border_x,border_y))
			game.blit(over_text, over_rect)
		pygame.display.flip()

		pygame.event.get()
		key_pressed = pygame.key.get_pressed()
		if key_pressed[pygame.K_ESCAPE]:
			pygame.quit()
			sys.exit()
		elif key_pressed[pygame.K_SPACE]:
			main()

		alpharec_drawn = True

		#time.sleep(2)
		#pygame.quit()
		#sys.exit()

def show_score():
	score_font = pygame.font.SysFont(None, 40)
	score_text = score_font.render("Score: {0}".format(score), True, red)
	score_rect = score_text.get_rect()
	score_rect.midtop = (80, 20)
	game.blit(score_text, score_rect)

def show_delay():
	score_font = pygame.font.SysFont(None, 40)
	getcontext().prec = 3
	score_decimal = Decimal(15) - Decimal(speed / 20)
	if delta_type == 0:
		score_text = score_font.render("Speed: {0} tiles/sec".format(str(score_decimal), ".2f"), True, red)
	else:
		score_text = score_font.render("Speed: {0} tiles/60 fps".format(str(score_decimal), ".2f"), True, red)
	score_rect = score_text.get_rect()
	score_rect.midtop = (600, 20)
	game.blit(score_text, score_rect)

def main():
	global direction
	global apple
	global score
	global speed

	# snake
	snake_head = [100,100]
	snake = [[100,100],[80,100],[60,100]]
	#snake = [(20,20),(21,20),(22,20)]

	# direction
	direction = 'RIGHT'

	# score
	score = 0
	
	# speed - lower => faster
	speed = 150

	# apple
	apple = [300,300]

	clock = pygame.time.Clock()
	run = True

	while run:
		# background
		game.fill(white)

		# speed
		if delta_type == 0:
			pygame.time.delay(int(speed))
		else:
			clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		key_pressed = pygame.key.get_pressed()
		if key_pressed[pygame.K_UP]:
			direction = 'UP'
		if key_pressed[pygame.K_DOWN]:
			direction = 'DOWN'
		if key_pressed[pygame.K_RIGHT]:
			direction = 'RIGHT'
		if key_pressed[pygame.K_LEFT]:
			direction = 'LEFT'
		if key_pressed[pygame.K_ESCAPE]:
			pygame.quit()
			sys.exit()

		if direction == 'RIGHT':
			snake_head[0] += m
		if direction == 'LEFT':
			snake_head[0] -= m
		if direction == 'UP':
			snake_head[1] -= m
		if direction == 'DOWN':
			snake_head[1] += m

		
		# snake moving
		snake.insert(0, list(snake_head))

		if appleList == 0:
			if snake_head == apple:
				score += 1

				if int(speed) > 0:
					speed *= 0.97
				else:
					speed -= 0.5
				while True:
					apple_x = random.randrange(border_x,w-border_x,20)
					apple_y = random.randrange(border_y,h-border_y,20)
					apple = [apple_x, apple_y]
					if apple not in snake:
						break
				# draw apple color
			else:
				snake.pop()

		else:
			if snake_head in apple_List:
				apple_List.remove(snake_head)
				# plus score
				score += 1
				# move faster
				if int(speed) > 0:
					speed *= 0.97
				else:
					speed -= 0.5
				for i in range(score):
					apple_x = random.randrange(border_x,w-20,20)
					apple_y = random.randrange(border_y,h-20,20)
					apple = [apple_x, apple_y]
					if apple not in apple_List and apple not in snake:
						apple_List.insert(0,apple)
			else:
				snake.pop()

		# draw snake color
		for s in snake:
			pygame.draw.rect(game,green,(s[0],s[1],m,m))
		# draw snake head
		if direction == 'RIGHT':
			game.blit(imgHead_r,pygame.Rect(snake_head[0],snake_head[1],m,m))
		if direction == 'LEFT':
			game.blit(imgHead_l,pygame.Rect(snake_head[0],snake_head[1],m,m))
		if direction == 'UP':
			game.blit(imgHead_u,pygame.Rect(snake_head[0],snake_head[1],m,m))
		if direction == 'DOWN':
			game.blit(imgHead_d,pygame.Rect(snake_head[0],snake_head[1],m,m))

		# draw apple
		if appleList == 0:
			pygame.draw.rect(game, red, (apple[0], apple[1], m, m))
		else:
			for a in apple_List:
				pygame.draw.rect(game, red, (a[0], a[1], m, m))


		#border
		pygame.draw.rect(game,gray,(border_x,border_y,w - border_x - 20,h - border_y - 20),10)


		#score
		show_score()

		# delay
		show_delay()

		# hit border
		if (snake_head[0] >= w - 20
		or snake_head[0] <= border_x - 10
		or snake_head[1] >= h - 20
		or snake_head[1] <= border_y - 10):
			if snake_bump == 1:
				game.blit(imgHead_die,pygame.Rect(snake_head[0],snake_head[1],m,m))
				run = False
				game_over()
			else:
				
				#score = score + (len(snake))

				if snake_head[0] <= border_x - 15:
					snake_head[0] = w - 2*m
				elif snake_head[0] >= w - m:
					snake_head [0] = border_x
				elif snake_head[1] >= h - m:
					snake_head[1] = border_y
				elif snake_head[1] <= border_y - 15:
					snake_head[1] = h - 2*m


		#update
		pygame.display.flip()

	return

if __name__ == "__main__":
	main()
