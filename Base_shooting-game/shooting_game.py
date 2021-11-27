import pygame
import random

from sprites import (MasterSprite, Ship, Friendship, Alien, Missile, BombPowerup,
                     ShieldPowerup, DoublemissilePowerup, FriendPowerup, Explosion, Siney, Spikey, Fasty,
                     Roundy, Crawly)
from database import Database
from load import load_image, load_sound, load_music
from menu import *
from mode_single import *
from mode_time import *

if not pygame.mixer:
    print('Warning, sound disablead')
if not pygame.font:
    print('Warning, fonts disabled')

BACK = 0

direction = {None: (0, 0), pygame.K_UP: (0, -2), pygame.K_DOWN: (0, 2),
             pygame.K_LEFT: (-2, 0), pygame.K_RIGHT: (2, 0)}

def main(): 
    # Initialize everything
    pygame.mixer.pre_init(11025, -16, 2, 512)
    pygame.init()
    screen_width = 500   # 스크린가로
    screen_height = 500  # 스크린세로
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Let's Kirin!")
    pygame.mouse.set_visible(0)


    def kill_alien(alien, aliensLeftThisWave, score) : # sprites 클래스에 넣을 수 있나욤
        aliensLeftThisWave -= 1
        if alien.pType == 'green':
            score += 1
        elif alien.pType == 'orange':
            score += 2
        elif alien.pType == 'red':
            score += 4
        elif alien.pType == 'yellow':
            score += 8
        return aliensLeftThisWave, score

# Create the background which will scroll and loop over a set of different
    background = pygame.Surface((500, 2000))
    background = background.convert()
    background.fill((0, 0, 0))

# Display the background
    screen.blit(background, (0, 0))
    pygame.display.flip()

# Prepare background image
    # Main_menu
    main_menu, main_menuRect = load_image("main_menu.png")
    main_menuRect.midtop = screen.get_rect().midtop

    # Menu
    img_menu, img_menuRect = load_image("menu.png")
    img_menuRect.midtop = screen.get_rect().midtop

# Prepare game objects
    # clockTime = 60  # maximum FPS
    # clock = pygame.time.Clock()  
    # font = pygame.font.Font(None, 36)

# Sound loop
    soundFX = Database().getSound() 
    music = Database.getSound(music=True) 
    if music and pygame.mixer: 
        pygame.mixer.music.play(loops=-1)

   # load만 일단
    title, titleRect = load_image('title.png')
    titleRect.midtop = screen.get_rect().inflate(0, -200).midtop


#########################
#    Init Menu Loop    #
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
                return


#########################
#    Start Menu Loop    #
#########################

    inMainMenu=True
    while inMainMenu:
        userSelection=Menu().inMenu_page()
        flag=True
        while flag:
            if userSelection==1:
                pageResult=Menu().select_game_page()
                if pageResult==BACK: #back
                    flag=False
                elif (pageResult=='SingleMode' or 
                    pageResult=='TimeMode' or
                    pageResult=='PVPMode'):
                    flag=False
                    inMainMenu=False 
            elif userSelection==2:
                pageResult=Menu().score_page()
                if pageResult==BACK:
                    flag=False
            elif userSelection==6:
                return

    

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
        #ship.initializeKeys() Pvp 클래스 안에 넣기
        #Pvp.play()    

if __name__ == '__main__':
    while(main()):
        pass
