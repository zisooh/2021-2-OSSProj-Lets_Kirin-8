import pygame
import sys
from database import Database
from load import load_image #load_sound, load_music
from menu import *
from mode_single import *
from mode_time import  *
from mode_pvp import *

if not pygame.mixer:
    print('Warning, sound disablead')
if not pygame.font:
    print('Warning, fonts disabled')

BACK = 0

# BLACK = (0, 0, 0)
# RED = (255, 0, 0)
# WHITE = (255, 255, 255)

direction = {None: (0, 0), pygame.K_UP: (0, -2), pygame.K_DOWN: (0, 2),
             pygame.K_LEFT: (-2, 0), pygame.K_RIGHT: (2, 0)}

# Initialize everything
pygame.mixer.pre_init(11025, -16, 2, 512)
pygame.init()
screen_width = 500   # 스크린가로
screen_height = 500  # 스크린세로
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Let's Kirin!")
pygame.mouse.set_visible(0)

# # Create the background which will scroll and loop over a set of different
# background = pygame.Surface((500, 2000))
# background = background.convert()
# background.fill((0, 0, 0))

# # Display the background
# screen.blit(background, (0, 0))
# pygame.display.flip()

# # Prepare background image
# # Main_menu
# main_menu, main_menuRect = load_image("main_menu.png")
# main_menuRect.midtop = screen.get_rect().midtop

# # Menu - Highscore
# menu, menuRect = load_image("menu.png")
# menuRect.midtop = screen.get_rect().midtop

# Prepare game objects
# clockTime = 60  # maximum FPS
# clock = pygame.time.Clock()  
# font = pygame.font.Font(None, 36)

# 데베 함수 메뉴 구현
hiScores=Database().getScores()
soundFX = Database.getSound()
music = Database.getSound(music=True)
if music and pygame.mixer:
    pygame.mixer.music.play(loops=-1)

# selection = 1
showSelectModes=False
showHiScores = False
#--------------------------------------------------------------------#

#########################
#    Init Menu Loop     #
#########################

# inInitMenu loop = Init_page & login_page & signup_page
# Init_page = 1. log in 2. sign up 3. Quit 
# login_page = enter ID, enter PWD, BACK
# signup_page = enter ID, enter PWD, BACK
inInitMenu=True
while inInitMenu:
    userSelection=Menu().init_page()
    flag=True
    while flag:   
        if userSelection==1 or userSelection==2: #로그인/회원가입
            pageResult=Menu().login_sign_page(userSelection)
            if pageResult==BACK: #back
                flag=False  
            else: 
                # print(pageResult)
                flag=False
                inInitMenu=False          
        elif userSelection==3: #끝내기
            pygame.quit()
            sys.exit()


# After login - infinite loop
windowShow = True
while windowShow:

#########################
#    Start Menu Loop    #
#########################

    inMainMenu=True
    while inMainMenu:
        userSelection=Menu().inMenu_page()
        flag=True
        while flag:
            if userSelection == 1:
                pageResult=Menu().select_game_page()
                if pageResult == BACK: #back
                    flag = False
                elif (pageResult == 'SingleMode' or 
                    pageResult == 'TimeMode' or
                    pageResult == 'PvpMode'):
                    flag = False
                    inMainMenu = False 
            elif userSelection == 2:
                pageResult = Menu().score_page()
                if pageResult == BACK:
                    flag = False
            elif userSelection == 6:
                pygame.quit()
                sys.exit()


#########################
#    Start Game Loop    #
#########################

    if pageResult == 'SingleMode':
        print('Single mode play')
        Single.playGame()
    elif pageResult == 'TimeMode':
        print('Time mode play')
        Time.playGame()
    elif pageResult == 'PvpMode':
        print('Pvp mode play')
        Pvp.playGame()    
    
    print("Game End")   