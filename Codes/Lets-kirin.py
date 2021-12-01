import pygame
import sys
from database import Database
from load import load_image #load_sound, load_music
from menu import *
from mode_single import *
from mode_time import *
from mode_pvp import *

if not pygame.mixer:
    print('Warning, sound disablead')
if not pygame.font:
    print('Warning, fonts disabled')

BACK = 0

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

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

# Menu - Highscore
menu, menuRect = load_image("menu.png")
menuRect.midtop = screen.get_rect().midtop

# Prepare game objects
clockTime = 60  # maximum FPS
clock = pygame.time.Clock()  
font = pygame.font.Font(None, 36)

# 데베 함수 메뉴 구현
hiScores=Database().getScores()
soundFX = Database().getSound()
music = Database().getSound(music=True)
# print(hiScores)
# print(len(hiScores))
highScoreTexts = [font.render("NAME", 1, RED), #폰트 렌터
                    font.render("SCORE", 1, RED),
                    font.render("ACCURACY", 1, RED)]
highScorePos = [highScoreTexts[0].get_rect(
                    topleft=screen.get_rect().inflate(-100, -100).topleft),
                highScoreTexts[1].get_rect(
                    midtop=screen.get_rect().inflate(-100, -100).midtop),
                highScoreTexts[2].get_rect(
                    topright=screen.get_rect().inflate(-100, -100).topright)]
for hs in hiScores:
    highScoreTexts.extend([font.render(str(hs[x]), 1, BLACK)
                            for x in range(3)])
    highScorePos.extend([highScoreTexts[x].get_rect(
        topleft=highScorePos[x].bottomleft) for x in range(-3, 0)])

# temp - only load
title, titleRect = load_image('title.png')
titleRect.midtop = screen.get_rect().inflate(0, -200).midtop

# Main menu 게임 메인 메뉴
# 폰트 렌더 함수 font.render('글씨',1(옵션인가봄),색깔)
# 폰트 위치 함수 font객체.get_rect(위치선언변수=기준이미지객체.inflate(좌,표).찐위치)    
startText = font.render('SELECT MODES', 1, BLACK)
startPos = startText.get_rect(midtop=titleRect.inflate(0, 100).midbottom)
hiScoreText = font.render('HIGH SCORES', 1, BLACK)
hiScorePos = hiScoreText.get_rect(topleft=startPos.bottomleft)
fxText = font.render('SOUND FX ', 1, BLACK)
fxPos = fxText.get_rect(topleft=hiScorePos.bottomleft)
fxOnText = font.render('ON', 1, RED)
fxOffText = font.render('OFF', 1, RED)
fxOnPos = fxOnText.get_rect(topleft=fxPos.topright)
fxOffPos = fxOffText.get_rect(topleft=fxPos.topright)
musicText = font.render('MUSIC', 1, BLACK)
musicPos = fxText.get_rect(topleft=fxPos.bottomleft)
musicOnText = font.render('ON', 1, RED) 
musicOffText = font.render('OFF', 1, RED)
musicOnPos = musicOnText.get_rect(topleft=musicPos.topright)
musicOffPos = musicOffText.get_rect(topleft=musicPos.topright)
helpText=font.render('HELP',1,BLACK)
helpPos=helpText.get_rect(topleft=musicPos.bottomleft)
quitText = font.render('QUIT', 1, BLACK)
quitPos = quitText.get_rect(topleft=helpPos.bottomleft)
selectText = font.render('*', 1, BLACK)
selectPos = selectText.get_rect(topright=startPos.topleft)

# Select Mode 안 글씨
singleText = font.render('SINGLE MODE', 1, BLACK)
singlePos = singleText.get_rect(midtop=titleRect.inflate(0, 100).midbottom)
timeText = font.render('TIME MODE', 1, BLACK)
timePos = timeText.get_rect(topleft=singlePos.bottomleft)
pvpText = font.render('PVP MODE ', 1, BLACK)
pvpPos = pvpText.get_rect(topleft=timePos.bottomleft)
backText=font.render('BACK',1,BLACK)
backPos=backText.get_rect(topleft=pvpPos.bottomleft)
selectText = font.render('*', 1, BLACK)
selectPos = selectText.get_rect(topright=singlePos.topleft)

selection = 1
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
            if userSelection==1:
                pageResult=Menu().select_game_page()
                if pageResult==BACK: #back
                    flag=False
                elif (pageResult=='SingleMode' or 
                    pageResult=='TimeMode' or
                    pageResult=='PvpMode'):
                    flag=False
                    inMainMenu=False 
            elif userSelection==2:
                pageResult=Menu().score_page()
                if pageResult==BACK:
                    flag=False
            elif userSelection==6:
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