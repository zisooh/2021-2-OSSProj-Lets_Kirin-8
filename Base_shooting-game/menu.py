import pygame
from load import load_image, load_sound, load_music
from collections import deque
import random
from database import Database

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
what_color=(0,255,255)

missile_sound = load_sound('missile.ogg')
bomb_sound = load_sound('bomb.ogg')
alien_explode_sound = load_sound('alien_explode.ogg')
ship_explode_sound = load_sound('ship_explode.ogg')
load_music('music_loop.ogg')

hiScores=Database().getScores()

class Keyboard(object):
    keys = {pygame.K_a: 'A', pygame.K_b: 'B', pygame.K_c: 'C', pygame.K_d: 'D',
            pygame.K_e: 'E', pygame.K_f: 'F', pygame.K_g: 'G', pygame.K_h: 'H',
            pygame.K_i: 'I', pygame.K_j: 'J', pygame.K_k: 'K', pygame.K_l: 'L',
            pygame.K_m: 'M', pygame.K_n: 'N', pygame.K_o: 'O', pygame.K_p: 'P',
            pygame.K_q: 'Q', pygame.K_r: 'R', pygame.K_s: 'S', pygame.K_t: 'T',
            pygame.K_u: 'U', pygame.K_v: 'V', pygame.K_w: 'W', pygame.K_x: 'X',
            pygame.K_y: 'Y', pygame.K_z: 'Z'}

