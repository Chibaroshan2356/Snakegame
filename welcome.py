import pygame
import time
from auth import attempt_login, attempt_register
from game import game_loop
from data_db import get_high_score, create_database, register_user
pygame.init()
white = (255, 255, 255)
bright_red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 100, 255)
black = (0, 0, 0)
yellow = (255, 255, 102)
gray = (169, 169, 169)
dis_width = 700
dis_height = 500
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')
background_image = pygame.image.load('gamestart.jpg')
background_image = pygame.transform.scale(background_image, (dis_width, dis_height))
game_background = pygame.image.load('gamebg.jpg')
game_background = pygame.transform.scale(game_background, (dis_width, dis_height))
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
input_font = pygame.font.SysFont("bahnschrift", 30)
clock = pygame.time.Clock()
error_message = ''
error_timer = 0
def render_error_message(msg, color):
    mesg = font_style.render(msg, True, color)
    text_width = mesg.get_width()
    dis.blit(mesg, [dis_width - text_width - 20, 20])
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(dis, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(dis, ic, (x, y, w, h))
    text_surface = input_font.render(msg, True, black)
    dis.blit(text_surface, (x + (w - text_surface.get_width()) // 2, y + (h - text_surface.get_height()) // 2))
def welcome_screen():
    global error_message, error_timer
    while True:
        dis.blit(background_image, (0, 0))
        button("Play", 250, 250, 200, 50, green, blue, login_screen)
        if error_message:
            render_error_message(error_message, bright_red if 'Invalid' in error_message else blue)
            if time.time() - error_timer > 2:
                error_message = ''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()
        clock.tick(30)
def login_screen():
    global error_message, error_timer
    username = ''
    password = ''
    active_username = False
    active_password = False
    input_box_username = pygame.Rect(250, 200, 400, 50)
    input_box_password = pygame.Rect(250, 280, 400, 50)
    while True:
        dis.blit(background_image, (0, 0))
        username_label = input_font.render("Username:", True, yellow)
        password_label = input_font.render("Password:", True, yellow)
        dis.blit(username_label, (50, 210))
        dis.blit(password_label, (50, 290))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_username.collidepoint(event.pos):
                    active_username = True
                    active_password = False
                elif input_box_password.collidepoint(event.pos):
                    active_password = True
                    active_username = False
                else:
                    active_username = False
                    active_password = False
            if event.type == pygame.KEYDOWN:
                if active_username:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
                if active_password:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode
        pygame.draw.rect(dis, white if active_username else gray, input_box_username)
        pygame.draw.rect(dis, white if active_password else gray, input_box_password)
        dis.blit(input_font.render(username, True, black), (input_box_username.x + 5, input_box_username.y + 5))
        dis.blit(input_font.render(password, True, black), (input_box_password.x + 5, input_box_password.y + 5))
        button("Login", 250, 350, 180, 50, green, blue, lambda: attempt_login_action(username, password))
        button("Register", 440, 350, 180, 50, green, blue, lambda: attempt_register_action(username, password))
        if error_message:
            render_error_message(error_message, bright_red if 'Invalid' in error_message else blue)
            if time.time() - error_timer > 2:
                error_message = ''
        pygame.display.update()
        clock.tick(30)
def attempt_login_action(username, password):
    global error_message, error_timer
    if not username or not password:
        error_message = "Username and password cannot be empty!"
        error_timer = time.time()
    elif attempt_login(username, password):
        game_loop(username, 15)
    else:
        error_message = "Invalid login details."
        error_timer = time.time()
def attempt_register_action(username, password):
    global error_message, error_timer
    if not username or not password:
        error_message = "Username and password cannot be empty!"
        error_timer = time.time()
    else:
        register_user(username, password)
        error_message = "Registration successful!"
        error_timer = time.time()
welcome_screen()