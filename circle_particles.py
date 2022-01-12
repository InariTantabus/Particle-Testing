import pygame, sys, os, random, math

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Particles')

WINDOW_SIZE = (750, 750)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((750, 750))
# /Setup pygame/window ---------------------------------------- #

particles = []
pi = math.pi
increment = 0
circle_angle = 0
cur_val = 0

amount = 1
speed = 1
lifespan = 2
alternate = False
alt_run = True
circle_parts = False
span_length = False
fade = False
reverse_fade = False
visual = True
follow_mouse = False
follow_circle = False
follow_center = True
spiral = False
auto_color = False
auto_color_counter = 0

def change_color(cur_val, direction):
    color_length = get_color(0, True)
    if direction == 0:
        cur_val += 1
    else:
        cur_val -= 1
        
    if cur_val >= color_length:
        cur_val = 0
    if cur_val <= -1:
        cur_val = color_length-1
    
    return cur_val

def get_color(cur_val, color_length=False):
    temp_rand = random.randint(0, 255)
    color_list = [
        (255, 255, 255),
        (temp_rand, temp_rand, temp_rand),
        (random.randint(0,255), random.randint(0,255), random.randint(0,255)),
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255),
        (0, 255, 255),
        # (255, (255/2), 0), # Extra colors
        # (255, 0, (255/2)),
        # ((255/2), 255, 0),
        # (0, 255, (255/2)),
        # ((255/2), 0, 255),
        # (0, (255/2), 255),
        # (255, (255/2), (255/2)),
        # ((255/2), 255, (255/2)),
        # ((255/2), (255/2), 255),
        # (255, (255/2), 255),
        # (255, 255, (255/2)),
        # ((255/2), 255, 255),
        (temp_rand, temp_rand/3, 0),
        (temp_rand, 0, temp_rand/3),
        (temp_rand/3, 0, temp_rand),
        (random.randint(0,255), 0, 0),
        (0, random.randint(0,255), 0),
        (0, 0, random.randint(0,255)),
        (temp_rand, temp_rand, 0),
        (temp_rand, 0, temp_rand),
        (0, temp_rand, temp_rand),
        (random.randint(0,255), random.randint(0,255), 0),
        (random.randint(0,255), 0, random.randint(0,255)),
        (0, random.randint(0,255), random.randint(0,255))
    ]

    if not color_length:
        return color_list[cur_val]
    else:
        return len(color_list)

def find_circle_thingy(ang):
    ang = ang/180*pi
    temp_x = 375+150*math.cos(ang)
    temp_y = 375+150*math.sin(ang)
    return temp_x, temp_y

def find_points(pos, rot, span):
    points = []
    if span_length:
        if_span = span/120
    else:
        if_span = 1

    dist = 0*if_span
    points.append((pos[0]+dist*math.cos(rot), pos[1]-dist*math.sin(rot)))
    
    dist = math.hypot(155-150, 155-150)*if_span
    angle = (rot+math.atan2(155-150, 155-150))%(2*math.pi)
    points.append((pos[0]-dist*math.cos(angle), pos[1]+dist*math.sin(angle)))

    dist = -30*if_span
    points.append((pos[0]+dist*math.cos((rot)%(2*math.pi)), pos[1]-dist*math.sin(rot)))

    dist = math.hypot(155-150, 155-150)*if_span
    angle = (rot+math.atan2(155-150, 145-150))%(2*math.pi)
    points.append((pos[0]+dist*math.cos(angle), pos[1]-dist*math.sin(angle)))

    return points

