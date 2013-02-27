# Import a library of functions called 'pygame'
import pygame
import math
import random

def p_to_r(angle, mag):
	angle_r = math.radians(angle)
	return ( math.sin(angle_r)*mag, -math.cos(angle_r)*mag)

def new_length(b):
	return b*random.randint( 8, 13 )*0.07

def new_angle(a,s):
	return a + s*random.randint( 8, 13 )*3.0

def do_continue():
	return random.random() > 0.45
	
def pseudo_green():
	r = random.randint(0,128)
	r2 = random.randint(0,128)
	return [r,255-r2,r]
		
def draw_branch(coords, branch_len, angle, s):
	x,y = coords
	dx,dy = p_to_r(angle, branch_len)
	third_dx,third_dy = (dx / 3.0, dy / 3.0)
	branch_end = (x+dx, y+dy)
	pygame.draw.line(screen,brown,coords,branch_end,int(branch_len/15))
	if branch_len > 60:
		branch_start_1 = (x + third_dx, y + third_dy) # One third along branch 
		branch_start_2 = (x + third_dx*2, y + third_dy*2) # Two thirds
		# Side branches...
		draw_branch(branch_start_1, new_length(branch_len), new_angle(angle, s), -s)
		draw_branch(branch_start_2, new_length(branch_len), new_angle(angle, -s), -s)
		# Continue the current stem...
		if do_continue():
			draw_branch(branch_end, new_length(branch_len), angle, s)
		else:
			cx,cy = int( branch_end[0] ), int( branch_end[1] )
			pygame.draw.circle( screen, pseudo_green(), (cx,cy), 10 )
	elif branch_len > 30:
		branch_start_1 = (x + third_dx, y + third_dy) # One third along branch 
		branch_start_2 = (x + third_dx*2, y + third_dy*2) # Two thirds
		# Side branches...
		if do_continue():
			draw_branch(branch_start_1, new_length(branch_len), new_angle(angle, s), -s)
		if do_continue():
			draw_branch(branch_start_2, new_length(branch_len), new_angle(angle, -s), -s)
		# Continue the current stem...
		if do_continue():
			draw_branch(branch_end, new_length(branch_len), angle, s)
		else:
			cx,cy = int( branch_end[0] ), int( branch_end[1] )
			pygame.draw.circle( screen, pseudo_green(), (cx,cy), 10 )
	else:
		cx,cy = int( branch_end[0] ), int( branch_end[1] )
		pygame.draw.circle( screen, pseudo_green(), (cx,cy), 10 )

def draw_tree():
	# Set the screen background
	screen.fill(white)
	draw_branch((600, 700), 150, 0, 1.0) 
	pygame.display.flip()


# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
white = [255,255,255]
green = [0,255,0]
brown = [196,128,0]

# Set the height and width of the screen
size=[1200,700]
screen=pygame.display.set_mode(size)

draw_tree()

done = False

pygame.display.flip()

while done==False:
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done=True # Flag that we are done so we exit this loop
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				draw_tree()
			if event.key == pygame.K_ESCAPE:
				done = True
		
		
