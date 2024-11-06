import pygame
import random
from data_db import get_high_score, update_high_score
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
game_background = pygame.image.load('gamebg.jpg')
game_background = pygame.transform.scale(game_background, (dis_width, dis_height))
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
input_font = pygame.font.SysFont("bahnschrift", 30)
clock = pygame.time.Clock()
snake_block = 10
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])
def display_score(score, high_score):
    score_text = score_font.render(f"Your Score: {score}  |  High Score: {high_score}", True, bright_red)
    dis.blit(score_text, [0, 0])
    pygame.draw.line(dis, black, (0, 50), (dis_width, 50), 4)
def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, bright_red, [x[0], x[1], snake_block, snake_block])
def game_loop(player_name, snake_speed):
    game_over = False
    game_close = False
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    snake_list = []
    length_of_snake = 1
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(50, dis_height - snake_block) / 10.0) * 10.0
    high_score = get_high_score(player_name)
    while not game_over:
        while game_close:
            dis.blit(game_background, (0, 0))
            message("You Lost! Press Q-Quit or C-Play Again", bright_red)
            display_score(length_of_snake - 1, high_score)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        if length_of_snake - 1 > high_score:
                            update_high_score(player_name, length_of_snake - 1)
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        if length_of_snake - 1 > high_score:
                            update_high_score(player_name, length_of_snake - 1)
                        game_loop(player_name, snake_speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 50:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.blit(game_background, (0, 0))
        pygame.draw.rect(dis, yellow, [foodx, foody, snake_block, snake_block])
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True
        draw_snake(snake_block, snake_list)
        display_score(length_of_snake - 1, high_score)
        pygame.display.update()
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(50, dis_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
        clock.tick(snake_speed)
    pygame.quit()
    quit()