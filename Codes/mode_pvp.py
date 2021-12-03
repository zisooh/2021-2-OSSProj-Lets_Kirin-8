import pygame
import random
import sys

from sprites import (MasterSprite, Kirin2, Kirin3, Bear, Leaf, BombPowerup,
                     ShieldPowerup, DoubleleafPowerup, Explosion, Siney, Spikey, Fasty,
                     Roundy, Crawly)
from database import Database
from load import load_image, load_sound, load_music
from menu import *

if not pygame.mixer: 
    print('Warning, sound disabled')
if not pygame.font:
    print('Warning, fonts disabled')

BACK = 0

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

direction = {None: (0, 0), pygame.K_UP: (0, -2), pygame.K_DOWN: (0, 2),
             pygame.K_LEFT: (-2, 0), pygame.K_RIGHT: (2, 0)}

direction2 = {None: (0, 0), pygame.K_w: (0, -2), pygame.K_s: (0, 2),
             pygame.K_a: (-2, 0), pygame.K_d: (2, 0)}


# class Keyboard(object):
#     keys = {pygame.K_a: 'A', pygame.K_b: 'B', pygame.K_c: 'C', pygame.K_d: 'D',
#             pygame.K_e: 'E', pygame.K_f: 'F', pygame.K_g: 'G', pygame.K_h: 'H',
#             pygame.K_i: 'I', pygame.K_j: 'J', pygame.K_k: 'K', pygame.K_l: 'L',
#             pygame.K_m: 'M', pygame.K_n: 'N', pygame.K_o: 'O', pygame.K_p: 'P',
#             pygame.K_q: 'Q', pygame.K_r: 'R', pygame.K_s: 'S', pygame.K_t: 'T',
#             pygame.K_u: 'U', pygame.K_v: 'V', pygame.K_w: 'W', pygame.K_x: 'X',
#             pygame.K_y: 'Y', pygame.K_z: 'Z'}


