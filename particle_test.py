import pygame, sys, os, random, math

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Particles')

WINDOW_SIZE = (750, 750)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
# /Setup pygame/window ---------------------------------------- #

click = False
r_click = False
rainbow = False
glow = False
bomb = [False, 0, 0]
particles = []
mouse = [0, 0]
speed = 1

TILE_SIZE = 20
tile_map = {}

def circle_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf

class part(object):
    def __init__(self, loc, velocity, timer, color=(255, 255, 255)):
        self.loc = loc.copy()
        self.vel = velocity
        self.timer = timer
        self.color = color
        self.glow_color = (int(self.color[0] / 255 * 50), int(self.color[1] / 255 * 50), int(self.color[2] / 255 * 50))
    
    def update(self, grav=False):
        self.loc[0] += self.vel[0]
        self.loc_str = str(int(self.loc[0] / TILE_SIZE)) + ';' + str(int(self.loc[1] / TILE_SIZE))
        if self.loc_str in tile_map:
            self.vel[0] = -0.7 * self.vel[0]
            self.vel[1] *= 0.95
            self.loc[0] += self.vel[0] * 2
        self.loc[1] += self.vel[1]
        self.loc_str = str(int(self.loc[0] / TILE_SIZE)) + ';' + str(int(self.loc[1] / TILE_SIZE))
        if self.loc_str in tile_map:
            self.vel[1] = -0.7 * self.vel[1]
            self.vel[0] *= 0.95
            self.loc[1] += self.vel[1] * 2
        if grav:
            self.vel[1] += 0.15
        self.timer -= 0.025
        pygame.draw.circle(screen, self.color, (int(self.loc[0]), int(self.loc[1])), int(self.timer))
        if glow:
            radius = self.timer * 2 + 20
            screen.blit(circle_surf(radius, self.glow_color), (int(self.loc[0] - radius), int(self.loc[1]) - radius), special_flags=BLEND_RGB_ADD)

class bomb_part(object):
    def __init__(self, loc, color=(255, 255, 255)):
        self.loc = loc.copy()
        self.vel = [1, 1]
        self.offset = [(random.randint(0, 20) / 10 - 1) * 50, (random.randint(0, 20) / 10 - 1) * 50]
        self.loc[0] += self.offset[0]
        self.loc[1] += self.offset[1]
        self.timer = random.randint(8, 16)
        if color == (255, 255, 255):
            temp = random.randint(150, 255)
            self.color = (temp, temp, temp)
        else:
            self.color = color

    def update(self, grav=False):
        self.loc[0] += self.vel[0]
        self.loc[1] += self.vel[1]
        self.timer -= 1 * ((self.timer / 8) * -1 + 3)
        if grav:
            self.vel[1] += 0.15
        pygame.draw.circle(screen, self.color, (int(self.loc[0]), int(self.loc[1])), (int(self.timer) * random.randint(1, 6)))

def create_tiles(tile_map):
    if tile_map:
        tile_map = {}
    else:
        for i in range(10):
            tile_map[str(i + 4) + ';14'] = (i + 4, 14, (255, 0, 0))
        for i in range(4):
            tile_map['15;' + str(i + 10)] = (15, i + 10, (0, 0, 255))
        tile_map['11;11'] = (11, 11, (0, 255, 255))
        tile_map['11;12'] = (11, 12, (0, 255, 255))
    return tile_map

while True:
    screen.fill((0, 0, 0))
    s = pygame.Surface((750,750), pygame.SRCALPHA)
    mouse[0], mouse[1] = pygame.mouse.get_pos()

    for tile in tile_map:
        pygame.draw.rect(screen, tile_map[tile][2], pygame.Rect(tile_map[tile][0] * TILE_SIZE, tile_map[tile][1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    if bomb[0]:
        for i in range(20):
            if rainbow:
                particles.append(bomb_part(mouse, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
            else:
                particles.append(bomb_part(mouse))
        bomb[1] -= 1
        if bomb[1] <= 0 and bomb[2] != 1:
            bomb[0] = not bomb[0]

    if click:
        for i in range(5): # particles generated per frame
            if rainbow:
                particles.append(part(mouse, [(random.randint(0, 42) / 6 - 3.5) * speed, (random.randint(0, 42) / 6 - 3.5) * speed], random.randint(4, 8), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
            else:
                particles.append(part(mouse, [(random.randint(0, 42) / 6 - 3.5) * speed, (random.randint(0, 42) / 6 - 3.5) * speed], random.randint(4, 8)))

    for i, particle in sorted(enumerate(particles), reverse=True):
        if r_click:
            particle.update(True)
        else:
            particle.update()
        if particle.timer <= 0:
            particles.remove(particle)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1: # left click
                click = True
            if event.button == 3:
                r_click = not r_click
            if event.button == 4:
                speed += 0.1
            if event.button == 5:
                speed -= 0.1
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                click = False
        if event.type == KEYDOWN:
            if event.key == K_a:
                rainbow = not rainbow
            if event.key == K_s:
                bomb[0] = not bomb[0]
                bomb[1] = 10
            if event.key == K_x:
                bomb[2] = 1 - bomb[2]
            if event.key == K_d:
                tile_map = create_tiles(tile_map)
            if event.key == K_f:
                glow = not glow

    screen.blit(s, (0,0))
    pygame.display.update()
    mainClock.tick(60)