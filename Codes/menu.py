import pygame
import sys
from pygame.locals import *
from load import load_image, load_sound, load_music
from database import Database

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

BACK=0

leaf_sound = load_sound('leaf.ogg')
bomb_sound = load_sound('bomb.ogg')
bear_explode_sound = load_sound('bear_explode.ogg')
kirin_explode_sound = load_sound('kirin_explode.ogg')
load_music('menu_music_loop.ogg')


class Keyboard(object):
    keys = {pygame.K_a: 'A', pygame.K_b: 'B', pygame.K_c: 'C', pygame.K_d: 'D',
            pygame.K_e: 'E', pygame.K_f: 'F', pygame.K_g: 'G', pygame.K_h: 'H',
            pygame.K_i: 'I', pygame.K_j: 'J', pygame.K_k: 'K', pygame.K_l: 'L',
            pygame.K_m: 'M', pygame.K_n: 'N', pygame.K_o: 'O', pygame.K_p: 'P',
            pygame.K_q: 'Q', pygame.K_r: 'R', pygame.K_s: 'S', pygame.K_t: 'T',
            pygame.K_u: 'U', pygame.K_v: 'V', pygame.K_w: 'W', pygame.K_x: 'X',
            pygame.K_y: 'Y', pygame.K_z: 'Z'}

