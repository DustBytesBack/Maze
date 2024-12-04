import pygame
import random as rd
import os

def compute_delay_and_width_tick(TILE):
    
    if TILE < 15:
        return 0  # No delay when TILE < 15
    else:
        m = 40 / (7*4)  # Slope
        c = -600 / (7*4)  # Y-intercept
        delay = m * TILE + c

    
    m = 3 / 7  # Slope
    c = -10 / 7  # Y-intercept
    line_width = m * TILE + c
    
    if TILE <= 20:
        tick =0
    else:
        tick = TILE * 0.5

    return int(delay), int(line_width),int(tick)

def get_tile_size():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "560,128"
    pygame.init()
    input_screen = pygame.display.set_mode((400, 200))
    pygame.display.set_caption("Enter TILE Size")
    font = pygame.font.Font(None, 40)
    input_text = ""
    running = True
    while running:
        input_screen.fill((30, 30, 30))  # Background color
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to submit
                    if input_text.isdigit() and int(input_text) > 0:
                        return int(input_text)  # Return the valid TILE size
                elif event.key == pygame.K_BACKSPACE:  # Allow backspace to edit
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode  # Add typed character to input

        # Render input box
        input_box = pygame.Rect(50, 80, 300, 50)
        pygame.draw.rect(input_screen, (200, 200, 200), input_box, 2)
        text_surface = font.render(input_text, True, (255, 255, 255))
        input_screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))

        # Render instructions
        instructions = font.render("Enter TILE Size", True, (255, 255, 255))
        input_screen.blit(instructions, (10, 10))

        pygame.display.flip()
