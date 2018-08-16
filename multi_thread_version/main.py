import pygame
from pygame.locals import *
from pygame.font import *
import threading
import random
import time

# import self made python files in lib
# pillar generate and operate functions support
from lib.pillar import *
# ui button class support
from lib.ui_Button import *

# import raw assets
raw_background_img = pygame.image.load(r"assets/background.png")
raw_upperPillar_img = pygame.image.load(r"assets/upper_pillar.png")
raw_lowerPillar_img = pygame.image.load(r"assets/lower_pillar.png")
raw_ground_img = pygame.image.load(r"assets/ground.png")
gameIcon = pygame.image.load(r"assets/icon.png")

raw_ui_start_up_img = pygame.image.load(r"assets/ui_start_up.png")
raw_ui_start_down_img = pygame.image.load(r"assets/ui_start_down.png")


pygame.init()

# game properties
red = (255,0,0)
green = (0,150,0)
white = (255,255,255)
black = (0,0,0)

running = True
is_game_over = False
is_game_paused = False
is_main_menu_shown = True

is_counting_down = False
count_down_font_size = 300
count_down_text = ""
count_down_time = 0


# ui button group array
# 0. start
# 1. about
# 2. exit
main_menu_ui_button_group = []

# height of the main title (for creating slowly going up effect)
main_title_height = 100
main_title_ui_height = 250

# store the reason of death
reason_of_death = ""

# score board
pillar_passed = 0

# actual drawing height is (window height - ground height)
ground_height = 110

# window properties
window_height = 500
window_width = 300

# box properties
gravity = 0.07
box_f_speed = 0
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




# game initialization
# modify the raw assets into assets that can be used in the game
first_background_img = pygame.transform.scale(raw_background_img, (window_width, window_height))
first_background_img_x = 0
second_background_img = pygame.transform.scale(raw_background_img, (window_width, window_height))
second_background_img_x = window_width

pillar_image_width = pillar_width * 2
pillar_img_height = pillar_width * 8
upper_pillar_img = pygame.transform.scale(raw_upperPillar_img, (pillar_image_width, pillar_img_height))
lower_pillar_img = pygame.transform.scale(raw_lowerPillar_img, (pillar_image_width, pillar_img_height))

first_ground_img = pygame.transform.scale(raw_ground_img, (window_width, window_height))
first_ground_img_x = 0
second_ground_img = pygame.transform.scale(raw_ground_img, (window_width, window_height))
second_ground_img = pygame.transform.flip(second_ground_img, True, False)
second_ground_img_x = window_width

# initialize screen
screen = pygame.display.set_mode((window_width, window_height), pygame.DOUBLEBUF | pygame.SRCALPHA)
# screen = screen.convert_alpha()
# set title
pygame.display.set_caption("flappy box")
# set icon
pygame.display.set_icon(gameIcon)
# generate and insert ui buttons into ui button group, prepare for render
start_button = UI_button(screen, raw_ui_start_up_img, raw_ui_start_down_img, 200, 100, (50, main_title_ui_height + 0))
main_menu_ui_button_group.append(start_button)
# update the current "screen" to the actual screen
pygame.display.flip()
# set up pygame loop clocks, prepare to launch
display_clock = pygame.time.Clock()
physics_clock = pygame.time.Clock()
control_clock = pygame.time.Clock()


def initialize_vars():
    global running
    global is_game_over
    global is_game_paused
    global is_main_menu_shown
    global is_counting_down
    global count_down_font_size

    global main_title_height
    global main_title_ui_height

    global first_background_img_x
    global second_background_img_x
    global first_ground_img_x
    global second_ground_img_x

    global reason_of_death
    global pillar_passed
    global box_f_speed
    global box_v_speed

    global box_x
    global box_y
    global box_jump_speed

    global pillar_moving_speed
    global pillar_group
    global time_past_since_last_pillar

    global start_button

    running = True
    is_game_over = False
    is_game_paused = False
    is_main_menu_shown = True
    is_counting_down = False
    count_down_font_size = 100

    main_title_height = 100
    main_title_ui_height = 250

    first_background_img_x = 0
    second_background_img_x = window_width
    first_ground_img_x = 0
    second_ground_img_x = window_width

    reason_of_death = ""
    pillar_passed = 0
    box_f_speed = 0
    box_v_speed = 0

    box_x = 100
    box_y = 200
    box_jump_speed = 2.2

    pillar_moving_speed = 1.0
    pillar_group = []
    time_past_since_last_pillar = 100000

    start_button.set_pos((50, main_title_ui_height + 0))


