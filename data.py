import numpy as np
import pygame
# import math
from pygame.constants import *
import sys
import random
pygame.init()
screen_width = 1300
screen_height = 650
button_width = 150
button_height = 40
#state
INIT_BOARD = np.full(12, 5)
INT_MAX = np.iinfo(np.int32).max
INT_MIN = np.iinfo(np.int32).min
# buttoncoordinate(left,top)
startbutton_coor = [(575, 300), (575,375), (575, 450)]
gamebutton_coor=[[475,545],[675,545]]
option_coor_0=[(375,500),(775,500),(775,575)]
direct_coor=[]
option_coor_1=[(375,500),(375,575),(775,500),(775,575)]
board_coor=[(930,270),(815,325),(705,325),(595,325),(485,325),
            (375,325),(270,270),(375,215),(485,215),(595,215),(705,215),(815,215)]
# font
font = pygame.font.SysFont('calibri', 25, True, False)
font_number = pygame.font.SysFont('calibri', 30, True, False)
font_title = pygame.font.SysFont('opensansregular',100,True,True)
# colors
black = (0, 0, 0)
white = (255, 255, 255)
boxcolor = (244, 199, 171) #mau o
scenery =(134, 84, 57)   #nen
shading = (215, 177, 157) #clickon
boxcontent= (64,34,24) #mau chu va mau da
rock_1=(128, 128, 128)
rock_2=(90,77,65)
rock=(54,69,79)
red=(139,0,0)
green=(0,139,0)
blue=(0,0,139)
playzonecolor=(198,139,89)
#boxcontent=(64,34,24) #mau chu

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ô ăn quan")
s_1 = pygame.Surface((150, 40))
s_1.fill(scenery)
pygame.draw.rect(s_1, shading, pygame.Rect(
        0, 0, button_width, button_height), 0, 40)
pygame.Surface.set_alpha(s_1, 100)
s=pygame.Surface((110,110))
s.fill(shading)
pygame.Surface.set_alpha(s,100)