class Menu:
    def __init__(self):
        #Game initial setting -> To be modified
        self.background = pygame.Surface((500, 2000))
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        self.backgroundLoc = 1500
        self.finalStars = deque()
        for y in range(0, 1500, 30):
            size = random.randint(2, 5)
            x = random.randint(0, 500 - size)
            if y <= 500:
                self.finalStars.appendleft((x, y + 1500, size))
            pygame.draw.rect(
                self.background, (255, 255, 0), pygame.Rect(x, y, size, size))
        while self.finalStars:
            x, y, size = self.finalStars.pop()
            pygame.draw.rect(
                self.background, (255, 255, 0), pygame.Rect(x, y, size, size))
        
        self.speed = 1.5
        self.clockTime = 60  # maximum FPS
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((500, 500))
        self.font = pygame.font.Font(None, 36)
        # 아래 title 두줄 없어도 되는데 loginPo가 얘 기준으로 잡고있음
        self.title, self.titleRect = load_image('title.png')
        self.titleRect.midtop = self.screen.get_rect().inflate(0, -200).midtop
        #데베 호출
        self.highScoreTexts = [self.font.render("NAME", 1, RED), #폰트 렌터
                        self.font.render("SCORE", 1, RED),
                        self.font.render("ACCURACY", 1, RED)]
        self.highScorePos = [self.highScoreTexts[0].get_rect(
                        topleft=self.screen.get_rect().inflate(-100, -100).topleft),
                        self.highScoreTexts[1].get_rect(
                        midtop=self.screen.get_rect().inflate(-100, -100).midtop),
                        self.highScoreTexts[2].get_rect(
                        topright=self.screen.get_rect().inflate(-100, -100).topright)]
        for hs in hiScores:
            self.highScoreTexts.extend([self.font.render(str(hs[x]), 1, BLACK)
                                for x in range(3)])
            self.highScorePos.extend([self.highScoreTexts[x].get_rect(
                topleft=self.highScorePos[x].bottomleft) for x in range(-3, 0)])
        #For init_page setting
        self.loginText = self.font.render('LOG IN', 1, BLACK)
        self.loginPos = self.loginText.get_rect(midtop=self.titleRect.inflate(0, 100).midbottom)
        self.signText=self.font.render('SIGN UP',1,BLACK)
        self.signPos=self.signText.get_rect(topleft=self.loginPos.bottomleft)
        self.quitText=self.font.render('QUIT',1,BLACK)
        self.quitPos=self.quitText.get_rect(topleft=self.signPos.bottomleft)
        #For login_page setting
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
        #For inMenu_page setting
        self.startText = self.font.render('SELECT MODES', 1, BLACK)
        self.startPos = self.startText.get_rect(midtop=self.titleRect.inflate(0, 100).midbottom)
        self.hiScoreText = self.font.render('HIGH SCORES', 1, BLACK)
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
        # self.quitPos = self.quitText.get_rect(topleft=self.helpPos.bottomleft)
        self.selectText = self.font.render('*', 1, BLACK)
        self.selectPos = self.selectText.get_rect(topright=self.startPos.topleft)

        # Select Mode 안 글씨
        self.singleText = self.font.render('SINGLE MODE', 1, BLACK)
        self.singlePos = self.singleText.get_rect(midtop=self.titleRect.inflate(0, 100).midbottom)
        self.timeText = self.font.render('TIME MODE', 1, BLACK)
        self.timePos = self.timeText.get_rect(topleft=self.singlePos.bottomleft)
        self.pvpText = self.font.render('PVP MODE ', 1, BLACK)
        self.pvpPos = self.pvpText.get_rect(topleft=self.timePos.bottomleft)
        self.backText=self.font.render('BACK',1,BLACK)
        self.backPos=self.backText.get_rect(topleft=self.pvpPos.bottomleft)
        self.selectText = self.font.render('*', 1, BLACK)
        self.selectPos =self.selectText.get_rect(topright=self.singlePos.topleft)
        self.menuDict = {1: self.startPos, 2: self.hiScorePos, 3:self.fxPos, 4: self.musicPos, 5:self.helpPos,6: self.quitPos}
        #For selection '*' setting        
        self.selectText = self.font.render('*', 1, BLACK)
        self.selextPos=0
        # self.selectPos = self.selectText.get_rect(topright=self.loginPos.topleft)
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
        self.soundFX = Database().getSound()
        self.music = Database().getSound(music=True)
        if self.music and pygame.mixer: 
            pygame.mixer.music.play(loops=-1)
        #user simple db
        self.log_test=[]
        self.userSelection=0

    def init_page(self):
        self.selectPos = self.selectText.get_rect(topright=self.loginPos.topleft)
        self.quitPos=self.quitText.get_rect(topleft=self.signPos.bottomleft)
        self.quitPos=self.quitText.get_rect(topleft=self.signPos.bottomleft)
        while self.ininitalMenu:
            self.clock.tick(self.clockTime) 
            self.screen.blit(
                self.background, (0, 0), area=pygame.Rect(
                    0, self.backgroundLoc, 500, 500))
            
            main_menu, main_menuRect = load_image("main_menu.png")
            main_menuRect.midtop = self.screen.get_rect().midtop
            self.screen.blit(main_menu, main_menuRect)

            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    return
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_RETURN):
                    if self.showlogin:
                        self.showlogin = False
                    elif self.selection == 1:
                        self.showlogin=True 
                        self.ininitalMenu = False
                        # Menu().login_page()
                        return 1
                    elif self.selection == 2:
                        return 2
                    elif self.selection == 3:
                        return 3
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_UP
                    and self.selection > 1
                    and not self.showlogin):
                    self.selection -= 1
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_DOWN
                    and self.selection < len(self.menuDict)
                    and not self.showlogin):
                    self.selection += 1

            self.selectPos = self.selectText.get_rect(topright=self.menuDict[self.selection].topleft)
            self.textOverlays = zip([self.loginText, self.signText,self.quitText,self.selectText],
                                [self.loginPos, self.signPos,self.quitPos,self.selectPos])

            for txt, pos in self.textOverlays:
                self.screen.blit(txt, pos)
            pygame.display.flip()
    
    def login_sign_page(self,userSelection):
        print(userSelection)
        self.showlogin=True
        self.ininitalMenu=False
        while self.showlogin:
            self.clock.tick(self.clockTime) 
            self.screen.blit(
                self.background, (0, 0), area=pygame.Rect(
                    0, self.backgroundLoc, 500, 500))

            main_menu, main_menuRect = load_image("main_menu.png")
            main_menuRect.midtop = self.screen.get_rect().midtop
            self.screen.blit(main_menu, main_menuRect)

            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    return
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_RETURN):
                    if (self.selection == 1
                    or self.selection==2
                    or self.selection==3
                    or self.selection==4) :
                        # print("다음 Return 성공")
                        if userSelection==1: #로그인 요청일때
                            if Database().id_not_exists(self.id):
                                print("아이디 없음")
                            else: 
                                if Database().compare_data(self.id, self.pwd):
                                    print("로그인 성공")
                                    return self.id
                                else:
                                    print("비번 확인")
                        elif userSelection==2: #회원가입 요청일때
                            if Database().id_not_exists(self.id):
                                print("아이디 없음")
                                if self.pwd!='':
                                    Database().add_id_data(self.id)
                                    Database().add_password_data(self.pwd, self.id)
                                    print("회원가입 성공")
                                    return self.id
                            else:
                                print("아이디 존재함")
                        
                    elif self.selection == 5:
                        return 0
                    
                elif (event.type == pygame.KEYDOWN
                    and self.selection==2
                    and event.key in Keyboard.keys.keys()
                    and len(self.idBuffer) < 8):
                    self.idBuffer.append(Keyboard.keys[event.key])
                    self.id = ''.join(self.idBuffer)
                elif (event.type == pygame.KEYDOWN
                    and self.selection==2
                    and event.key == pygame.K_BACKSPACE
                    and len(self.idBuffer) > 0):
                    self.idBuffer.pop()
                    self.id = ''.join(self.idBuffer)
                elif (event.type == pygame.KEYDOWN
                    and self.selection==4
                    and event.key in Keyboard.keys.keys()
                    and len(self.pwdBuffer) < 8):
                    self.pwdBuffer.append(Keyboard.keys[event.key])
                    self.pwd = ''.join(self.pwdBuffer)
                elif (event.type == pygame.KEYDOWN
                    and self.selection==4
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

            self.enterIdText=self.font.render('ID:  ',1,RED)
            self.enterIdPos=self.enterIdText.get_rect(topright=self.titleRect.inflate(0, 100).midbottom)
            self.idText = self.font.render(self.id, 1, WHITE)
            self.idPos = self.idText.get_rect(topleft=self.enterIdPos.bottomleft)
            self.enterPwdText=self.font.render('PWD:',1,RED)
            self.enterPwdPos=self.enterPwdText.get_rect(topleft=self.idPos.bottomleft)
            self.pwdText = self.font.render(self.pwd, 1, WHITE)
            self.pwdPos = self.pwdText.get_rect(topleft=self.enterPwdPos.bottomleft)
            self.backText = self.font.render('BACK', 1, BLACK)
            self.backPos = self.backText.get_rect(topleft=self.pwdPos.bottomleft)
            self.selectText = self.font.render('*', 1, BLACK)
            self.loginDict={1:self.enterIdPos,2:self.idPos,3:self.enterPwdPos,4:self.pwdPos,5:self.backPos}
            self.selectPos = self.selectText.get_rect(topright=self.loginDict[self.selection].topleft)
            self.textOverlays = zip([self.enterIdText, self.idText,self.enterPwdText,self.pwdText,self.selectText,self.backText],
                                [self.enterIdPos, self.idPos,self.enterPwdPos,self.pwdPos,self.selectPos,self.backPos])

            for txt, pos in self.textOverlays:
                self.screen.blit(txt, pos)
            pygame.display.flip()
    
    def inMenu_page(self):
        self.inMenu = True
        self.quitPos = self.quitText.get_rect(topleft=self.helpPos.bottomleft)
        while self.inMenu:
            self.clock.tick(self.clockTime) 
            self.flag=True
            main_menu, main_menuRect = load_image("main_menu.png")
            main_menuRect.midtop = self.screen.get_rect().midtop
            self.screen.blit(main_menu, main_menuRect)
 
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    return
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_RETURN):
                    if self.showHiScores:
                        self.showHiScores = False
                    elif self.showSelectModes:
                        self.showSelectModes = False
                    elif self.showHelp:
                        self.showHelp=False
                    elif self.selection == 1:
                        self.showSelectModes=True 
                        self.inMenu = False
                        self.inSelectMenu=True
                        return 1
                    elif self.selection == 2:
                        self.showHiScores = True
                    elif self.selection == 3:
                        self.soundFX = not self.soundFX
                        if self.soundFX:
                            missile_sound.play()
                        Database().setSound(int(self.soundFX))
                    elif self.selection == 4 and pygame.mixer:
                        self.music = not self.music
                        if self.music:
                            pygame.mixer.music.play(loops=-1)
                        else:
                            pygame.mixer.music.stop()
                        Database().setSound(int(self.music), music=True)
                    elif self.selection == 5:
                        self.showHelp=True                                        
                    elif self.selection == 6:
                        return 6
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
            
            self.menuDict = {1: self.startPos, 2: self.hiScorePos, 3:self.fxPos, 4: self.musicPos, 5:self.helpPos,6: self.quitPos}
            self.selectPos = self.selectText.get_rect(topright=self.menuDict[self.selection].topleft)


            if self.showHiScores:
                self.screen.blit(self.background, (0, 0))
                img_menu, img_menuRect = load_image("menu.png")
                img_menuRect.midtop = self.screen.get_rect().midtop
                self.screen.blit(img_menu, img_menuRect)
                self.textOverlays = zip(self.highScoreTexts, self.highScorePos)
            elif self.showHelp:
                self.screen.blit(self.background, (0, 0))
                img_menu, img_menuRect = load_image("pause.png") #Help 이미지는 예시로
                img_menuRect.midtop = self.screen.get_rect().midtop
                self.screen.blit(img_menu, img_menuRect) 
            elif self.showSelectModes:
                self.textOverlays = zip([self.singleText,self.timeText,self.pvpText],[self.singlePos,self.timePos,self.pvpPos])
            else:
                self.textOverlays = zip([self.startText, self.hiScoreText, self.helpText, self.fxText,
                                    self.musicText, self.quitText, self.selectText,
                                    self.fxOnText if self.soundFX else self.fxOffText,
                                    self.musicOnText if self.music else self.musicOffText],
                                [self.startPos, self.hiScorePos, self.helpPos, self.fxPos,
                                    self.musicPos, self.quitPos, self.selectPos,
                                    self.fxOnPos if self.soundFX else self.fxOffPos,
                                    self.musicOnPos if self.music else self.musicOffPos])
            for txt, pos in self.textOverlays:
                self.screen.blit(txt, pos)
            pygame.display.flip()


    
    
        

    
 