def game_restart():
    initialize_vars()
    pass


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
            return True
    if box_y > (window_height - ground_height):
        reason_of_death = "you hit the ground!"
        return True

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
    global box_f_speed

    is_game_over = True
    is_game_paused = False
    box_f_speed = pillar_moving_speed




def graphics_thread():
    global running
    global is_game_over
    global is_game_paused
    global is_main_menu_shown
    global is_counting_down

    global count_down_text
    global count_down_font_size

    while running:
        # graphics
        # clear screen by redraw the background image
        screen.blit(first_background_img,[first_background_img_x,0])
        screen.blit(second_background_img,[second_background_img_x,0])

        # draw pillars
        for pillar in pillar_group:
            # top pillar
            screen.blit(upper_pillar_img, [pillar.x - 15, pillar.pillar_hole_height - (pillar_hole_size / 2) - pillar_img_height + 22])
            # bottom pillar
            screen.blit(lower_pillar_img, [pillar.x - 15, pillar.pillar_hole_height + (pillar_hole_size / 2) - 7])

        # draw box character
        if not is_main_menu_shown:
            pygame.draw.rect(screen, pygame.Color(255,0,0,0), (box_x, box_y, box_w, box_h))

        # draw ground (in order to cover the bottom of the lower pillar, the ground is illustrated after the pillars)
        screen.blit(first_ground_img, [first_ground_img_x, 0])
        screen.blit(second_ground_img, [second_ground_img_x, 0])

        # draw ui, ui should be at the top, therefore draw it at last
        if is_main_menu_shown:
            draw_text(screen, "FLAPPY BOX", white, (10, main_title_height), font_size=43)
            for ui_button in main_menu_ui_button_group:
                ui_button.render()




        # display game paused if game is paused
        if is_game_paused and not is_counting_down:
            # display game paused tag
            draw_text(screen, "GAME PAUSED", white, (10, 100), font_size=40)
        

        # display count down if resume from pause
        if is_counting_down:
            draw_text(screen, count_down_text, white, (150 - int(count_down_font_size) / 3, 200 - int(count_down_font_size) / 3), font_size=int(count_down_font_size))



        # display game over, the score and the reason of death if the game is over
        if is_game_over:
            # display game over tag
            draw_text(screen, "GAME OVER", white, (25, 100), font_size=43)
            # display score
            if pillar_passed > 1:
                # if score less than or equal to 1, use single form (pillar)
                draw_text(screen, "you passed " + str(pillar_passed) + " pillars", white, (25, 200), font_size=20)
            else:
                # if score more than 1, use plural form (pillars)
                draw_text(screen, "you passed " + str(pillar_passed) + " pillar", white, (25, 200), font_size=20)
            # display the reason of death
            draw_text(screen, reason_of_death, white, (25, 240), font_size=20)
        else:
            # draw score
            if not is_main_menu_shown and not is_game_paused and not is_counting_down:
                draw_text(screen, str(pillar_passed), white, (window_width / 2, 50))

        # update display
        # graphic_lock.release()
        # time.sleep(0.01)
        # pygame.display.update()
        pygame.display.flip()
        display_clock.tick(100)
        




