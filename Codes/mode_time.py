import pygame
import random
import sys
from pygame.locals import *

from sprites import (MasterSprite, 
                     Kirin, Friendkirin, Bear, Leaf, Explosion, 
                     BombPowerup, ShieldPowerup, DoubleleafPowerup, FriendPowerup, LifePowerup,
                     Siney, Spikey, Fasty, Roundy, Crawly)
from database import Database
from load import load_image, load_sound, load_music
from menu import *

if not pygame.mixer:
    print('Warning, sound disablead')
if not pygame.font:
    print('Warning, fonts disabled')

BACK = 0
TIME = 1

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

direction = {None: (0, 0), pygame.K_UP: (0, -2), pygame.K_DOWN: (0, 2),
             pygame.K_LEFT: (-2, 0), pygame.K_RIGHT: (2, 0)}

class Time():
    def playGame(screen_size):     # 창크기조절: 메인에서 기준size argument 받아오기 / 적용 : V 표시
    # Initialize everything
        pygame.mixer.pre_init(11025, -16, 2, 512)
        pygame.init()
        ratio = (screen_size / 500)
        screen = pygame.display.set_mode((screen_size, screen_size))
        pygame.display.set_caption("Let's Kirin!")
        pygame.mouse.set_visible(0)

    # Score Function
        def kill_bear(bear, score) : # 남은 곰 개수 줄이는 역할 제거
            if bear.pType == 'green':
                score += 1
            elif bear.pType == 'orange':
                score += 2
            elif bear.pType == 'red':
                score += 4
            elif bear.pType == 'yellow':
                score += 8
            return score

       # Create the background which will scroll and loop over a set of different
        background = pygame.Surface((2000, 2000))
        background = background.convert()
        background.fill((0, 0, 0))

    # Display the background
        screen.blit(background, (0, 0))
        pygame.display.flip()

    # Prepare background image
        # Game field
        field1, field1Rect = load_image("field.png")
        field2, field2Rect = load_image("field.png")
        field1Rect.midtop = screen.get_rect().midtop
        field2Rect.midbottom = field1Rect.midtop

        # Menu - pause 메뉴 Highscore & help
        menu, menuRect = load_image("menu.png")
        menuRect.midtop = screen.get_rect().midtop
        
        # pause
        pause,pauseRect = load_image('pause.png')
        pauseRect.midtop = screen.get_rect().midtop
        pauseMenu = False        

    # Prepare game contents : non-reset
        # life
        life1, life1Rect = load_image('heart1.png')
        life2, life2Rect = load_image('heart2.png')
        life3, life3Rect = load_image('heart3.png')

        # Sounds
        leaf_sound = load_sound('leaf.ogg')
        bomb_sound = load_sound('bomb.ogg')
        bear_explode_sound = load_sound('bear_explode.ogg')
        kirin_explode_sound = load_sound('kirin_explode.ogg')
        load_music('menu_music_loop.ogg')

        # font
        font = pygame.font.Font(None, 36)
        beforeWaveCountFont = pygame.font.Font(None, 60)
        leftCountFont = pygame.font.Font(None, 60)

        # clock - 60 FPS game
        clockTime = 60  # maximum FPS
        clock = pygame.time.Clock()

        # speed
        speed = 2
        MasterSprite.speed = speed
        
        # object
        kirin = Kirin(screen_size)
        minikirin = Friendkirin(screen_size)
        initialBearTypes = (Siney, Spikey, Fasty, Roundy, Crawly)
        powerupTypes = (BombPowerup, ShieldPowerup, DoubleleafPowerup, 
                        FriendPowerup, LifePowerup)
        bombs = pygame.sprite.Group()
        powerups = pygame.sprite.Group()

    # High Score
        hiScores=Database().getTimeScores()
        soundFX = Database.getSound()
        music = Database.getSound(music=True)
        if music and pygame.mixer: 
            pygame.mixer.music.play(loops=-1)
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
    
    # pause menu text  
        blankText=font.render('            ',1,BLACK)
        blankPos=blankText.get_rect(topright=screen.get_rect().center)
        restartText = font.render('RESTART GAME', 1, BLACK)
        restartPos = restartText.get_rect(topleft=blankPos.bottomleft)  
        hiScoreText = font.render('HIGH SCORES', 1, BLACK)
        hiScorePos = hiScoreText.get_rect(topleft=restartPos.bottomleft)
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
        selectPos = selectText.get_rect(topright=restartPos.topleft)
        selection = 1
        showHiScores = False
        showHelp=False


    #########################
    #    Start Time Mode    #
    #########################

        restart = True
        while restart == True:

        # Prepare game objects : reset
            # Reset Sprite groups
            alldrawings = pygame.sprite.Group()
            allsprites = pygame.sprite.RenderPlain((kirin,))
            MasterSprite.allsprites = allsprites
            Bear.pool = pygame.sprite.Group(
                [bear(screen_size) for bear in initialBearTypes for _ in range(5)])
            Bear.active = pygame.sprite.Group()
            Leaf.pool = pygame.sprite.Group([Leaf(screen_size) for _ in range(10)]) 
            Leaf.active = pygame.sprite.Group()
            Explosion.pool = pygame.sprite.Group([Explosion(screen_size) for _ in range(10)])
            Explosion.active = pygame.sprite.Group()

            # Reset game contents
            bearsThisWave, bearsLeftThisWave, Bear.numOffScreen = 1000, 0, 1000
            friendkirin = False
            doubleleaf = False
            bombsHeld = 3
            score = 0
            leafFired = 0

            # speed
            speed = 2
            MasterSprite.speed = speed

            # Reset all time
            bearPeriod = clockTime // speed
            curTime = 0
            powerupTime = 4 * clockTime
            powerupTimeLeft = powerupTime
            beforeWaveTime = 4 * clockTime      # 게임시작 전 3, 2, 1...
            beforeWaveCount = beforeWaveTime
            leftTime = 60 * clockTime           # 타임모드 카운트다운
            leftCount = leftTime
            
            betweenDoubleTime = 8 * clockTime
            betweenDoubleCount = betweenDoubleTime
            friendkirinTime = 8 * clockTime
            friendkirinCount = friendkirinTime
            friendkirinLeafTime = 0.2 * clockTime
            friendkirinLeafCount = friendkirinLeafTime
            
            kirin.alive = True
            kirin.life = 3
            kirin.initializeKeys()


        # Start Game
            while kirin.alive:
                clock.tick(clockTime)

            # Test Resize windowSize
            #    kirin.life = 10000 # 게임 중 창크기조절 테스트

            # Drop Items
                powerupTimeLeft -= 1
                if powerupTimeLeft <= 0:
                    powerupTimeLeft = powerupTime
                    random.choice(powerupTypes)(screen_size).add(powerups, allsprites)
                
            # Event Handling
                for event in pygame.event.get():
                    if (event.type == pygame.QUIT
                        or event.type == pygame.KEYDOWN
                            and event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    # Resize windowSize
                    elif (event.type == pygame.VIDEORESIZE):
                        screen_size = min(event.w, event.h)
                        screen = pygame.display.set_mode((screen_size, screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
                        ratio = (screen_size / 500)
                        font = pygame.font.Font(None, round(36*ratio))
                        beforeWaveCountFont = pygame.font.Font(None, round(60*ratio))
                        leftCountFont = pygame.font.Font(None, round(60*ratio))
                    # Kirin Moving
                    elif (event.type == pygame.KEYDOWN
                        and event.key in direction.keys()):
                        kirin.horiz += direction[event.key][0] * speed
                        kirin.vert += direction[event.key][1] * speed
                    elif (event.type == pygame.KEYUP
                        and event.key in direction.keys()):
                        kirin.horiz -= direction[event.key][0] * speed
                        kirin.vert -= direction[event.key][1] * speed
                    # Leaf
                    elif (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_SPACE):
                        if doubleleaf :
                            Leaf.position(kirin.rect.topleft)
                            Leaf.position(kirin.rect.topright)
                            leafFired += 2
                        else : 
                            Leaf.position(kirin.rect.midtop)
                            leafFired += 1
                        if soundFX:
                            leaf_sound.play()
                    # Bomb
                    elif (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_b):
                        if bombsHeld > 0:
                            bombsHeld -= 1
                            newBomb = kirin.bomb()
                            newBomb.add(bombs, alldrawings)
                            if soundFX:
                                bomb_sound.play()
                    # Pause Menu
                    elif (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_p):
                        pauseMenu = True
                        cnt=0

                        while pauseMenu:
                            clock.tick(clockTime)

                            screen.blit(background, (0, 0))
                            pause_size = (round(pause.get_width() * ratio), round(pause.get_height() * ratio))
                            screen.blit(pygame.transform.scale(pause, pause_size), (0,0))

                            for event in pygame.event.get():
                                if (event.type == pygame.QUIT
                                    or event.type == pygame.KEYDOWN
                                        and event.key == pygame.K_ESCAPE):
                                    pygame.quit()
                                    sys.exit()
                                # Resize windowSize
                                elif (event.type == pygame.VIDEORESIZE):
                                    screen_size = min(event.w, event.h)
                                    if screen_size <= 300:
                                        screen_size = 300
                                    screen = pygame.display.set_mode((screen_size, screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
                                    ratio = (screen_size / 500)
                                    font = pygame.font.Font(None, round(36*ratio))
                                elif (event.type == pygame.KEYDOWN  # unpause
                                    and event.key == pygame.K_p):
                                    pauseMenu = False
                                elif (event.type == pygame.KEYDOWN
                                    and event.key == pygame.K_RETURN):
                                    if showHiScores:
                                        showHiScores = False
                                    elif showHelp:
                                        cnt+=1
                                        if cnt%3!=0:
                                            showHelp=True
                                        else:
                                            showHelp=False
                                    elif selection == 1:    
                                        pauseMenu = False
                                        kirin.alive = False
                                    elif selection == 2:
                                        showHiScores = True
                                    elif selection == 3:
                                        soundFX = not soundFX
                                        if soundFX:
                                            leaf_sound.play()
                                        Database.setSound(int(soundFX))
                                    elif selection == 4 and pygame.mixer:
                                        music = not music
                                        if music:
                                            pygame.mixer.music.play(loops=-1)
                                        else:
                                            pygame.mixer.music.stop()
                                        Database.setSound(int(music), music=True)
                                    elif selection == 5:
                                        cnt+=1
                                        showHelp=True
                                    elif selection == 6:
                                        pygame.quit()
                                        sys.exit()
                                elif (event.type == pygame.KEYDOWN
                                    and event.key == pygame.K_UP
                                    and selection > 1
                                    and not showHiScores):
                                    selection -= 1
                                elif (event.type == pygame.KEYDOWN
                                    and event.key == pygame.K_DOWN
                                    and selection < len(pauseMenuDict)
                                    and not showHiScores):
                                    selection += 1
                            
                            blankText=font.render('            ',1,BLACK)
                            blankPos=blankText.get_rect(topright=screen.get_rect().center)
                            restartText = font.render('RESTART GAME', 1, BLACK)
                            restartPos = restartText.get_rect(topleft=blankPos.bottomleft)  
                            hiScoreText = font.render('HIGH SCORES', 1, BLACK)
                            hiScorePos = hiScoreText.get_rect(topleft=restartPos.bottomleft)
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
                            pauseMenuDict = {1: restartPos, 2: hiScorePos, 3: fxPos, 
                                    4: musicPos, 5: helpPos, 6: quitPos}
                            selectText = font.render('*', 1, BLACK)
                            selectPos = selectText.get_rect(topright=pauseMenuDict[selection].topleft)

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

                            if showHiScores:
                                menu_size = (round(menu.get_width() * ratio), round(menu.get_height() * ratio))
                                screen.blit(pygame.transform.scale(menu, menu_size), (0,0))                                
                                textOverlays = zip(highScoreTexts, highScorePos)
                            elif showHelp:
                                if cnt%3==1:
                                    screen.blit(background, (0, 0))
                                    menu, menuRect = load_image("help1.png")
                                    menuRect.midtop = screen.get_rect().midtop
                                    screen.blit(menu, menuRect) 
                                    menu_size = (round(menu.get_width() * ratio), round(menu.get_height() * ratio))
                                    screen.blit(pygame.transform.scale(menu, menu_size), (0,0))
                                elif cnt%3==2:
                                    screen.blit(background, (0, 0))
                                    menu, menuRect = load_image("help2.png") 
                                    menuRect.midtop = screen.get_rect().midtop
                                    screen.blit(menu, menuRect) 
                                    menu_size = (round(menu.get_width() * ratio), round(menu.get_height() * ratio))
                                    screen.blit(pygame.transform.scale(menu, menu_size), (0,0))     
                            else:
                                textOverlays = zip([blankText,restartText, hiScoreText, helpText, fxText,
                                                    musicText, quitText, selectText,
                                                    fxOnText if soundFX else fxOffText,
                                                    musicOnText if music else musicOffText],
                                                    [blankPos,restartPos, hiScorePos, helpPos, fxPos,
                                                    musicPos, quitPos, selectPos,
                                                    fxOnPos if soundFX else fxOffPos,
                                                    musicOnPos if music else musicOffPos])
                            for txt, pos in textOverlays:
                                screen.blit(txt, pos)

                            alldrawings.update()
                            pygame.display.flip()
                    

            # Collision Detection
                # Bears
                for bear in Bear.active:
                    for bomb in bombs:
                        if pygame.sprite.collide_circle(
                                bomb, bear) and bear in Bear.active:
                            if bear.pType != 'white' :
                                bear.table()
                                Explosion.position(bear.rect.center)
                                score = kill_bear(bear, score)
                            leafFired += 1
                            if soundFX:
                                bear_explode_sound.play()
                    for leaf in Leaf.active:
                        if pygame.sprite.collide_rect(
                                leaf, bear) and bear in Bear.active:
                            leaf.table()
                            if bear.pType != 'white' :
                                bear.table()
                                Explosion.position(bear.rect.center)
                                score = kill_bear(bear, score)
                            if soundFX:
                                bear_explode_sound.play()
                    if pygame.sprite.collide_rect(bear, kirin):
                        if kirin.shieldUp:
                            bear.table()
                            Explosion.position(bear.rect.center)
                            score = kill_bear(bear, score)
                            leafFired += 1
                            kirin.shieldUp = False
                        elif kirin.life > 1:   # life
                            bear.table()
                            Explosion.position(bear.rect.center)
                            score = kill_bear(bear, score) 
                            kirin.life -= 1
                        else:
                            restart = False
                            kirin.alive = False
                            kirin.remove(allsprites)
                            Explosion.position(kirin.rect.center)
                            if soundFX:
                                kirin_explode_sound.play()

                # PowerUps
                for powerup in powerups:
                    if pygame.sprite.collide_circle(powerup, kirin):
                        if powerup.pType == 'bomb':
                            bombsHeld += 1
                        elif powerup.pType == 'shield':
                            kirin.shieldUp = True
                        elif powerup.pType == 'doubleleaf' :
                            doubleleaf = True 
                        elif powerup.pType == 'life':
                            if kirin.life < 3:
                                kirin.life += 1
                        elif powerup.pType == 'friendkirin' :
                            friendkirin = True
                            MasterSprite.allsprites.add(minikirin) 
                            allsprites.update(screen_size)
                            allsprites.draw(screen)
                        powerup.kill()
                    elif powerup.rect.top > powerup.area.bottom:
                        powerup.kill()

            # Update Bears
                if curTime <= 0 and bearsLeftThisWave > 0:
                    Bear.position()
                    curTime = bearPeriod
                elif curTime > 0:
                    curTime -= 1

            # Update text overlays
                waveText = font.render("Wave: -", 1, BLACK)
                leftCountText = leftCountFont.render(str(leftCount // clockTime), 1, RED)
                scoreText = font.render("Score: " + str(score), 1, BLACK)
                bombText = font.render("Fart Bombs: " + str(bombsHeld), 1, BLACK)
                
                wavePos = waveText.get_rect(topleft=screen.get_rect().topleft)
                leftCountPos = leftCountText.get_rect(midtop=screen.get_rect().midtop)
                scorePos = scoreText.get_rect(topright=screen.get_rect().topright)
                bombPos = bombText.get_rect(bottomleft=screen.get_rect().bottomleft)                

                text = [waveText, leftCountText, scoreText, bombText]
                textposition = [wavePos, leftCountPos, scorePos, bombPos]

            # Update using items(activate)
                # item - doubleleaf 
                if doubleleaf:
                    if betweenDoubleCount > 0:
                        betweenDoubleCount -= 1
                    elif betweenDoubleCount == 0:
                        doubleleaf = False
                        betweenDoubleCount = betweenDoubleTime
                
                # item - friendkirin
                minikirin.rect.bottomright = kirin.rect.bottomleft
                if friendkirin:
                    # friendkirin
                    if friendkirinCount > 0:
                        friendkirinCount -= 1
                    elif friendkirinCount == 0:
                        friendkirin = False
                        minikirin.remove()
                        friendkirinCount = friendkirinTime
                    # friendkirin's leaf
                    if friendkirinLeafCount > 0:
                        friendkirinLeafCount -= 1
                    elif friendkirinLeafCount == 0:
                        friendkirinLeafCount = friendkirinLeafTime
                        Leaf.position(minikirin.rect.midtop)

            # leftCount - Count Down 60 to 0
                if bearsLeftThisWave > 0:
                    if leftCount > 0:
                        leftCount -= 1
                    elif leftCount == 0:
                        restart = False
                        kirin.alive = False
                        kirin.remove(allsprites)
                        Explosion.position(kirin.rect.center)
                        if soundFX:
                            kirin_explode_sound.play()

            # beforeWaveCount - Count Down 3, 2, 1, START!
                if bearsLeftThisWave == 0:
                    if beforeWaveCount >= 1 * clockTime:
                        beforeWaveCount -= 1
                        beforeWaveText = beforeWaveCountFont.render(str(beforeWaveCount // clockTime), 1, BLACK)
                        beforeWavePos = beforeWaveText.get_rect(center=screen.get_rect().center)
                    elif beforeWaveCount >= 0:
                        beforeWaveCount -= 1
                        beforeWaveText = beforeWaveCountFont.render("START!", 1, RED)
                        beforeWavePos = beforeWaveText.get_rect(center=screen.get_rect().center)
                    else:
                        beforeWaveText = beforeWaveCountFont.render("", 1, BLACK)
                        bearsLeftThisWave = Bear.numOffScreen = bearsThisWave
                    text.extend([beforeWaveText])
                    textposition.extend([beforeWavePos])

                textOverlays = zip(text, textposition)

            # moving field
                if bearsLeftThisWave == 0:
                    field1_size = (round(field1.get_width() * ratio), round(field1.get_height() * ratio))
                    screen.blit(pygame.transform.scale(field1, field1_size), (0,0))
                else:
                    field1Rect.y += int(3 * ratio)
                    field2Rect.y += int(3 * ratio)
                    if field1Rect.y >= screen_size:
                        field1Rect.midbottom = field2Rect.midtop
                    if field2Rect.y >= screen_size:
                        field2Rect.midbottom = field1Rect.midtop
                    
                    field_size = (round(field1.get_width() * ratio), round(field1.get_height() * ratio))
                    screen.blit(pygame.transform.scale(field1, field_size), (0,field1Rect.y))
                    screen.blit(pygame.transform.scale(field2, field_size), (0,field2Rect.y))

            # Update and draw all sprites and text                    
                allsprites.update(screen_size)
                allsprites.draw(screen)
                alldrawings.update()
                for txt, pos in textOverlays:
                    screen.blit(txt, pos)

            # Update life
                life1Rect.topleft = wavePos.bottomleft
                life2Rect.topleft = wavePos.bottomleft
                life3Rect.topleft = wavePos.bottomleft

                life_size = (round(life1.get_width() * ratio), round(life1.get_height() * ratio))
                if kirin.life == 3:
                    screen.blit(pygame.transform.scale(life3, life_size), life3Rect)
                elif kirin.life == 2:
                    screen.blit(pygame.transform.scale(life2, life_size), life2Rect)
                elif kirin.life == 1:
                    screen.blit(pygame.transform.scale(life1, life_size), life1Rect)

                pygame.display.flip()


        # Data for Highscore
            accuracy = round(score / leafFired, 4) if leafFired > 0 else 0.0
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
            # Resize windowSize
                elif (event.type == pygame.VIDEORESIZE):
                    screen_size = min(event.w, event.h)
                    if screen_size <= 300:
                        screen_size = 300
                    screen = pygame.display.set_mode((screen_size, screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
                    ratio = (screen_size / 500)
                    font = pygame.font.Font(None, round(36*ratio))
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
                    if Database().name_not_exists(name,mode=TIME):
                        Database().setTimeScore(hiScores,name, score, accuracy)
                        return True
                    else:
                        print("중복된 이름 존재함")
                      

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

        # moving field           
            field1Rect.y += int(3 * ratio)
            field2Rect.y += int(3 * ratio)
            if field1Rect.y >= screen_size:
                field1Rect.midbottom = field2Rect.midtop
            if field2Rect.y >= screen_size:
                field2Rect.midbottom = field1Rect.midtop
            
            field_size = (round(field1.get_width() * ratio), round(field1.get_height() * ratio))
            screen.blit(pygame.transform.scale(field1, field_size), (0,field1Rect.y))
            screen.blit(pygame.transform.scale(field2, field_size), (0,field2Rect.y))

        # Update and draw all sprites
            allsprites.update(screen_size)
            allsprites.draw(screen)
            alldrawings.update()
            for txt, pos in textOverlay:
                screen.blit(txt, pos)

            pygame.display.flip()

        # code is unreachable...?
        #return screen_size  # for delivering screen_size after game