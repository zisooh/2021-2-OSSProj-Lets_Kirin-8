import pygame
from load import load_image, load_sound, load_music
from collections import deque
import random

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)


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
        #For selection '*' setting        
        self.selectText = self.font.render('*', 1, BLACK)
        self.selextPos=0
        self.selectPos = self.selectText.get_rect(topright=self.loginPos.topleft)
        self.menuDict = {1: self.loginPos, 2: self.signPos,3:self.quitPos}
        self.loginDict={}
        self.selection = 1
        self.ininitalMenu=True
        self.showlogin=False
        self.showsign=False
        self.textOverlays=0
        #user simple db
        self.log_test=[]
        self.userSelection=0

    def init_page(self):
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
    
    def login_page(self):
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
                        print("다음 Return 성공")
                        return self.id,self.pwd
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

    def sign_page(self):
        Menu().login_page()


    
    
        

    
 