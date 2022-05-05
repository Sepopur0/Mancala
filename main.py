from funcs import *


def main():
    step_1 = -9
    step_2 = [-9, 0]
    step_3 = [-9, 0]
    step_fin = -2
    while True:
        step_1 = start_screen(screen)
        step_2 = options(screen, step_1)
        if step_2[1] == -2:
            continue
        step_3 = everything(screen, step_1, step_2[0], step_2[1])
        if step_3 == -2:
            continue
        step_fin = winner(screen, step_3)
        if step_fin == -2:
            continue


main()
