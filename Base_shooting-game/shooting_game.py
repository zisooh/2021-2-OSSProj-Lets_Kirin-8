import pygame
import random
from collections import deque

from sprites import (MasterSprite, Ship, Alien, Missile, BombPowerup,
                     ShieldPowerup, DoublemissilePowerup, FriendPowerup, Explosion, Siney, Spikey, Fasty,
                     Roundy, Crawly)
from database import Database
from load import load_image, load_sound, load_music
from menu import *
from mode_single import *

if not pygame.mixer:
    print('Warning, sound disablead')
if not pygame.font:
    print('Warning, fonts disable d')

BACK = 0


BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

direction = {None: (0, 0), pygame.K_UP: (0, -2), pygame.K_DOWN: (0, 2),
             pygame.K_LEFT: (-2, 0), pygame.K_RIGHT: (2, 0)}

def main(): 
    # Initialize everything
    pygame.mixer.pre_init(11025, -16, 2, 512)
    pygame.init()
    screen_width = 500   # 스크린가로
    screen_height = 500  # 스크린세로
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Let\'s Kirin!")
    pygame.mouse.set_visible(0)

    def kill_alien(alien, aliensLeftThisWave, score) :
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
# size stars
    background = pygame.Surface((500, 2000))
    background = background.convert()
    background.fill((0, 0, 0))
    backgroundLoc = 1500

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

    # Game field
    field1, field1Rect = load_image("field.png")
    field2, field2Rect = load_image("field.png")
    field1Rect.midtop = screen.get_rect().midtop
    field2Rect.midbottom = field1Rect.midtop

# Prepare game objects
    speed = 1.5
    MasterSprite.speed = speed
    alienPeriod = 60 / speed
    clockTime = 60  # maximum FPS
    clock = pygame.time.Clock()
    ship = Ship()
    
    initialAlienTypes = (Siney, Spikey)
    # 수정
    powerupTypes = (BombPowerup, ShieldPowerup, DoublemissilePowerup, FriendPowerup)

    # pause
    pause,pauseRect = load_image('pause.png')
    pauseRect.midtop = screen.get_rect().midtop
    pauseMenu = False

    # Sprite groups
    alldrawings = pygame.sprite.Group()
    allsprites = pygame.sprite.RenderPlain((ship,))
    MasterSprite.allsprites = allsprites
    Alien.pool = pygame.sprite.Group(
        [alien() for alien in initialAlienTypes for _ in range(5)])
    Alien.active = pygame.sprite.Group()
    Missile.pool = pygame.sprite.Group([Missile() for _ in range(10)]) 
    Missile.active = pygame.sprite.Group()
    Explosion.pool = pygame.sprite.Group([Explosion() for _ in range(10)])
    Explosion.active = pygame.sprite.Group()
    
    # doublemissile = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    # life
    life1, life1Rect = load_image('heart1.png')
    life2, life2Rect = load_image('heart2.png')
    life3, life3Rect = load_image('heart3.png')

    # Sounds
    missile_sound = load_sound('missile.ogg')
    bomb_sound = load_sound('bomb.ogg')
    alien_explode_sound = load_sound('alien_explode.ogg')
    ship_explode_sound = load_sound('ship_explode.ogg')
    load_music('music_loop.ogg')

    alienPeriod = clockTime // 2
    curTime = 0
    aliensThisWave, aliensLeftThisWave, Alien.numOffScreen = 10, 10, 10
    wave = 1
    # 내려오는 미사일 먹으면 8초동안 spacebar로 사용 가능
    doublemissile = False
    # 수정
    friendship = False
    bombsHeld = 3
    score = 0
    missilesFired = 0
    powerupTime = 10 * clockTime
    powerupTimeLeft = powerupTime
    betweenWaveTime = 3 * clockTime
    betweenWaveCount = betweenWaveTime
    betweenDoubleTime = 8 * clockTime
    betweenDoubleCount = betweenDoubleTime
    font = pygame.font.Font(None, 36)
    inMenu = True

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

   # load만 일단
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

    # menuDict = {1: startPos, 2: hiScorePos, 3:fxPos, 4: musicPos, 5:helpPos,6: quitPos}
    selection = 1
    showSelectModes=False
    showHiScores = False

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
    inSelectMenu=False
    userSelection=Menu().inMenu_page()
    if userSelection==1:
        inSelectMenu=True
    elif userSelection==6:
        return


    showSingleMode = False
    showTimeMode = False
    showPvpMode = False
    selectModeDict = {1:singlePos,2:timePos,3:pvpPos,4:backPos}
    selection = 1
    while inSelectMenu:
                clock.tick(clockTime)
        #blit()
                screen.blit(background, (0, 0))
                screen.blit(main_menu, main_menuRect)

                for event in pygame.event.get():
                    if (event.type == pygame.QUIT):
                        return
                    elif (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_RETURN):
                        if showSingleMode:
                            showSingleMode = False
                        elif showTimeMode:
                            showTimeMode = False
                        elif showPvpMode:
                            showPvpMode = False
                        elif selection == 1:
                            inSelectMenu = False
                            selectMode = 'SingleMode'
                            ship.initializeKeys()
                        elif selection == 2:
                            inSelectMenu = False
                            selectMode = 'TimeMode'
                            ship.initializeKeys()
                        elif selection == 3:
                            inSelectMenu = False
                            selectMode = 'PvpMode'
                            ship.initializeKeys()
                        elif selection == 4:
                            inMenu = True
                            inSelectMenu = False
                    elif (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_UP
                        and selection > 1
                        and not showSingleMode
                        and not showTimeMode
                        and not showPvpMode):
                        selection -= 1
                    elif (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_DOWN
                        and selection < len(selectModeDict)
                        and not showSingleMode
                        and not showTimeMode
                        and not showPvpMode):
                        selection += 1
                selectPos = selectText.get_rect(topright=selectModeDict[selection].topleft)

                textOverlays = zip([singleText,timeText,pvpText,selectText,backText],[singlePos,timePos,pvpPos,selectPos,backPos])
                for txt, pos in textOverlays:
                    screen.blit(txt, pos)
                
                pygame.display.flip()


