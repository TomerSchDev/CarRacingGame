import pygame


def img_scale(img, scale):
    size = round(img.get_width() * scale), round(img.get_height() * scale)
    return pygame.transform.scale(img, size)


def change_img_size(img, size):
    return pygame.transform.scale(img, size)


def rotate_image(win, img, top_left, angle):
    rotated_img = pygame.transform.rotate(img, angle)
    new_rect = rotated_img.get_rect(  center=img.get_rect(topleft=top_left).center)
    win.blit(rotated_img, new_rect.topleft)
