import pygame
import variables
import colors
import random

# main
pygame.init()
pygame.display.set_caption('Python snake')
screen = pygame.display.set_mode(variables.WINDOW_MODE)
font = pygame.font.Font(None, 22)

clock = pygame.time.Clock()

def generate_food(snake_position):
    while True:
        x = random.randint(0, 39) * variables.BLOCK_SIZE
        y = random.randint(2, 41) * variables.BLOCK_SIZE

        food_position = (x, y)

        if food_position not in snake_position:
            return food_position

def draw(snake_position, food_position):
    pygame.draw.rect(screen, colors.FOOD, [*food_position, variables.BLOCK_SIZE, variables.BLOCK_SIZE])

    for x, y in snake_position:
        pygame.draw.rect(screen, colors.SNAKE, [x, y, variables.BLOCK_SIZE, variables.BLOCK_SIZE])

def move_snake(snake_position, direction):
    head_x, head_y = snake_position[0]

    new_position = (head_x, head_y)

    if direction == 'Up':
        new_position = (head_x, head_y - variables.BLOCK_SIZE)
    elif direction == 'Down':
        new_position = (head_x, head_y + variables.BLOCK_SIZE)
    elif direction == 'Left':
        new_position = (head_x - variables.BLOCK_SIZE, head_y)
    elif direction == 'Right':
        new_position = (head_x + variables.BLOCK_SIZE, head_y)

    snake_position.insert(0, new_position)
    snake_position.pop(-1)

def define_direction(event, current_direction):
    key = event.__dict__.get('key')

    new_direction = variables.KEY_MAP[key]

    all_directions = variables.KEY_MAP.values()
    opposite_directions = [set(('Up', 'Down')), set(('Left', 'Right'))]

    if new_direction in all_directions and {new_direction, current_direction} not in opposite_directions:
        return new_direction
    
    return current_direction

def check_colisions(snake_position):
    head_x, head_y = snake_position[0]

    return (
      head_x in (-variables.BLOCK_SIZE, screen.get_width())
      or head_y in (variables.BLOCK_SIZE, screen.get_height())
      or (head_x, head_y) in snake_position[1:]
    )

def check_food_colisions(snake_position, food_position):
    if snake_position[0] == food_position:
        snake_position.append(snake_position[-1])
        return True
    return False

def main():
    score = 0
    direction = 'Right'

    snake_position = [(100, 100), (80, 100), (60, 100)]
    food_position = generate_food(snake_position)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                direction = define_direction(event, direction)
        
        text = font.render(f'Score: {score}', True, colors.TEXT)
        screen.fill(colors.BACKGROUND)
        screen.blit(text, (5, 5))

        draw(snake_position, food_position)

        pygame.display.update()

        move_snake(snake_position, direction)

        if check_food_colisions(snake_position, food_position):
            food_position = generate_food(snake_position)
            score += 1

        if (check_colisions(snake_position)):
            return
        
        clock.tick(15)
            
main()