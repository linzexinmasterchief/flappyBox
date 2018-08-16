import pygame

class UI_button(object):
    def __init__(self, screen, up_pic, down_pic, width, height, position):
        self.screen = screen

        up_pic = up_pic.convert_alpha()
        self.up_pic = pygame.transform.scale(up_pic, (width, height))
        down_pic = down_pic.convert_alpha()
        self.down_pic = pygame.transform.scale(down_pic, (width, height))

        self.position = position

    def set_pos(self, pos):
        self.position = pos

    def get_pos(self):
        return self.position

    def is_over(self):
        point_x, point_y = pygame.mouse.get_pos()
        x, y = self.position
        w, h = self.up_pic.get_size()

        in_x = x < point_x < x + w
        in_y = y < point_y < y + h
        return in_x and in_y

    def render(self):
        if not self.is_over():
            self.screen.blit(self.up_pic, self.position)
        else:
            self.screen.blit(self.down_pic, self.position)