def physics_thread():
    global time_past_since_last_pillar
    global pillar_generate_duration
    global pillar_group
    global pillar_moving_speed
    global pillar_passed
    global box_y
    global box_x
    global box_v_speed
    global first_background_img_x
    global second_background_img_x
    global first_ground_img_x
    global second_ground_img_x

    global running
    global is_game_over
    global is_game_paused
    global is_main_menu_shown

    while running:
        if is_game_paused or is_main_menu_shown or is_counting_down:
            continue
        # do the physics if the game is not over nor paused
        if not is_game_over:
            # physics
            time_past_since_last_pillar += 1
            # box character falling physics calculation

            # pillar physics
            if time_past_since_last_pillar >= pillar_generate_duration:
                # add a new pillar if time duration is reached
                push_pillar(pillar_group, window_width)
                time_past_since_last_pillar = 0

                pillar_group = remove_used_pillar(pillar_group)

            pillar_group = pillar_move(pillar_group, pillar_moving_speed)
            # detect collision
            if collide_detect():
                if is_main_menu_shown:
                    initialize_vars()
                else:
                    game_over()


            pillar_group, pillar_passed, pillar_moving_speed = score_increase(pillar_group, pillar_passed, pillar_moving_speed)
            # modify the pillar generate duration in order to fit the increasing pillar moving speed
            pillar_generate_duration = 200 / pillar_moving_speed

        # allow the box to keep falling off the screen after game is over
        # box physics
        if box_y > 0:
            box_v_speed, box_y = box_fall(box_v_speed, box_y)
            box_x += box_f_speed

        # the two background images are connected together to leave no space between
        if not is_game_over:
            if first_ground_img_x < -window_width:
                # respawn the image at initial point if the image is completely gone from the screen
                # - moving speed * 2 to make sure the ground textures leave no blank
                first_ground_img_x = window_width - pillar_moving_speed * 2
            else:
                # make the background image to move 1 pixel in 1 loop cycle
                first_ground_img_x -= pillar_moving_speed

            if second_ground_img_x < -window_width:
                # respawn the image at initial point if the image is completely gone from the screen
                # - moving speed * 2 to make sure the ground textures leave no blank
                second_ground_img_x = window_width - pillar_moving_speed * 2
            else:
                # make the background image to move 1 pixel in 1 loop cycle
                second_ground_img_x -= pillar_moving_speed

        # the two background images are connected together to leave no space between
        if not is_game_over:
            if first_background_img_x < -window_width:
                # respawn the image at initial point if the image is completely gone from the screen
                # - moving speed * 2 to make sure the ground textures leave no blank
                first_background_img_x = window_width - pillar_moving_speed * 2
            else:
                # make the background image to move 1 pixel in 1 loop cycle
                first_background_img_x -= 1

            if second_background_img_x < -window_width:
                # respawn the image at initial point if the image is completely gone from the screen
                # - moving speed * 2 to make sure the ground textures leave no blank
                second_background_img_x = window_width - pillar_moving_speed * 2
            else:
                # make the background image to move 1 pixel in 1 loop cycle
                second_background_img_x -= 1
        
        # update physics
        physics_clock.tick(100)

    

pt=threading.Thread(target=physics_thread)
gt=threading.Thread(target=graphics_thread)

pt.start()
gt.start()

while running:
    # basic event control
    for event in pygame.event.get():
        # window exit
        if event.type == pygame.QUIT:
            running = False
        # mouse monitor
        if event.type == MOUSEBUTTONDOWN:
            pressed_array = pygame.mouse.get_pressed()
            if pressed_array[0]:
                # print('Pressed LEFT Button!')
                if main_menu_ui_button_group[0].is_over():
                    # play ui animation after the start button is pressed
                    count = -5
                    while main_title_height > -100:
                        count += 0.5
                        main_title_height -= count
                        for main_menu_ui_button in main_menu_ui_button_group:
                            main_menu_ui_button.set_pos((main_menu_ui_button.get_pos()[0], main_menu_ui_button.get_pos()[1] + count * 2))
                        time.sleep(0.01)
                    is_main_menu_shown = False
                    box_v_speed = -2

            elif pressed_array[1]:
                # print('The mouse wheel Pressed!')
                pass
            elif pressed_array[2]:
                # print('Pressed RIGHT Button!')
                pass

        if is_game_over:
            time.sleep(5)
            initialize_vars()



        # key monitor
        if event.type == pygame.KEYDOWN and not is_game_over and not is_main_menu_shown:
            # box jump control
            if event.key == pygame.K_SPACE and not is_game_paused:
                box_v_speed = -box_jump_speed
            if event.key == pygame.K_ESCAPE:
                if is_game_paused:
                    is_counting_down = True
                    count_down_font_size = 300
                    count_down_time = 0
                else:
                    is_game_paused = not is_game_paused

    # if is_counting_down:
    #     i = int(count_down_time / 100)
    #     if count_down_font_size < 0:
    #         count_down_font_size = 300
    #
    #     count_down_text = str(4 - i)
    #
    #     count_down_time += 0.1
    #     count_down_font_size -= (count_down_time - i * 100)
    #     print(count_down_text)
    #     if count_down_time > 300:
    #         is_counting_down = False
    #         count_down_font_size = 300
    #         count_down_time = 0
    #         is_game_paused = not is_game_paused

    # update control
    # time.sleep(0.01)
    control_clock.tick(100)