#########################
#    Start Game Loop    #
#########################

    if selectMode == 'SingleMode':
        Single.play()
    elif selectMode == 'TimeMode':
        print('Time play')
        #Time.play()
    elif selectMode == 'PvpMode':
        print('Pvp play')
        #Pvp.play()    


# Single Mode. 클래스화 예정
    restart = True
    while restart == True:

        # Reset Sprite groups
        alldrawings = pygame.sprite.Group()
        allsprites = pygame.sprite.RenderPlain((ship,))
        MasterSprite.allsprites = allsprites
        Alien.pool = pygame.sprite.Group(
            [alien() for alien in initialAlienTypes for _ in range(5)])
        Alien.active = pygame.sprite.Group()
        Missile.pool = pygame.sprite.Group([Missile() for _ in range(10)]) 
        Missile.active = pygame.sprite.Group()
        Explosion.pool = pygame.sprite.Group([Explosion() for _ in range(10)])
        Explosion.active = pygame.sprite.Group()

        # Reset game contents
        curTime = 0
        aliensThisWave, aliensLeftThisWave, Alien.numOffScreen = 10, 10, 10
        wave = 1
        doublemissile = False
        bombsHeld = 3
        score = 0
        missilesFired = 0
        powerupTime = 10 * clockTime
        powerupTimeLeft = powerupTime
        betweenWaveTime = 3 * clockTime
        betweenWaveCount = betweenWaveTime
        betweenDoubleTime = 8 * clockTime
        betweenDoubleCount = betweenDoubleTime
        ship.alive = True

        # pause 메뉴 글씨  
        restartText = font.render('RESTART GAME', 1, BLACK)
        restartPos = restartText.get_rect(bottomleft=hiScorePos.topleft)  
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

        # 본게임시작
        while ship.alive:
            clock.tick(clockTime)

            if aliensLeftThisWave >= 20:
                powerupTimeLeft -= 1
            if powerupTimeLeft <= 0:
                powerupTimeLeft = powerupTime
                random.choice(powerupTypes)().add(powerups, allsprites)

        # Event Handling
            for event in pygame.event.get():
                if (event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN
                        and event.key == pygame.K_ESCAPE):
                    return
                # Ship Moving
                elif (event.type == pygame.KEYDOWN
                    and event.key in direction.keys()):
                    ship.horiz += direction[event.key][0] * speed
                    ship.vert += direction[event.key][1] * speed
                elif (event.type == pygame.KEYUP
                    and event.key in direction.keys()):
                    ship.horiz -= direction[event.key][0] * speed
                    ship.vert -= direction[event.key][1] * speed
                # Missile
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_SPACE):
                    if doublemissile :
                        Missile.position(ship.rect.topleft)
                        Missile.position(ship.rect.topright)
                        missilesFired += 2
                    else : 
                        Missile.position(ship.rect.midtop)
                        missilesFired += 1
                    if soundFX:
                        missile_sound.play()
                # Bomb
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_b):
                    if bombsHeld > 0:
                        bombsHeld -= 1
                        newBomb = ship.bomb()
                        newBomb.add(bombs, alldrawings)
                        if soundFX:
                            bomb_sound.play()
                # Pause
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_p):
                    pauseMenu = True
                    menuDict = {1: restartPos, 2: hiScorePos, 3: fxPos, 
                                4: musicPos, 5: helpPos, 6: quitPos}
                    
                    while pauseMenu:
                        clock.tick(clockTime)

                        screen.blit(background, (0, 0))
                        screen.blit(pause, pauseRect)

                        for event in pygame.event.get():
                            if (event.type == pygame.QUIT):
                                return
                            elif (event.type == pygame.KEYDOWN  # unpause
                                and event.key == pygame.K_p):
                                pauseMenu = False
                            # Pause Menu
                            elif (event.type == pygame.KEYDOWN
                                and event.key == pygame.K_RETURN):
                                if showHiScores:
                                    showHiScores = False
                                elif selection == 1:    
                                    pauseMenu = False
                                    ship.alive = False
                                elif selection == 2:
                                    showHiScores = True
                                elif selection == 3:
                                    soundFX = not soundFX
                                    if soundFX:
                                        missile_sound.play()
                                    Database.setSound(int(soundFX))
                                elif selection == 4 and pygame.mixer:
                                    music = not music
                                    if music:
                                        pygame.mixer.music.play(loops=-1)
                                    else:
                                        pygame.mixer.music.stop()
                                    Database.setSound(int(music), music=True)
                                elif selection == 5:
                                    return
                                elif selection == 6:
                                    return
                            elif (event.type == pygame.KEYDOWN
                                and event.key == pygame.K_UP
                                and selection > 1
                                and not showHiScores):
                                selection -= 1
                            elif (event.type == pygame.KEYDOWN
                                and event.key == pygame.K_DOWN
                                and selection < len(menuDict)
                                and not showHiScores):
                                selection += 1
                            

                        selectPos = selectText.get_rect(topright=menuDict[selection].topleft)

                        if showHiScores:
                            textOverlays = zip(highScoreTexts, highScorePos)
                        else:
                            textOverlays = zip([restartText, hiScoreText, helpText, fxText,
                                                musicText, quitText, selectText,
                                                fxOnText if soundFX else fxOffText,
                                                musicOnText if music else musicOffText],
                                                [restartPos, hiScorePos, helpPos, fxPos,
                                                musicPos, quitPos, selectPos,
                                                fxOnPos if soundFX else fxOffPos,
                                                musicOnPos if music else musicOffPos])
                        for txt, pos in textOverlays:
                            screen.blit(txt, pos)

                        alldrawings.update()
                        pygame.display.flip()
                

        # Collision Detection
            # Aliens
            for alien in Alien.active:
                for bomb in bombs:
                    if pygame.sprite.collide_circle(
                            bomb, alien) and alien in Alien.active:
                        if alien.pType != 'white' :
                            alien.table()
                            Explosion.position(alien.rect.center)
                            aliensLeftThisWave, score = kill_alien(alien, aliensLeftThisWave, score)
                        missilesFired += 1
                        if soundFX:
                            alien_explode_sound.play()
                for missile in Missile.active:
                    if pygame.sprite.collide_rect(
                            missile, alien) and alien in Alien.active:
                        missile.table()
                        if alien.pType != 'white' :
                            alien.table()
                            Explosion.position(alien.rect.center)
                            aliensLeftThisWave, score = kill_alien(alien, aliensLeftThisWave, score)
                        if soundFX:
                            alien_explode_sound.play()
                if pygame.sprite.collide_rect(alien, ship):
                    if ship.shieldUp:
                        alien.table()
                        Explosion.position(alien.rect.center)
                        aliensLeftThisWave, score = kill_alien(alien, aliensLeftThisWave, score)
                        missilesFired += 1
                        ship.shieldUp = False
                    elif ship.life > 1:   # life
                        alien.table()
                        Explosion.position(alien.rect.center)
                        aliensLeftThisWave -= 1
                        score += 1
                        ship.life -= 1
                    else:
                        restart = False
                        ship.alive = False
                        ship.remove(allsprites)
                        Explosion.position(ship.rect.center)
                        if soundFX:
                            ship_explode_sound.play()

            # PowerUps
            for powerup in powerups:
                if pygame.sprite.collide_circle(powerup, ship):
                    if powerup.pType == 'bomb':
                        bombsHeld += 1
                    elif powerup.pType == 'shield':
                        ship.shieldUp = True
                    elif powerup.pType == 'doublemissile' :
                        doublemissile = True
                    elif powerup.pType == 'friendship' :
                        friendship = True    
                    powerup.kill()
                elif powerup.rect.top > powerup.area.bottom:
                    powerup.kill()

        # Update Aliens
            if curTime <= 0 and aliensLeftThisWave > 0:
                Alien.position()
                curTime = alienPeriod
            elif curTime > 0:
                curTime -= 1

        # Update text overlays
            waveText = font.render("Wave: " + str(wave), 1, BLACK)
            leftText = font.render("Bears Left: " + str(aliensLeftThisWave), 1, BLACK)
            scoreText = font.render("Score: " + str(score), 1, BLACK)
            bombText = font.render("Fart Bombs: " + str(bombsHeld), 1, BLACK)
            #lifeText = font.render("Life: ", 1, BLACK)

            wavePos = waveText.get_rect(topleft=screen.get_rect().topleft)
            leftPos = leftText.get_rect(midtop=screen.get_rect().midtop)
            scorePos = scoreText.get_rect(topright=screen.get_rect().topright)
            bombPos = bombText.get_rect(bottomleft=screen.get_rect().bottomleft)
            #lifePos = lifeText.get_rect(topleft=wavePos.bottomleft)

            text = [waveText, leftText, scoreText, bombText] #, lifeText]
            textposition = [wavePos, leftPos, scorePos, bombPos] #, lifePos]

            if doublemissile:
                if betweenDoubleCount > 0:
                    betweenDoubleCount -= 1
                elif betweenDoubleCount == 0:
                    doublemissile = False
                    betweenDoubleCount = betweenDoubleTime

        # Detertmine when to move to next wave
            if aliensLeftThisWave <= 0:
                if betweenWaveCount > 0:
                    betweenWaveCount -= 1
                    nextWaveText = font.render(
                        'Wave ' + str(wave + 1) + ' in', 1, BLACK)
                    nextWaveNum = font.render(
                        str((betweenWaveCount // clockTime) + 1), 1, BLACK)
                    text.extend([nextWaveText, nextWaveNum])
                    nextWavePos = nextWaveText.get_rect(
                        center=screen.get_rect().center)
                    nextWaveNumPos = nextWaveNum.get_rect(
                        midtop=nextWavePos.midbottom)
                    textposition.extend([nextWavePos, nextWaveNumPos])
                    if wave % 4 == 0:
                        speedUpText = font.render('SPEED UP!', 1, RED)
                        speedUpPos = speedUpText.get_rect(
                            midtop=nextWaveNumPos.midbottom)
                        text.append(speedUpText)
                        textposition.append(speedUpPos)
                elif betweenWaveCount == 0:
                    if wave % 4 == 0:
                        speed += 0.5
                        MasterSprite.speed = speed
                        ship.initializeKeys()
                        aliensThisWave = 10
                        aliensLeftThisWave = Alien.numOffScreen = aliensThisWave
                    else:
                        aliensThisWave *= 2
                        aliensLeftThisWave = Alien.numOffScreen = aliensThisWave
                    if wave == 1:
                        Alien.pool.add([Fasty() for _ in range(5)])
                    if wave == 2:
                        Alien.pool.add([Roundy() for _ in range(5)])
                    if wave == 3:
                        Alien.pool.add([Crawly() for _ in range(5)])
                    wave += 1
                    betweenWaveCount = betweenWaveTime

            textOverlays = zip(text, textposition)

        # Update and draw all sprites and text
            screen.blit(pause, pauseRect)
            
            field1Rect.y += 2 # speed? float(x) / int(o)
            field2Rect.y += 2
            if field1Rect.y >= screen_height:
                field1Rect.midbottom = field2Rect.midtop
            if field2Rect.y >= screen_height:
                field2Rect.midbottom = field1Rect.midtop

            screen.blit(field1, field1Rect)
            screen.blit(field2, field2Rect)
                
            allsprites.update()
            allsprites.draw(screen)
            alldrawings.update()
            for txt, pos in textOverlays:
                screen.blit(txt, pos)

        # Update life
            life1Rect.topleft = wavePos.bottomleft #lifePos.topright
            life2Rect.topleft = wavePos.bottomleft #lifePos.topright
            life3Rect.topleft = wavePos.bottomleft #lifePos.topright

            if ship.life == 3:
                screen.blit(life3, life3Rect)
            elif ship.life == 2:
                screen.blit(life2, life2Rect)
            elif ship.life == 1:
                screen.blit(life1, life1Rect)

            pygame.display.flip()



        accuracy = round(score / missilesFired, 4) if missilesFired > 0 else 0.0
        isHiScore = len(hiScores) < Database().numScores or score > hiScores[-1][1]
        name = ''
        nameBuffer = []


#########################
#    After Game Loop    #
#########################

    while True:
        clock.tick(clockTime)

    # Event Handling
        for event in pygame.event.get():
            if (event.type == pygame.QUIT
                or not isHiScore
                and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE):
                return False
            elif (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_RETURN
                  and not isHiScore):
                return True
            elif (event.type == pygame.KEYDOWN
                  and event.key in Keyboard.keys.keys()
                  and len(nameBuffer) < 8):
                nameBuffer.append(Keyboard.keys[event.key])
                name = ''.join(nameBuffer)
            elif (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_BACKSPACE
                  and len(nameBuffer) > 0):
                nameBuffer.pop()
                name = ''.join(nameBuffer)
            elif (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_RETURN
                  and len(name) > 0):
                Database().setScore(hiScores,name, score, accuracy)
                return True  

        if isHiScore:
            hiScoreText = font.render('SCORE', 1, RED)
            hiScorePos = hiScoreText.get_rect(
                midbottom=screen.get_rect().center)
            scoreText = font.render(str(score), 1, BLACK)
            scorePos = scoreText.get_rect(midtop=hiScorePos.midbottom)
            enterNameText = font.render('ENTER YOUR NAME:', 1, RED)
            enterNamePos = enterNameText.get_rect(midtop=scorePos.midbottom)
            nameText = font.render(name, 1, WHITE)
            namePos = nameText.get_rect(midtop=enterNamePos.midbottom)
            textOverlay = zip([hiScoreText, scoreText,
                               enterNameText, nameText],
                              [hiScorePos, scorePos,
                               enterNamePos, namePos])
        else:

            gameOverText = font.render('GAME OVER', 1, BLACK)
            gameOverPos = gameOverText.get_rect(
                center=screen.get_rect().center)
            scoreText = font.render('SCORE: {}'.format(score), 1, BLACK)
            scorePos = scoreText.get_rect(midtop=gameOverPos.midbottom)
            textOverlay = zip([gameOverText, scoreText],
                              [gameOverPos, scorePos])

    # Update and draw all sprites
        screen.blit(pause, pauseRect)
        
        field1Rect.y += 2 # speed? float(x) / int(o)
        field2Rect.y += 2
        if field1Rect.y >= screen_height:
            field1Rect.midbottom = field2Rect.midtop
        if field2Rect.y >= screen_height:
            field2Rect.midbottom = field1Rect.midtop

        screen.blit(field1, field1Rect)
        screen.blit(field2, field2Rect)

        allsprites.update()
        allsprites.draw(screen)
        alldrawings.update()
        for txt, pos in textOverlay:
            screen.blit(txt, pos)
        pygame.display.flip()


if __name__ == '__main__':
    while(main()):
        pass