class Pvp() :
    def playGame(): 
        # Initialize everything
        pygame.mixer.pre_init(11025, -16, 2, 512)
        pygame.init()
        screen_width = 500   # 스크린가로
        screen_height = 500  # 스크린세로
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Let's Kirin!")
        pygame.mouse.set_visible(0)    

        def kill_bear(bear, bearsLeftThisWave, score) :
            bearsLeftThisWave -= 1
            if bear.pType == 'green':
                score += 1
            elif bear.pType == 'orange':
                score += 2
            elif bear.pType == 'red':
                score += 4
            elif bear.pType == 'yellow':
                score += 8
            return bearsLeftThisWave, score
        
        # def background_update(screen, background, backgroundLoc) :
        #     screen.blit(
        #         background, (0, 0), area=pygame.Rect(
        #             0, backgroundLoc, 500, 500))
        #     backgroundLoc -= speed
        #     if backgroundLoc - speed <= speed:
        #         backgroundLoc = 1500
        #     return screen, background, backgroundLoc

        # # 인게임에서 배경색으로 플레이어 영역 구분
        # def background_update_half(screen, background, backgroundLoc) :
        #     screen.blit(
        #         background, (0, 0), area=pygame.Rect(
        #             0, backgroundLoc, 500, 500))
        #     screen.fill((80, 20, 30, 125),(0, 0, screen.get_width()//2, screen.get_height()), special_flags = 1) # special_flags = 3 : 별 색깔만 바뀜
        #     backgroundLoc -= speed
        #     if backgroundLoc - speed <= speed:
        #         backgroundLoc = 1500
        #     return screen, background, backgroundLoc

        # def background_update_half_two(screen, background, backgroundLoc) :
        #     screen.blit(
        #         background, (0, 0), area=pygame.Rect(
        #             0, backgroundLoc, 500, 500))
        #     screen.fill((80, 20, 30, 125),(screen.get_width()//2, 0, screen.get_width()//size.x_background_ratio, screen.get_height()), special_flags = 1)
        #     backgroundLoc -= speed
        #     if backgroundLoc - speed <= speed:
        #         backgroundLoc = 1500
        #     return screen, background, backgroundLoc

        # def ingame_text_update() :
        #     return [font.render("Wave: " + str(wave), 1, WHITE),
        #             font.render("bears Left: " + str(bearsLeftThisWave), 1, WHITE),
        #             font.render("Score: " + str(score), 1, WHITE),
        #             font.render("Score: " + str(score2), 1, WHITE),
        #             font.render("Bombs: " + str(bombsHeld), 1, WHITE),
        #             font.render("Bombs: " + str(bombsHeld2), 1, WHITE),
        #             # font.render("Life: ", 1, WHITE)
        #             # font.render("Life: ", 1, WHITE)
        #             font.render('PLAYER 1 WIN!', 1, WHITE),
        #             font.render('PLAYER 2 WIN!', 1, WHITE),
        #             font.render('DRAW!', 1, WHITE)]

    # Create the background which will scroll and loop over a set of different
        background = pygame.Surface((500, 2000))
        background = background.convert()
        background.fill((0, 0, 0))
        # backgroundLoc = 1500

    # Display the background
        screen.blit(background, (0, 0))
        pygame.display.flip()
    
    # Prepare background image
        # Game field
        field1, field1Rect = load_image("field_pvp.png")
        field2, field2Rect = load_image("field_pvp.png")
        field1Rect.midtop = screen.get_rect().midtop
        field2Rect.midbottom = field1Rect.midtop
        pygame.draw.rect(screen, BLACK, [250,0,3,500])

        # Menu - pause 메뉴 Highscore & help
        menu, menuRect = load_image("menu.png")
        menuRect.midtop = screen.get_rect().midtop

        # pause
        pause,pauseRect = load_image('pause.png')
        pauseRect.midtop = screen.get_rect().midtop
        pauseMenu = False 

        # # Main_menu
        # main_menu, main_menuRect = load_image("main_menu.png")
        # main_menuRect.midtop = screen.get_rect().midtop

        # # Menu
        # img_menu, img_menuRect = load_image("menu.png")
        # img_menuRect.midtop = screen.get_rect().midtop


    # Prepare game objects
        # life
        # life1, life1Rect = load_image('heart1.png')
        # life2, life2Rect = load_image('heart2.png')
        # life3, life3Rect = load_image('heart3.png')

        # Sounds
        leaf_sound = load_sound('leaf.ogg')
        bomb_sound = load_sound('bomb.ogg')
        bear_explode_sound = load_sound('bear_explode.ogg')
        kirin_explode_sound = load_sound('kirin_explode.ogg')
        load_music('music_loop.ogg')

        speed = 1.5
        MasterSprite.speed = speed
        bearPeriod = 60 / speed
        clockTime = 60  # maximum FPS
        clock = pygame.time.Clock()
        kirin = Kirin2()
        kirin2 = Kirin3() 
        
        initialbearTypes = (Siney, Spikey)
        powerupTypes = (BombPowerup, ShieldPowerup, DoubleleafPowerup)

        bombs = pygame.sprite.Group()
        bombs2 = pygame.sprite.Group()
        powerups = pygame.sprite.Group()

        # font
        font = pygame.font.Font(None, 36)

        # # Sprite groups
        # alldrawings = pygame.sprite.Group()
        # allsprites = pygame.sprite.RenderPlain((kirin,kirin2))
        # MasterSprite.allsprites = allsprites
        # bear.pool = pygame.sprite.Group(
        #     [bear() for bear in initialbearTypes for _ in range(5)])
        # bear.active = pygame.sprite.Group()
        # Leaf.pool = pygame.sprite.Group([Leaf() for _ in range(10)]) 
        # Leaf.active = pygame.sprite.Group()
        # Explosion.pool = pygame.sprite.Group([Explosion() for _ in range(10)])
        # Explosion.active = pygame.sprite.Group()

        # bearPeriod = clockTime // 2
        # curTime = 0
        # bearsThisWave, bearsLeftThisWave, bear.numOffScreen = 10, 10, 10
        # wave = 1

        # doubleleaf = False
        # doubleleaf2 = False
        # bombsHeld = 3
        # bombsHeld2 = 3
        # score = 0
        # score2 = 0

        # leafsFired = 0
        # powerupTime = 10 * clockTime
        # powerupTimeLeft = powerupTime
        # betweenWaveTime = 3 * clockTime
        # betweenWaveCount = betweenWaveTime
        # betweenDoubleTime = 8 * clockTime
        # betweenDoubleCount = betweenDoubleTime
        # betweenDoubleCount2 = betweenDoubleTime

        # # # ?
        # # inMenu = True
        half_tf = True

        # 데베 함수 메뉴 구현
        hiScores = Database().getScores()
        soundFX = Database().getSound()
        music = Database().getSound(music=True)
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

    # Temp - only load for Rect
        title, titleRect = load_image('title.png')
        titleRect.midtop = screen.get_rect().inflate(0, -200).midtop
    
    # pause menu text
        restartText = font.render('RESTART GAME', 1, BLACK)
        restartPos = restartText.get_rect(midtop=titleRect.inflate(0, 100).midbottom)  
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

    #########################
    #    Start Pvp Loop    #
    #########################
        restart = True
        while restart == True:

        # Prepare game objects : reset
            # Reset Sprite groups
            alldrawings = pygame.sprite.Group()
            allsprites = pygame.sprite.RenderPlain((kirin,kirin2))
            MasterSprite.allsprites = allsprites
            Bear.pool = pygame.sprite.Group(
                [bear() for bear in initialbearTypes for _ in range(5)])
            Bear.active = pygame.sprite.Group()
            Leaf.pool = pygame.sprite.Group([Leaf() for _ in range(10)]) 
            Leaf.active = pygame.sprite.Group()
            Explosion.pool = pygame.sprite.Group([Explosion() for _ in range(10)])
            Explosion.active = pygame.sprite.Group()

            # Reset game contents
            bearsThisWave, bearsLeftThisWave, Bear.numOffScreen = 10, 10, 10
            doubleleaf = False
            bombsHeld = 3
            score = 0
            doubleleaf2 = False
            bombsHeld2 = 3
            score2 = 0
            leafFired = 0
            wave = 1

            bearPeriod = clockTime // 2
            curTime = 0
            powerupTime = 8 * clockTime
            powerupTimeLeft = powerupTime
            betweenWaveTime = 3 * clockTime
            betweenWaveCount = betweenWaveTime
            betweenDoubleTime = 8 * clockTime
            betweenDoubleCount = betweenDoubleTime
            betweenDoubleCount2 = betweenDoubleTime
            # friendkirinTime = 8 * clockTime
            # friendkirinCount = friendkirinTime
            # friendkirinleafTime = 0.2 * clockTime
            # friendkirinleafCount = friendkirinleafTime
            
            kirin.alive = True
            kirin.life = 3
            kirin.initializeKeys()
            kirin2.alive = True
            kirin2.life = 3
            kirin2.initializeKeys()

            # half_tf = True

            # 본게임시작
            while kirin.alive and kirin2.alive :
                clock.tick(clockTime)

                if bearsLeftThisWave >= 0:
                    powerupTimeLeft -= 1
                if powerupTimeLeft <= 0:
                    powerupTimeLeft = powerupTime
                    random.choice(powerupTypes)().add(powerups, allsprites)

            # Event Handling
                for event in pygame.event.get():
                    if (event.type == pygame.QUIT
                        or event.type == pygame.KEYDOWN
                            and event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    # kirin1 Moving
                    elif (event.type == pygame.KEYDOWN
                        and event.key in direction.keys()):
                        kirin.horiz += direction[event.key][0] * speed
                        kirin.vert += direction[event.key][1] * speed
                    elif (event.type == pygame.KEYUP
                        and event.key in direction.keys()):
                        kirin.horiz -= direction[event.key][0] * speed
                        kirin.vert -= direction[event.key][1] * speed
                    # leaf1
                    elif (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_m):
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
                    # kirin2 Moving
                    elif (event.type == pygame.KEYDOWN
                        and event.key in direction2.keys()):
                        kirin2.horiz += direction2[event.key][0] * speed
                        kirin2.vert += direction2[event.key][1] * speed
                    elif (event.type == pygame.KEYUP
                        and event.key in direction2.keys()):
                        kirin2.horiz -= direction2[event.key][0] * speed
                        kirin2.vert -= direction2[event.key][1] * speed
                    # leaf2
                    elif (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_SPACE):
                        if doubleleaf2 :
                            Leaf.position(kirin2.rect.topleft)
                            Leaf.position(kirin2.rect.topright)
                            leafFired += 2
                        else : 
                            Leaf.position(kirin2.rect.midtop)
                            leafFired += 1
                        if soundFX:
                            leaf_sound.play()
                    # Bomb
                    elif (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_b):
                        if bombsHeld2 > 0:
                            bombsHeld2 -= 1
                            newBomb = kirin2.bomb()
                            newBomb.add(bombs2, alldrawings)
                            if soundFX:
                                bomb_sound.play()
                    # Pause
                    elif (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_p):
                        pauseMenu = True
                        pauseMenuDict = {1: restartPos, 2: hiScorePos, 3: fxPos, 
                                    4: musicPos, 5: helpPos, 6: quitPos}
                        
                        while pauseMenu:
                            clock.tick(clockTime)

                            # screen.blit(
                            #     background, (0, 0), area=pygame.Rect(
                            #         0, backgroundLoc, 500, 500))    ## 이 3줄이 없으면 text업데이트가 안됨. why

                            screen.blit(background, (0, 0))
                            screen.blit(pause, pauseRect)

                            for event in pygame.event.get():
                                if (event.type == pygame.QUIT
                                    or event.type == pygame.KEYDOWN
                                        and event.key == pygame.K_ESCAPE):
                                    pygame.quit()
                                    sys.exit()
                                elif (event.type == pygame.KEYDOWN
                                    and event.key == pygame.K_p): 
                                    pauseMenu = False
                                # Pause Menu
                                elif (event.type == pygame.KEYDOWN
                                    and event.key == pygame.K_RETURN):
                                    if showHiScores:
                                        showHiScores = False
                                    elif showHelp:
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
                                        showHelp=True
                                    elif selection == 6:
                                        pygame.quit()
                                        sys.exit()
                                elif (event.type == pygame.KEYDOWN
                                    and event.key == pygame.K_w
                                    and selection > 1
                                    and not showHiScores):
                                    selection -= 1
                                elif (event.type == pygame.KEYDOWN
                                    and event.key == pygame.K_s
                                    and selection < len(pauseMenuDict)
                                    and not showHiScores):
                                    selection += 1
                                

                            # selectPos = selectText.get_rect(topright=menuDict[selection].topleft)
                            selectPos = selectText.get_rect(topright=pauseMenuDict[selection].topleft)

                            if showHiScores:
                                screen.blit(menu, menuRect)
                                textOverlays = zip(highScoreTexts, highScorePos)
                            elif showHelp:
                                screen.blit(menu, menuRect) 
                            else:
                                textOverlays = zip([restartText, hiScoreText, helpText, fxText,
                                                    musicText, quitText, selectText,
                                                    fxOnText if soundFX else fxOffText,
                                                    musicOnText if music else musicOffText],
                                                    [restartPos, hiScorePos, helpPos, fxPos,
                                                    musicPos, quitPos, selectPos,
                                                    fxOnPos if soundFX else fxOffPos,
                                                    musicOnPos if music else musicOffPos])
                                # screen.blit(pause, pauseRect)
                            for txt, pos in textOverlays:
                                screen.blit(txt, pos)

                            alldrawings.update()
                            pygame.display.flip()
                    

            # Collision Detection
                # bears
                for bear in Bear.active:
                    for bomb in bombs:
                        if pygame.sprite.collide_circle(
                                bomb, bear) and bear in Bear.active:
                            if bear.pType != 'white' :
                                bear.table()
                                Explosion.position(bear.rect.center)
                                bearsLeftThisWave, score = kill_bear(bear, bearsLeftThisWave, score)
                            leafFired += 1
                            if soundFX:
                                bear_explode_sound.play()
                    for bomb in bombs2:
                        if pygame.sprite.collide_circle(
                                bomb, bear) and bear in Bear.active:
                            if bear.pType != 'white' :
                                bear.table()
                                Explosion.position(bear.rect.center)
                                bearsLeftThisWave, score2 = kill_bear(bear, bearsLeftThisWave, score2)
                            if soundFX:
                                bear_explode_sound.play()
                    for leaf in Leaf.active:
                        if pygame.sprite.collide_rect(
                                leaf, bear) and bear in bear.active:
                            leaf.table()
                            if bear.pType != 'white' :
                                bear.table()
                                Explosion.position(bear.rect.center)
                                if bear.rect.center[0] < 500 :
                                    bearsLeftThisWave, score = kill_bear(bear, bearsLeftThisWave, score)
                                else :
                                    bearsLeftThisWave, score2 = kill_bear(bear, bearsLeftThisWave, score2)
                            if soundFX:
                                bear_explode_sound.play()

                    if pygame.sprite.collide_rect(bear, kirin):
                        if kirin.shieldUp:
                            bear.table()
                            Explosion.position(bear.rect.center)
                            bearsLeftThisWave, score = kill_bear(bear, bearsLeftThisWave, score)
                            leafFired += 1
                            kirin.shieldUp = False
                        elif kirin.life > 1:   # life
                            bear.table()
                            Explosion.position(bear.rect.center)
                            bearsLeftThisWave-= 1
                            score += 1
                            kirin.life -= 1
                        else:
                            restart = False
                            kirin.alive = False
                            kirin.remove(allsprites)
                            Explosion.position(kirin.rect.center)
                            if soundFX:
                                kirin_explode_sound.play()
                    if pygame.sprite.collide_rect(bear, kirin2):
                        if kirin2.shieldUp:
                            bear.table()
                            Explosion.position(bear.rect.center)
                            bearsLeftThisWave, score2 = kill_bear(bear, bearsLeftThisWave, score2)
                            leafFired += 1
                            kirin2.shieldUp = False
                        elif kirin2.life > 1:   # life
                            bear.table()
                            Explosion.position(bear.rect.center)
                            bearsLeftThisWave -= 1
                            score2 += 1
                            kirin2.life -= 1
                        else:
                            restart = False
                            kirin2.alive = False
                            kirin2.remove(allsprites)
                            Explosion.position(kirin2.rect.center)
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
                        # elif powerup.pType == 'friendkirin' :
                        #     friendkirin = True 
                        #     minikirin.alive = True   
                        powerup.kill()
                    elif powerup.rect.top > powerup.area.bottom:
                        powerup.kill()
                for powerup in powerups:
                    if pygame.sprite.collide_circle(powerup, kirin2):
                        if powerup.pType == 'bomb':
                            bombsHeld2 += 1
                        elif powerup.pType == 'shield':
                            kirin2.shieldUp = True
                        elif powerup.pType == 'doubleleaf' :
                            doubleleaf2 = True
                        # elif powerup.pType == 'friendkirin' :
                        #     friendkirin = True 
                        #     minikirin.alive = True   
                        powerup.kill()
                    elif powerup.rect.top > powerup.area.bottom:
                        powerup.kill()

            # Update bears
                if curTime <= 0 and bearsLeftThisWave> 0:
                    Bear.position()
                    curTime = bearPeriod
                elif curTime > 0:
                    curTime -= 1

            # Update text overlays
                # if half_tf :
                #     waveText, leftText, scoreText, scoreText2, bombText, bombText2, kirin1winText, kirin2winText, drawText = ingame_text_update()
                # else :
                #     waveText, leftText, scoreText2, scoreText, bombText2, bombText, kirin1winText, kirin2winText, drawText = ingame_text_update()
                # font.render("Wave: " + str(wave), 1, WHITE),
        #             font.render("bears Left: " + str(bearsLeftThisWave), 1, WHITE),
        #             font.render("Score: " + str(score), 1, WHITE),
        #             font.render("Score: " + str(score2), 1, WHITE),
        #             font.render("Bombs: " + str(bombsHeld), 1, WHITE),
        #             font.render("Bombs: " + str(bombsHeld2), 1, WHITE),
        #             # font.render("Life: ", 1, WHITE)
        #             # font.render("Life: ", 1, WHITE)
        #             font.render('PLAYER 1 WIN!', 1, WHITE),
        #             font.render('PLAYER 2 WIN!', 1, WHITE),
        #             font.render('DRAW!', 1, WHITE)
                
                if half_tf :
                    waveText = font.render("Wave: " + str(wave), 1, WHITE)
                    leftText = font.render("bears: " + str(bearsLeftThisWave), 1, WHITE)
                    scoreText = font.render("Score: " + str(score), 1, WHITE)
                    scoreText2 = font.render("Score: " + str(score2), 1, WHITE)
                    bombText = font.render("Bombs: " + str(bombsHeld), 1, WHITE)
                    bombText2 = font.render("Bombs: " + str(bombsHeld2), 1, WHITE)
                    # lifeText = font.render("Life: ", 1, WHITE)
                    # lifeText2 = font.render("Life: ", 1, WHITE)
                    kirin1winText = font.render('PLAYER 1 WIN!', 1, WHITE)
                    kirin2winText = font.render('PLAYER 2 WIN!', 1, WHITE)
                    drawText = font.render('DRAW!', 1, WHITE)
                else :
                    waveText = font.render("Wave: " + str(wave), 1, WHITE)
                    leftText = font.render("bears Left: " + str(bearsLeftThisWave), 1, WHITE)
                    scoreText2 = font.render("Score: " + str(score2), 1, WHITE)
                    bombText2 = font.render("Bombs: " + str(bombsHeld2), 1, WHITE)
                    # lifeText2 = font.render("Life: ", 1, WHITE)
                    kirin2winText = font.render('PLAYER 2 WIN!', 1, WHITE)
                    drawText = font.render('DRAW!', 1, WHITE)

        
                wavePos = waveText.get_rect(topright=screen.get_rect().midtop)
                leftPos = leftText.get_rect(topleft=screen.get_rect().midtop)
                scorePos = scoreText.get_rect(topleft=screen.get_rect().bottomleft)
                # bombPos = bombText.get_rect(bottomleft=screen.get_rect().bottomleft)
                # lifePos = lifeText.get_rect(topleft=wavePos.bottomleft)
                scorePos2 = scoreText2.get_rect(topright=screen.get_rect().midbottom)
                # bombPos2 = bombText2.get_rect(bottomleft=screen.get_rect().midbottom)
                # lifePos2 = lifeText2.get_rect(topleft=wavePos.midbottom)
                kirin1winPos = kirin1winText.get_rect(center=screen.get_rect().center)
                kirin2winPos = kirin2winText.get_rect(center=screen.get_rect().center)
                drawPos = drawText.get_rect(center=screen.get_rect().center)

                text = [waveText, leftText, scoreText, scoreText2, bombText, bombText2] # lifeText, lifeText2]
                # textposition = [wavePos, leftPos, scorePos, bombPos, lifePos, scorePos2, bombPos2, lifePos2]
                textposition = [wavePos, leftPos, scorePos, scorePos2]

                if doubleleaf:
                    if betweenDoubleCount > 0:
                        betweenDoubleCount -= 1
                    elif betweenDoubleCount == 0:
                        doubleleaf = False
                        betweenDoubleCount = betweenDoubleTime
                
                if doubleleaf2:
                    if betweenDoubleCount2 > 0:
                        betweenDoubleCount2 -= 1
                    elif betweenDoubleCount2 == 0:
                        doubleleaf2 = False
                        betweenDoubleCount = betweenDoubleTime
                
                # if friendkirin:
                #     if betweenDoubleCount > 0:
                #         betweenDoubleCount -= 1
                #     elif betweenDoubleCount == 0:
                #         friendkirin = False
                #         betweenDoubleCount = betweenDoubleTime

            # Detertmine when to move to next wave
                if bearsLeftThisWave <= 0:
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
                            kirin.initializeKeys()
                            kirin2.initializeKeys()
                            bearsThisWave = 10
                            bearsLeftThisWave = bear.numOffScreen = bearsThisWave
                        else:
                            bearsThisWave *= 2
                            bearsLeftThisWave = bear.numOffScreen = bearsThisWave
                        if wave == 1:
                            bear.pool.add([Fasty() for _ in range(5)])
                        if wave == 2:
                            bear.pool.add([Roundy() for _ in range(5)])
                        if wave == 3:
                            bear.pool.add([Crawly() for _ in range(5)])
                        wave += 1
                        betweenWaveCount = betweenWaveTime

                textOverlays = zip(text, textposition)

            # Update and draw all sprites and text
                # screen.blit(
                #     background, (0, 0), area=pygame.Rect(
                #         0, backgroundLoc, 500, 500))
                # backgroundLoc -= speed
                # if backgroundLoc - speed <= speed:
                #     backgroundLoc = 1500

                # if half_tf:
                #     screen, background, backgroundLoc = background_update_half(screen, background, backgroundLoc)
                # else:
                #     screen, background, backgroundLoc = background_update_half_two(screen, background, backgroundLoc)
            # moving field
                field1Rect.y += 2
                field2Rect.y += 2
                if field1Rect.y >= screen_height:
                    field1Rect.midbottom = field2Rect.midtop
                if field2Rect.y >= screen_height:
                    field2Rect.midbottom = field1Rect.midtop
                screen.blit(field1, field1Rect)
                screen.blit(field2, field2Rect)
                pygame.draw.rect(screen, BLACK, [250,0,3,500])

                allsprites.update()
                allsprites.draw(screen)
                alldrawings.update()

                for txt, pos in textOverlays:
                    screen.blit(txt, pos)

            # # Update life
            #     life1Rect.topleft = lifePos.topright
            #     life2Rect.topleft = life1Rect.topright
            #     life3Rect.topleft = life2Rect.topright

            #     if kirin.life >= 3:
            #         screen.blit(life3, life3Rect)
            #     if kirin.life >= 2:
            #         screen.blit(life2, life2Rect)
            #     if kirin.life >= 1:
            #         screen.blit(life1, life1Rect)
                
            #     if kirin2.life >= 3:
            #         screen.blit(life3, life3Rect)
            #     if kirin2.life >= 2:
            #         screen.blit(life2, life2Rect)
            #     if kirin2.life >= 1:
            #         screen.blit(life1, life1Rect)

                pygame.display.flip()


            # accuracy = round(score / leafsFired, 4) if leafsFired > 0 else 0.0
            # isHiScore = len(hiScores) < Database.numScores or score > hiScores[-1][1]
            # name = ''
            # nameBuffer = []


    #########################
    #    After Game Loop    #
    #########################

        while True:
            clock.tick(clockTime)

            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()
                # elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN :
                #     return scr_size, level_size, id, language

        # # Event Handling
        #     for event in pygame.event.get():
        #         if (event.type == pygame.QUIT
        #             or not isHiScore
        #             and event.type == pygame.KEYDOWN
        #                 and event.key == pygame.K_ESCAPE):
        #             return False
        #         elif (event.type == pygame.KEYDOWN
        #               and event.key == pygame.K_RETURN
        #               and not isHiScore):
        #             return True
        #         elif (event.type == pygame.KEYDOWN
        #               and event.key in Keyboard.keys.keys()
        #               and len(nameBuffer) < 8):
        #             nameBuffer.append(Keyboard.keys[event.key])
        #             name = ''.join(nameBuffer)
        #         elif (event.type == pygame.KEYDOWN
        #               and event.key == pygame.K_BACKSPACE
        #               and len(nameBuffer) > 0):
        #             nameBuffer.pop()
        #             name = ''.join(nameBuffer)
        #         elif (event.type == pygame.KEYDOWN
        #               and event.key == pygame.K_RETURN
        #               and len(name) > 0):
        #             Database().setScore(hiScores,name, score, accuracy)
        #             return True

        #     if isHiScore:
        #         hiScoreText = font.render('HIGH SCORE!', 1, RED)
        #         hiScorePos = hiScoreText.get_rect(
        #             midbottom=screen.get_rect().center)
        #         scoreText = font.render(str(score), 1, BLACK)
        #         scorePos = scoreText.get_rect(midtop=hiScorePos.midbottom)
        #         enterNameText = font.render('ENTER YOUR NAME:', 1, RED)
        #         enterNamePos = enterNameText.get_rect(midtop=scorePos.midbottom)
        #         nameText = font.render(name, 1, BLACK)
        #         namePos = nameText.get_rect(midtop=enterNamePos.midbottom)
        #         textOverlay = zip([hiScoreText, scoreText,
        #                            enterNameText, nameText],
        #                           [hiScorePos, scorePos,
        #                            enterNamePos, namePos])
        #     else:
        #         gameOverText = font.render('GAME OVER', 1, BLACK)
        #         gameOverPos = gameOverText.get_rect(
        #             center=screen.get_rect().center)
        #         scoreText = font.render('SCORE: {}'.format(score), 1, BLACK)
        #         scorePos = scoreText.get_rect(midtop=gameOverPos.midbottom)
        #         textOverlay = zip([gameOverText, scoreText],
        #                           [gameOverPos, scorePos])

        # Update and draw all sprites
            # kirin1winPos = kirin1winText.get_rect(center=screen.get_rect().center)
            # kirin2winPos = kirin2winText.get_rect(center=screen.get_rect().center)
            # drawPos = drawText.get_rect(center=screen.get_rect().center)

            # screen.blit(
            #     background, (0, 0), area=pygame.Rect(
            #         0, backgroundLoc, 500, 500))
            # backgroundLoc -= speed
            # if backgroundLoc - speed <= 0:
            #     backgroundLoc = 1500
            # screen, background, backgroundLoc = background_update(screen, background, backgroundLoc)

            # moving field         
            field1Rect.y += 2
            field2Rect.y += 2
            if field1Rect.y >= screen_height:
                field1Rect.midbottom = field2Rect.midtop
            if field2Rect.y >= screen_height:
                field2Rect.midbottom = field1Rect.midtop

            screen.blit(field1, field1Rect)
            screen.blit(field2, field2Rect)
            pygame.draw.rect(screen, BLACK, [250,0,3,500])

            allsprites.update()
            allsprites.draw(screen)
            alldrawings.update()

            if kirin.alive and not kirin2.alive :
                screen.blit(kirin1winText, kirin1winPos)
            elif kirin2.alive and not kirin.alive :
                screen.blit(kirin2winText, kirin2winPos)
            elif not kirin.alive and not kirin2.alive :
                screen.blit(drawText, drawPos)

            elif kirin.alive and kirin2.alive :
                if score > score2 :
                    screen.blit(kirin1winText, kirin1winPos)
                elif score < score2 :
                    screen.blit(kirin2winText, kirin2winPos)
                elif score == score2 :
                    screen.blit(drawText, drawPos)

            # for txt, pos in textOverlay:
            #     screen.blit(txt, pos)
            pygame.display.flip()


if __name__ == '__main__':
    while(main()):
        pass