class Particle:
    def __init__(self, increment, x, y, clr=(255,255,255), ml=120):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.angle = (15*increment/180*pi)%(2*pi)
        self.radius = 10
        self.maxlife = ml
        self.life = ml
        self.rot = self.angle
        self.true_color = clr
        self.color = clr

    def draw(self):
        if circle_parts:
            if span_length:
                if_span = self.life/120
            else:
                if_span = 1
            pygame.draw.circle(display, self.color, (self.target_x, self.target_y), self.radius*(if_span)) ## draw circle
        else:
            points = find_points((self.target_x, self.target_y), -self.rot, self.life)
            pygame.draw.polygon(display, self.color, points)
        
    def update(self):
        self.life -= 1
        temp_pos = (self.target_x, self.target_y)

        if spiral:
            self.target_x = self.x+((-(self.life)+self.maxlife)*2)*math.cos(self.angle)
            self.target_y = self.y+((-(self.life)+self.maxlife)*2)*math.sin(self.angle)
        else:
            self.target_x = self.x+((-(self.life)+120)*2)*math.cos(self.angle)
            self.target_y = self.y+((-(self.life)+120)*2)*math.sin(self.angle)

        self.rot = math.atan2(self.target_y-temp_pos[1], self.target_x-temp_pos[0])
        self.angle = (self.angle+(speed/180*pi))%(2*pi)
    
    def fade(self):
        if self.life > 0:
            self.color = (self.true_color[0]*(self.life/self.maxlife), self.true_color[1]*(self.life/self.maxlife), self.true_color[2]*(self.life/self.maxlife))
    
    def reverse_fade(self):
        if self.life > 0:
            temp_value = self.maxlife-self.life
            self.color = (self.true_color[0]*(temp_value/self.maxlife), self.true_color[1]*(temp_value/self.maxlife), self.true_color[2]*(temp_value/self.maxlife))

while True:
    display.fill((0, 0, 0))
    mx, my = pygame.mouse.get_pos()
    cx, cy = find_circle_thingy(circle_angle)

    circle_angle = (circle_angle+1)%360

    if auto_color:
        if auto_color_counter == 0:
            cur_val = change_color(cur_val, 0)
            auto_color_counter = 240
        else:
            auto_color_counter -= 1

    if visual:
        if follow_circle:
            particles.append(Particle(increment, cx, cy, get_color(cur_val), lifespan*60))
        if follow_mouse:
            particles.append(Particle(increment, mx, my, get_color(cur_val), lifespan*60))
        if follow_center:
            particles.append(Particle(increment, 375, 375, get_color(cur_val), lifespan*60))

        increment = (increment+amount)%360
    
    if alternate:
        if alt_run:
            cur_val += 1
            if cur_val == get_color(0, True):
                cur_val = 0
        else:
            cur_val -= 1
            if cur_val == -1:
                cur_val = -1 + get_color(0, True)
        alt_run = not alt_run
    else:
        if not alt_run:
            cur_val -= 1
            if cur_val == -1:
                cur_val = -1 + get_color(0, True)
            alt_run = not alt_run
    
    for i, particle in sorted(enumerate(particles), reverse=True):
        particle.update()
        if fade:
            particle.fade()
        if reverse_fade:
            particle.reverse_fade()
        if particle.life <= 0:
            particles.pop(i)
        particle.draw()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                cur_val = change_color(cur_val, 0)
            if event.button == 3:
                cur_val = change_color(cur_val, 1)
            if event.button == 4:
                amount += 1
            if event.button == 5:
                amount -= 1
        if event.type == KEYDOWN:
            if event.key == K_a:
                alternate = not alternate
            if event.key == K_q:
                circle_parts = not circle_parts
            if event.key == K_t:
                span_length = not span_length
            if event.key == K_g:
                spiral = not spiral
            if event.key == K_b:
                auto_color = not auto_color
            if event.key == K_SPACE:
                visual = not visual

            if event.key == K_r:
                speed += 1
            if event.key == K_f:
                speed -= 1
            if event.key == K_v:
                speed = 1

            if event.key == K_w:
                if lifespan < 8:
                    lifespan += 1
            if event.key == K_s:
                if lifespan > 0:
                    lifespan -= 1

            if event.key == K_d:
                fade = not fade
                if reverse_fade:
                    reverse_fade = not reverse_fade
            if event.key == K_e:
                reverse_fade = not reverse_fade
                if fade:
                    fade = not fade

            if event.key == K_z:
                follow_mouse = not follow_mouse
            if event.key == K_x:
                follow_circle = not follow_circle
            if event.key == K_c:
                follow_center = not follow_center

            if event.key == K_1:
                amount = 0 
            if event.key == K_2:
                amount = -12 
            if event.key == K_3:
                amount = -8 
            if event.key == K_4:
                amount = -6 
            if event.key == K_5:
                pass
            if event.key == K_6:
                amount = -4
            if event.key == K_7:
                pass
            if event.key == K_8:
                amount = -3

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    mainClock.tick(60)