import pygame
from pygame.locals import *
from pygame.font import *

import time
import random

pygame.init()

# game properties
red = (255,0,0)
green = (0,150,0)
white = (255,255,255)
black = (0,0,0)

running = True
is_game_over = False
is_game_paused = False

# store the reason of death
reason_of_death = ""

# score board
pillar_passed = 0

# actual drawing height is (window height - ground height)
ground_height = 50


# window properties
window_height = 500
window_width = 300


# box properties
gravity = 0.07
box_f_speed = 5
box_v_speed = 0

box_h = 10
box_w = 10

box_x = 100
box_y = 200

box_jump_speed = 2.2


# random pillar properties
pillar_hole_size = 100
pillar_width = 30
pillar_moving_speed = 1.0
pillar_group = []

# time in ms
pillar_generate_duration = 200
time_past_since_last_pillar = 100000




# ==================================[ code below this line are providing class supports for game process ]===================================
class Pillar(object):
    def __init__(self):
        self.x = 300
        self.pillar_hole_height = random.randint(100, 300)
        self.isPassed = False


# =================================[ code below this line are providing function supports for game process ]==================================


def pillar_move(pillar_group):
    # move every pillar in the same speed (right to left)
    for pillar in pillar_group:
        pillar.x -= pillar_moving_speed
    return pillar_group





def push_pillar(pillar_group):
    # append a new pillar to the end of pillar_group array
    pillar_group.append(Pillar())

def pop_pillar(pillar_group):
    # pop out pillar 0
    pillar_group = pillar_group[1:]
    return pillar_group

def remove_used_pillar(pillar_group):
    # execute pop_pillar function if the oldest pillar is out of the screen
    for i in range(len(pillar_group)):
        try:
            if pillar_group[0].x < 0:
                pillar_group = pop_pillar(pillar_group)
        except:
            pass
    return pillar_group



def is_box_in_hole(pillar, box_x, box_y, box_h, box_w):
    global reason_of_death
    # check if the box is colliding with the pillar if that pillar's x coordinate is in collide range (100 + (box width / 2) + (pillar width /2)) to (100 - (box width / 2) + (pillar width /2))
    # if True, pass; if False, game over
    # box right face clip
    if pillar.x < (100 + box_w):
        # box left face clip
        if pillar.x > (100 - pillar_width):
            # box top clip
            if box_y > (pillar.pillar_hole_height - (pillar_hole_size / 2)):
                # box bottom clip
                if box_y < (pillar.pillar_hole_height + (pillar_hole_size / 2) - box_h):
                    return True
                else:
                    reason_of_death = "you are too low!"
                    return False
            else:
                reason_of_death = "you are too high!"
                return False
        else:
            return True
    else:
        return True

    return True

def collide_detect():
    global reason_of_death
    # detect if the box character hits any of the pillars
    for pillar in pillar_group:
        if not is_box_in_hole(pillar, box_x, box_y, box_h, box_w):
            game_over()
    if box_y > (window_height - ground_height):
        reason_of_death = "you hit the ground!"
        game_over()

def box_fall(box_v_speed, box_y):
    box_v_speed += gravity
    box_y += box_v_speed
    return (box_v_speed, box_y)


def score_increase(pillar_group, pillar_passed, pillar_moving_speed):
    # if a pillar's x coordinate is smaller than box_x and the isPassed flag is not raised, raise the isPassed flag and increase the score (pillar_passed) by 1
    for pillar in pillar_group:
        if (pillar.x + pillar_width) < box_x:
            if not pillar.isPassed:
                pillar.isPassed = True
                pillar_passed += 1
                pillar_moving_speed += 0.1
    return (pillar_group, pillar_passed, pillar_moving_speed)


def draw_text(surface, text,color=white, pos=(0,0), font_size=30):
    # get sys font and set font size
    cur_font = pygame.font.SysFont("Consolas", font_size)
    # set bold
    cur_font.set_bold(True)
    # set text content (pillar passed)
    text_fmt = cur_font.render(text, 1, color)
    # draw text
    surface.blit(text_fmt, pos)

def game_over():
    # execute this function if game is over (character dead)
    global is_game_over
    global is_game_paused
    global running
    is_game_over = True
    is_game_paused = False

# ========================================[ code below this line are resposible for game process ]==========================================
# game initialization
(width, height) = (window_width, window_height)
screen = pygame.display.set_mode((width, height))
pygame.display.flip()

while running:
    for event in pygame.event.get():
        # window exit
        if event.type == pygame.QUIT:
            running = False

        # key monitor
        if event.type == pygame.KEYDOWN and not is_game_over:
            # box jump control
            if event.key == pygame.K_SPACE and not is_game_paused:
                box_v_speed = -box_jump_speed
            if event.key == pygame.K_ESCAPE:
                is_game_paused = not is_game_paused
    


    if not is_game_over and not is_game_paused:
        # physics
        time_past_since_last_pillar += 1
        # box character falling physics calculation
        # box physics
        box_v_speed, box_y = box_fall(box_v_speed, box_y)

        # pillar physics
        if time_past_since_last_pillar >= pillar_generate_duration:
            # add a new pillar if time duration is reached
            push_pillar(pillar_group)
            time_past_since_last_pillar = 0

            pillar_group = remove_used_pillar(pillar_group)

        pillar_group = pillar_move(pillar_group)
        collide_detect()
        pillar_group, pillar_passed, pillar_moving_speed = score_increase(pillar_group, pillar_passed, pillar_moving_speed)
        # modify the pillar generate duration in order to fit the increasing pillar moving speed
        pillar_generate_duration = 200 / pillar_moving_speed


    # graphics
    # clear screen
    screen.fill((0,0,0))

    # draw box character
    pygame.draw.rect(screen, red, (box_x, box_y, box_w, box_h))

    # draw pillars
    for pillar in pillar_group:
        # top pillar
        pygame.draw.rect(screen, green, (pillar.x, 0, pillar_width, pillar.pillar_hole_height - (pillar_hole_size / 2)))
        # bottom pillar
        pygame.draw.rect(screen, green, (pillar.x, pillar.pillar_hole_height + (pillar_hole_size / 2), pillar_width, window_height- pillar.pillar_hole_height - (pillar_hole_size / 2)))

    # draw ground
    # actual drawing height is (window height - ground height)
    pygame.draw.rect(screen, green, (0, window_height - ground_height, window_width, ground_height))
    if is_game_paused:
        draw_text(screen, "GAME PAUSED", white, (10, 200), font_size=40)

    if is_game_over:
        draw_text(screen, "GAME OVER", white, (25, 50), font_size=43)
        if pillar_passed > 1:
            draw_text(screen, "you passed " + str(pillar_passed) + " pillars", white, (25, 200), font_size=20)
        else:
            draw_text(screen, "you passed " + str(pillar_passed) + " pillar", white, (25, 200), font_size=20)
        draw_text(screen, reason_of_death, white, (25, 240), font_size=20)
    else:
        # draw score board
        draw_text(screen, str(pillar_passed), white, (window_width / 2, 50))

    # update display
    pygame.display.update()
    time.sleep(0.01)