class Menu:
    def __init__(self, screen_size):   
        self.speed = 1.5
        self.clockTime = 60  # maximum FPS
        self.clock = pygame.time.Clock()
        self.screen_size = screen_size
        self.ratio = (self.screen_size / 500)
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.font = pygame.font.Font(None, round(36*self.ratio))
        
        # For hiscore setting 
        self.hiScores=Database().getScores()
        self.timeHiScores=Database().getTimeScores()
        self.highScoreTexts = [self.font.render("NAME", 1, RED),
                        self.font.render("SCORE", 1, RED),
                        self.font.render("ACCURACY", 1, RED)]
        self.highScorePos = [self.highScoreTexts[0].get_rect(
                        topleft=self.screen.get_rect().inflate(-100, -100).topleft),
                        self.highScoreTexts[1].get_rect(
                        midtop=self.screen.get_rect().inflate(-100, -100).midtop),
                        self.highScoreTexts[2].get_rect(
                        topright=self.screen.get_rect().inflate(-100, -100).topright)]
        self.timeHighScoreTexts= [self.font.render("NAME", 1, RED),
                        self.font.render("SCORE", 1, RED),
                        self.font.render("ACCURACY", 1, RED)]
        self.timeHighScorePos = [self.timeHighScoreTexts[0].get_rect(
                        topleft=self.screen.get_rect().inflate(-100, -100).topleft),
                        self.timeHighScoreTexts[1].get_rect(
                        midtop=self.screen.get_rect().inflate(-100, -100).midtop),
                        self.timeHighScoreTexts[2].get_rect(
                        topright=self.screen.get_rect().inflate(-100, -100).topright)]
        for hs in self.hiScores:
            self.highScoreTexts.extend([self.font.render(str(hs[x]), 1, BLACK)
                                for x in range(3)])
            self.highScorePos.extend([self.highScoreTexts[x].get_rect(
                topleft=self.highScorePos[x].bottomleft) for x in range(-3, 0)])
        for hs in self.timeHiScores:
            self.timeHighScoreTexts.extend([self.font.render(str(hs[x]), 1, BLACK)
                                for x in range(3)])
            self.timeHighScorePos.extend([self.timeHighScoreTexts[x].get_rect(
                topleft=self.timeHighScorePos[x].bottomleft) for x in range(-3, 0)])
        
        # For init_page setting
        self.blankText=self.font.render('       ',1,BLACK)
        self.blankPos=self.blankText.get_rect(topright=self.screen.get_rect().center)
        self.loginText = self.font.render('LOG IN', 1, BLACK)
        self.loginPos = self.loginText.get_rect(topleft=self.blankPos.bottomleft)
        self.signText=self.font.render('SIGN UP',1,BLACK)
        self.signPos=self.signText.get_rect(topleft=self.loginPos.bottomleft)
        self.quitText=self.font.render('QUIT',1,BLACK)
        self.quitPos=self.quitText.get_rect(topleft=self.signPos.bottomleft)
        
        # For login_page setting
        self.id=''
        self.idBuffer = []
        self.pwd=''
        self.pwdBuffer= []
        self.enterIdText=0
        self.enterIdPos=0
        self.idText =0
        self.idPos = 0
        self.enterPwdText=0
        self.enterPwdPos=0
        self.pwdText = 0
        self.pwdPos =0
        self.secretPwd=0

        # For inMenu_page setting
        self.startText = self.font.render('SELECT MODE', 1, BLACK)
        self.startPos = self.startText.get_rect(topleft=self.blankPos.bottomleft)
        self.hiScoreText = self.font.render('HIGH SCORE', 1, BLACK)
        self.hiScorePos = self.hiScoreText.get_rect(topleft=self.startPos.bottomleft)
        self.fxText = self.font.render('SOUND FX ', 1, BLACK)
        self.fxPos = self.fxText.get_rect(topleft=self.hiScorePos.bottomleft)
        self.fxOnText = self.font.render('ON', 1, RED)
        self.fxOffText = self.font.render('OFF', 1, RED)
        self.fxOnPos = self.fxOnText.get_rect(topleft=self.fxPos.topright)
        self.fxOffPos = self.fxOffText.get_rect(topleft=self.fxPos.topright)
        self.musicText = self.font.render('MUSIC', 1, BLACK)
        self.musicPos = self.fxText.get_rect(topleft=self.fxPos.bottomleft)
        self.musicOnText = self.font.render('ON', 1, RED)
        self.musicOffText = self.font.render('OFF', 1, RED)
        self.musicOnPos = self.musicOnText.get_rect(topleft=self.musicPos.topright)
        self.musicOffPos = self.musicOffText.get_rect(topleft=self.musicPos.topright)
        self.helpText=self.font.render('HELP',1,BLACK)
        self.helpPos=self.helpText.get_rect(topleft=self.musicPos.bottomleft)
        self.quitText = self.font.render('QUIT', 1, BLACK)
        self.selectText = self.font.render('*', 1, BLACK)
        self.selectPos = self.selectText.get_rect(topright=self.startPos.topleft)

        # For Select Mode setting
        self.singleText = self.font.render('SINGLE MODE', 1, BLACK)
        self.singlePos = self.singleText.get_rect(midtop=self.screen.get_rect().center)
        self.timeText = self.font.render('TIME MODE', 1, BLACK)
        self.timePos = self.timeText.get_rect(topleft=self.singlePos.bottomleft)
        self.pvpText = self.font.render('PVP MODE ', 1, BLACK)
        self.pvpPos = self.pvpText.get_rect(topleft=self.timePos.bottomleft)
        self.backText=self.font.render('BACK',1,BLACK)
        self.backPos=self.backText.get_rect(topleft=self.pvpPos.bottomleft)
        self.selectText = self.font.render('*', 1, BLACK)
        self.selectPos =self.selectText.get_rect(topright=self.singlePos.topleft)
        
        # For selection '*' setting        
        self.selectText = self.font.render('*', 1, BLACK)
        self.selextPos=''
        self.selectModeDict = {1:self.singlePos,2:self.timePos,3:self.pvpPos,4:self.backPos}
        self.menuDict = {1: self.startPos, 2: self.hiScorePos, 3:self.fxPos, 4: self.musicPos, 5:self.helpPos,6: self.quitPos}
        self.selectScoresDict = {1:self.singlePos,2:self.timePos,3:self.backPos}
        self.menuDict = {1: self.loginPos, 2: self.signPos,3:self.quitPos}
        self.loginDict={}
        self.selection = 1
        self.ininitalMenu=True
        self.showlogin=False
        self.showsign=False
        self.textOverlays=0
        self.inMenu = False
        self.showHelp=False
        self.showSelectModes=False
        self.showHiScores = False
        self.inSelectMenu=False
        self.soundFX = Database.getSound()
        self.music = Database.getSound(music=True)


    def init_page(self):        
        while self.ininitalMenu:
            self.clock.tick(self.clockTime) 
            
            main_menu, main_menuRect = load_image("main_menu.png")
            main_menuRect.midtop = self.screen.get_rect().midtop
            main_menu_size = (round(main_menu.get_width() * self.ratio), round(main_menu.get_height() * self.ratio))
            self.screen.blit(pygame.transform.scale(main_menu, main_menu_size), (0,0))

            for event in pygame.event.get():
                if (event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                # Resize windowSize
                elif (event.type == pygame.VIDEORESIZE):
                    self.screen_size = min(event.w, event.h)
                    if self.screen_size <= 300:
                        self.screen_size = 300
                    self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
                    self.ratio = (self.screen_size / 500)
                    self.font = pygame.font.Font(None, round(36*self.ratio))
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_RETURN):
                    if self.showlogin:
                        self.showlogin = False
                    elif self.selection == 1:
                        self.showlogin=True 
                        self.ininitalMenu = False
                        return 1, self.screen_size
                    elif self.selection == 2:
                        return 2, self.screen_size
                    elif self.selection == 3:
                        return 3, self.screen_size
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_UP
                    and self.selection > 1
                    and not self.showlogin):
                    self.selection -= 1
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_DOWN
                    and self.selection < len(menuDict)
                    and not self.showlogin):
                    self.selection += 1
            self.blankText=self.font.render('       ',1,BLACK)
            self.blankPos=self.blankText.get_rect(topright=self.screen.get_rect().center)
            self.loginText = self.font.render('LOG IN', 1, BLACK)
            self.loginPos = self.loginText.get_rect(topleft=self.blankPos.bottomleft)
            self.signText=self.font.render('SIGN UP',1,BLACK)
            self.signPos=self.signText.get_rect(topleft=self.loginPos.bottomleft)
            self.quitText=self.font.render('QUIT',1,BLACK)
            self.quitPos=self.quitText.get_rect(topleft=self.signPos.bottomleft)
            menuDict = {1: self.loginPos, 2: self.signPos,3:self.quitPos}
            self.selectPos = self.selectText.get_rect(topright=menuDict[self.selection].topleft)
            self.textOverlays = zip([self.blankText,self.loginText, self.signText,self.quitText,self.selectText],
                                [self.blankPos,self.loginPos, self.signPos,self.quitPos,self.selectPos])

            for txt, pos in self.textOverlays:
                self.screen.blit(txt, pos)
            pygame.display.flip()
    

    def login_sign_page(self,userSelection):
        self.showlogin=True
        self.ininitalMenu=False
        while self.showlogin:
            self.clock.tick(self.clockTime) 

            main_menu, main_menuRect = load_image("main_menu.png")
            main_menuRect.midtop = self.screen.get_rect().midtop
            main_menu_size = (round(main_menu.get_width() * self.ratio), round(main_menu.get_height() * self.ratio))
            self.screen.blit(pygame.transform.scale(main_menu, main_menu_size), (0,0))

            for event in pygame.event.get():
                if (event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                # Resize windowSize
                elif (event.type == pygame.VIDEORESIZE):
                    self.screen_size = min(event.w, event.h)
                    if self.screen_size <= 300:
                        self.screen_size = 300
                    self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
                    self.ratio = (self.screen_size / 500)
                    self.font = pygame.font.Font(None, round(36*self.ratio))
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_RETURN):
                    if (self.selection==1
                    or self.selection==2) :
                        if userSelection==1: # login
                            if Database().id_not_exists(self.id):
                                print("아이디 없음")
                            else: 
                                if Database().compare_data(self.id, self.pwd):
                                    print("로그인 성공")
                                    return self.id, self.screen_size
                                else:
                                    print("비번 확인")
                        elif userSelection==2: # signup
                            if Database().id_not_exists(self.id):
                                print("아이디 없음")
                                if self.pwd!='':
                                    Database().add_id_data(self.id)
                                    Database().add_password_data(self.pwd, self.id)
                                    print("회원가입 성공")
                                    return self.id, self.screen_size
                            else:
                                print("아이디 존재함")
                        
                    elif self.selection == 3:
                        return False, self.screen_size
                    
                elif (event.type == pygame.KEYDOWN
                    and self.selection==1
                    and event.key in Keyboard.keys.keys()
                    and len(self.idBuffer) < 8):
                    self.idBuffer.append(Keyboard.keys[event.key])
                    self.id = ''.join(self.idBuffer)
                elif (event.type == pygame.KEYDOWN
                    and self.selection==1
                    and event.key == pygame.K_BACKSPACE
                    and len(self.idBuffer) > 0):
                    self.idBuffer.pop()
                    self.id = ''.join(self.idBuffer)
                elif (event.type == pygame.KEYDOWN
                    and self.selection==2
                    and event.key in Keyboard.keys.keys()
                    and len(self.pwdBuffer) < 8):
                    self.pwdBuffer.append(Keyboard.keys[event.key])
                    self.pwd = ''.join(self.pwdBuffer)
                elif (event.type == pygame.KEYDOWN
                    and self.selection==2
                    and event.key == pygame.K_BACKSPACE
                    and len(self.pwdBuffer) > 0):
                    self.pwdBuffer.pop()
                    self.pwd = ''.join(self.pwdBuffer)
                    
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_UP
                    and self.selection > 1):
                    self.selection -= 1
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_DOWN
                    and self.selection < len(self.loginDict)):
                    self.selection += 1

            self.blankText=self.font.render('     ',1,BLACK)
            self.blankPos=self.blankText.get_rect(topright=self.screen.get_rect().center)
            self.enterIdText=self.font.render('ID  ',1,BLACK)
            self.enterIdPos=self.enterIdText.get_rect(topleft=self.blankPos.bottomleft)
            self.idText = self.font.render(self.id, 1, WHITE)
            self.idPos = self.idText.get_rect(topleft=self.enterIdPos.bottomleft)
            self.enterPwdText=self.font.render('PWD',1,BLACK)
            self.enterPwdPos=self.enterPwdText.get_rect(topleft=self.idPos.bottomleft)
            self.secretPwd='*'*len(self.pwd)
            self.pwdText = self.font.render(self.secretPwd, 1, WHITE)
            self.pwdPos = self.pwdText.get_rect(topleft=self.enterPwdPos.bottomleft)
            self.backText = self.font.render('BACK', 1, BLACK)
            self.backPos = self.backText.get_rect(topleft=self.pwdPos.bottomleft)
            self.selectText = self.font.render('*', 1, BLACK)
            self.loginDict={1:self.idPos,2:self.pwdPos,3:self.backPos}
            self.selectPos = self.selectText.get_rect(topright=self.loginDict[self.selection].topleft)
            self.textOverlays = zip([self.blankText,self.enterIdText, self.idText,self.enterPwdText,self.pwdText,self.selectText,self.backText],
                                [self.blankPos,self.enterIdPos, self.idPos,self.enterPwdPos,self.pwdPos,self.selectPos,self.backPos])

            for txt, pos in self.textOverlays:
                self.screen.blit(txt, pos)
            pygame.display.flip()
    

    def inMenu_page(self):
        self.inMenu = True
        cnt=0

        while self.inMenu:
            self.clock.tick(self.clockTime) 
            self.flag=True
            main_menu, main_menuRect = load_image("main_menu.png")
            main_menuRect.midtop = self.screen.get_rect().midtop
            main_menu_size = (round(main_menu.get_width() * self.ratio), round(main_menu.get_height() * self.ratio))
            self.screen.blit(pygame.transform.scale(main_menu, main_menu_size), (0,0))
 
            for event in pygame.event.get():
                if (event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                # Resize windowSize
                elif (event.type == pygame.VIDEORESIZE):
                    self.screen_size = min(event.w, event.h)
                    if self.screen_size <= 300:
                        self.screen_size = 300
                    self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
                    self.ratio = (self.screen_size / 500)
                    self.font = pygame.font.Font(None, round(36*self.ratio))
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_RETURN):
                    if self.showSelectModes:
                        self.showSelectModes = False
                    elif self.showHelp:
                        cnt+=1
                        if cnt%3!=0:
                            self.showHelp=True
                        else:
                            self.showHelp=False
                    elif self.selection == 1:
                        return 1, self.screen_size
                    elif self.selection == 2:
                        return 2, self.screen_size
                    elif self.selection == 3:
                        self.soundFX = not self.soundFX
                        if self.soundFX:
                            leaf_sound.play()
                        Database.setSound(int(self.soundFX))
                    elif self.selection == 4 and pygame.mixer:
                        self.music = not self.music
                        if self.music:
                            pygame.mixer.music.play(loops=-1)
                        else:
                            pygame.mixer.music.stop()
                        Database.setSound(int(self.music), music=True)
                    elif self.selection == 5:
                        cnt+=1
                        self.showHelp=True                                        
                    elif self.selection == 6:
                        return 6, self.screen_size
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_UP
                    and self.selection > 1
                    and not self.showHiScores
                    and not self.showSelectModes
                    and not self.showHelp):
                    self.selection -= 1
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_DOWN
                    and self.selection < len(self.menuDict)
                    and not self.showHiScores
                    and not self.showSelectModes):
                    self.selection += 1
            
            self.blankText=self.font.render('           ',1,BLACK)
            self.blankPos=self.blankText.get_rect(topright=self.screen.get_rect().center)
            self.startText = self.font.render('SELECT MODE', 1, BLACK)
            self.startPos = self.startText.get_rect(topleft=self.blankPos.bottomleft)
            self.hiScoreText = self.font.render('HIGH SCORE', 1, BLACK)
            self.hiScorePos = self.hiScoreText.get_rect(topleft=self.startPos.bottomleft)
            self.fxText = self.font.render('SOUND FX ', 1, BLACK)
            self.fxPos = self.fxText.get_rect(topleft=self.hiScorePos.bottomleft)
            self.fxOnText = self.font.render('ON', 1, RED)
            self.fxOffText = self.font.render('OFF', 1, RED)
            self.fxOnPos = self.fxOnText.get_rect(topleft=self.fxPos.topright)
            self.fxOffPos = self.fxOffText.get_rect(topleft=self.fxPos.topright)
            self.musicText = self.font.render('MUSIC', 1, BLACK)
            self.musicPos = self.fxText.get_rect(topleft=self.fxPos.bottomleft)
            self.musicOnText = self.font.render('ON', 1, RED)
            self.musicOffText = self.font.render('OFF', 1, RED)
            self.musicOnPos = self.musicOnText.get_rect(topleft=self.musicPos.topright)
            self.musicOffPos = self.musicOffText.get_rect(topleft=self.musicPos.topright)
            self.helpText=self.font.render('HELP',1,BLACK)
            self.helpPos=self.helpText.get_rect(topleft=self.musicPos.bottomleft)
            self.quitText = self.font.render('QUIT', 1, BLACK)
            self.quitPos = self.quitText.get_rect(topleft=self.helpPos.bottomleft)

            self.menuDict = {1: self.startPos, 2: self.hiScorePos, 3:self.fxPos, 4: self.musicPos, 5:self.helpPos,6: self.quitPos}
            self.selectPos = self.selectText.get_rect(topright=self.menuDict[self.selection].topleft)


            if self.showHelp:
                if cnt%3==1:
                    menu, menuRect = load_image("help1.png")
                    menuRect.midtop = self.screen.get_rect().midtop
                    menu_size = (round(menu.get_width() * self.ratio), round(menu.get_height() * self.ratio))
                    self.screen.blit(pygame.transform.scale(menu, menu_size), (0,0))
                elif cnt%3==2:
                    menu, menuRect = load_image("help2.png")
                    menuRect.midtop = self.screen.get_rect().midtop
                    menu_size = (round(menu.get_width() * self.ratio), round(menu.get_height() * self.ratio))
                    self.screen.blit(pygame.transform.scale(menu, menu_size), (0,0))
            else:
                self.textOverlays = zip([self.blankText,self.startText, self.hiScoreText, self.helpText, self.fxText,
                                    self.musicText, self.quitText, self.selectText,
                                    self.fxOnText if self.soundFX else self.fxOffText,
                                    self.musicOnText if self.music else self.musicOffText],
                                [self.blankPos,self.startPos, self.hiScorePos, self.helpPos, self.fxPos,
                                    self.musicPos, self.quitPos, self.selectPos,
                                    self.fxOnPos if self.soundFX else self.fxOffPos,
                                    self.musicOnPos if self.music else self.musicOffPos])
            for txt, pos in self.textOverlays:
                self.screen.blit(txt, pos)
            pygame.display.flip()


    def select_game_page(self):
        main_menu, main_menuRect = load_image("main_menu.png")
        main_menuRect.midtop = self.screen.get_rect().midtop
        inSelectMenu=True
        showSingleMode = False
        showTimeMode = False
        showPvpMode = False
        
        while inSelectMenu:
            self.clock.tick(self.clockTime)
            main_menu_size = (round(main_menu.get_width() * self.ratio), round(main_menu.get_height() * self.ratio))
            self.screen.blit(pygame.transform.scale(main_menu, main_menu_size), (0,0))

            for event in pygame.event.get():
                if (event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                # Resize windowSize
                elif (event.type == pygame.VIDEORESIZE):
                    self.screen_size = min(event.w, event.h)
                    if self.screen_size <= 300:
                        self.screen_size = 300
                    self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
                    self.ratio = (self.screen_size / 500)
                    self.font = pygame.font.Font(None, round(36*self.ratio))
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_RETURN):
                    if showSingleMode:
                        showSingleMode = False
                    elif showTimeMode:
                        showTimeMode = False
                    elif showPvpMode:
                        showPvpMode = False
                    elif self.selection == 1:
                        inSelectMenu = False
                        selectMode = 'SingleMode'
                        return selectMode, self.screen_size
                    elif self.selection == 2:
                        inSelectMenu = False
                        selectMode = 'TimeMode'
                        return selectMode, self.screen_size
                    elif self.selection == 3:
                        inSelectMenu = False
                        selectMode = 'PvpMode'
                        return selectMode, self.screen_size
                    elif self.selection == 4:
                        inSelectMenu = False
                        return BACK, self.screen_size
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_UP
                    and self.selection > 1
                    and not showSingleMode
                    and not showTimeMode
                    and not showPvpMode):
                    self.selection -= 1
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_DOWN
                    and self.selection < len(self.selectModeDict)
                    and not showSingleMode
                    and not showTimeMode
                    and not showPvpMode):
                    self.selection += 1
            
            self.blankText=self.font.render('       ',1,BLACK)
            self.blankPos=self.blankText.get_rect(topright=self.screen.get_rect().center)
            self.singleText = self.font.render('SINGLE', 1, BLACK)
            self.singlePos = self.singleText.get_rect(topleft=self.blankPos.bottomleft)
            self.timeText = self.font.render('TIME', 1, BLACK)
            self.timePos = self.timeText.get_rect(topleft=self.singlePos.bottomleft)
            self.pvpText = self.font.render('PVP', 1, BLACK)
            self.pvpPos = self.pvpText.get_rect(topleft=self.timePos.bottomleft)
            self.backText=self.font.render('BACK',1,BLACK)
            self.backPos=self.backText.get_rect(topleft=self.pvpPos.bottomleft)
            
            self.selectModeDict = {1:self.singlePos,2:self.timePos,3:self.pvpPos,4:self.backPos}
            self.selectText = self.font.render('*', 1, BLACK)
            self.selectPos = self.selectText.get_rect(topright=self.selectModeDict[self.selection].topleft)

            textOverlays = zip([self.blankText,self.singleText,self.timeText,self.pvpText,self.selectText,self.backText],
            [self.blankPos,self.singlePos,self.timePos,self.pvpPos,self.selectPos,self.backPos])
            for txt, pos in textOverlays:
                self.screen.blit(txt, pos)
            
            pygame.display.flip()
    

    def score_page(self):
        main_menu, main_menuRect = load_image("main_menu.png")
        main_menuRect.midtop = self.screen.get_rect().midtop

        inScoreMenu=True
        showSingleScores =False
        showTimeScores=False

        while inScoreMenu:
            self.clock.tick(self.clockTime)
            main_menu_size = (round(main_menu.get_width() * self.ratio), round(main_menu.get_height() * self.ratio))
            self.screen.blit(pygame.transform.scale(main_menu, main_menu_size), (0,0))
            for event in pygame.event.get():
                if (event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                # Resize windowSize
                elif (event.type == pygame.VIDEORESIZE):
                    self.screen_size = min(event.w, event.h)
                    if self.screen_size <= 300:
                        self.screen_size = 300
                    self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
                    self.ratio = (self.screen_size / 500)
                    self.font = pygame.font.Font(None, round(36*self.ratio))
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_RETURN):
                    if showSingleScores:
                        showSingleScores = False
                    elif showTimeScores:
                        showTimeScores = False
                    elif self.selection == 1:
                        showSingleScores=True 
                    elif self.selection == 2:
                        showTimeScores = True
                    elif self.selection == 3:
                        return BACK, self.screen_size 
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_UP
                    and self.selection > 1
                    and not showSingleScores
                    and not showTimeScores):
                    self.selection -= 1
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_DOWN
                    and self.selection < len(self.selectScoresDict)
                    and not showSingleScores
                    and not showTimeScores):
                    self.selection += 1 

            self.blankText=self.font.render('      ',1,BLACK)
            self.blankPos=self.blankText.get_rect(topright=self.screen.get_rect().center)
            self.singleText=self.font.render('SINGLE  ',1,BLACK)
            self.singlePos=self.singleText.get_rect(topleft=self.blankPos.bottomleft)
            self.timeText = self.font.render('TIME', 1, BLACK)
            self.timePos = self.timeText.get_rect(topleft=self.singlePos.bottomleft)
            self.backText = self.font.render('BACK', 1, BLACK)
            self.backPos = self.backText.get_rect(topleft=self.timePos.bottomleft)

            selectScoresDict = {1:self.singlePos,2:self.timePos,3:self.backPos}
            self.selectPos= self.selectText.get_rect(topright=selectScoresDict[self.selection].topleft)

            self.highScoreTexts = [self.font.render("NAME", 1, RED), #폰트 렌터
                            self.font.render("SCORE", 1, RED),
                            self.font.render("ACCURACY", 1, RED)]
            self.highScorePos = [self.highScoreTexts[0].get_rect(
                            topleft=self.screen.get_rect().inflate(-100, -100).topleft),
                            self.highScoreTexts[1].get_rect(
                            midtop=self.screen.get_rect().inflate(-100, -100).midtop),
                            self.highScoreTexts[2].get_rect(
                            topright=self.screen.get_rect().inflate(-100, -100).topright)]
            self.timeHighScoreTexts= [self.font.render("NAME", 1, RED), #폰트 렌터
                            self.font.render("SCORE", 1, RED),
                            self.font.render("ACCURACY", 1, RED)]
            self.timeHighScorePos = [self.timeHighScoreTexts[0].get_rect(
                            topleft=self.screen.get_rect().inflate(-100, -100).topleft),
                            self.timeHighScoreTexts[1].get_rect(
                            midtop=self.screen.get_rect().inflate(-100, -100).midtop),
                            self.timeHighScoreTexts[2].get_rect(
                            topright=self.screen.get_rect().inflate(-100, -100).topright)]
            for hs in self.hiScores:
                self.highScoreTexts.extend([self.font.render(str(hs[x]), 1, BLACK)
                                    for x in range(3)])
                self.highScorePos.extend([self.highScoreTexts[x].get_rect(
                    topleft=self.highScorePos[x].bottomleft) for x in range(-3, 0)])
            for hs in self.timeHiScores:
                self.timeHighScoreTexts.extend([self.font.render(str(hs[x]), 1, BLACK)
                                    for x in range(3)])
                self.timeHighScorePos.extend([self.timeHighScoreTexts[x].get_rect(
                    topleft=self.timeHighScorePos[x].bottomleft) for x in range(-3, 0)])

            if showSingleScores:
                menu, menuRect = load_image("menu.png")
                menuRect.midtop = self.screen.get_rect().midtop
                menu_size = (round(menu.get_width() * self.ratio), round(menu.get_height() * self.ratio))
                self.screen.blit(pygame.transform.scale(menu, menu_size), (0,0))
                textOverlays = zip(self.highScoreTexts, self.highScorePos)
            elif showTimeScores:
                menu, menuRect = load_image("menu.png")
                menuRect.midtop = self.screen.get_rect().midtop
                menu_size = (round(menu.get_width() * self.ratio), round(menu.get_height() * self.ratio))
                self.screen.blit(pygame.transform.scale(menu, menu_size), (0,0))
                textOverlays = zip(self.timeHighScoreTexts, self.timeHighScorePos)
            else:
                textOverlays = zip([self.blankText,self.singleText, self.timeText,self.backText,self.selectText],
                                [self.blankPos,self.singlePos, self.timePos,self.backPos, self.selectPos])
            for txt, pos in textOverlays:
                self.screen.blit(txt, pos)
            pygame.display.flip()