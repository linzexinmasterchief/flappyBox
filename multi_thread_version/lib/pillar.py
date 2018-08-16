import random

class Pillar(object):
    def __init__(self, window_width):
        self.x = window_width + 20
        self.pillar_hole_height = random.randint(150, 250)
        self.isPassed = False

def pillar_move(pillar_group, pillar_moving_speed):
    # move every pillar in the same speed (right to left)
    for pillar in pillar_group:
        pillar.x -= pillar_moving_speed
    return pillar_group

def push_pillar(pillar_group, window_width):
    # append a new pillar to the end of pillar_group array
    pillar_group.append(Pillar(window_width))

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