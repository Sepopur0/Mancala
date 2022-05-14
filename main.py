from funcs import *


def main():
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Ô ăn quan")
    step_1 = -9
    step_2 = [-9, 0, 0]
    step_3 = []
    step_fin = -2
    while True:
        step_1 = start_screen(screen)
        step_2 = options(screen, step_1)
        if step_2[1] == -2:
            step_2 = [-9, 0, 0]
            continue
        step_3 = everything(screen, step_1, step_2[0], step_2[2], step_2[1])
        if step_3[0] == -2:
            step_2 = [-9, 0, 0]
            step_3 = []
            continue
        step_fin = winner(screen, step_3)
        if step_fin == -2:
            step_2 = [-9, 0, 0]
            step_3 = []
            continue

if __name__ == "__main__":
    main()
