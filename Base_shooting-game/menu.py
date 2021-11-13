import pygame
from load import load_image, load_sound, load_music
from collections import deque
import random

BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

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
        self.title, self.titleRect = load_image('title.png')
        self.titleRect.midtop = self.screen.get_rect().inflate(0, -200).midtop
        #For init_page setting
        self.loginText = self.font.render('LOG IN', 1, BLUE)
        self.loginPos = self.loginText.get_rect(midtop=self.titleRect.inflate(0, 100).midbottom)
        self.signText=self.font.render('SIGN UP',1,BLUE)
        self.signPos=self.signText.get_rect(topleft=self.loginPos.bottomleft)
        self.quitText=self.font.render('QUIT',1,BLUE)
        self.quitPos=self.quitText.get_rect(topleft=self.signPos.bottomleft)
        #For login_page setting
        self.idText=self.font.render('ID:',1,BLUE)
        self.idPos=self.idText.get_rect(midtop=self.titleRect.inflate(0, 100).midbottom)
        self.pwdText=self.font.render('PWD:',1,BLUE)
        self.pwdPos=self.pwdText.get_rect(topleft=self.idPos.bottomleft)
        self.signText2=self.font.render('SIGN UP',1,BLUE)
        self.signPos2=self.signText2.get_rect(topleft=self.pwdPos.bottomleft)
        self.quitText2=self.font.render('QUIT',1,BLUE)
        self.quitPos2=self.quitText2.get_rect(topleft=self.signPos2.bottomleft)
        #For selection '*' setting        
        self.selectText = self.font.render('*', 1, BLUE)
        self.selextPos=0
        self.selectPos = self.selectText.get_rect(topright=self.loginPos.topleft)

        self.ininitalMenu=True
        self.menuDict = {1: self.loginPos, 2: self.signPos,3:self.quitPos}
        self.loginDict={1:self.idPos,2:self.pwdPos,3:self.signPos2,4:self.quitPos2}
        self.selection = 1
        self.showlogin=False
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
            self.backgroundLoc -= self.speed
            if self.backgroundLoc - self.speed <= self.speed:
                self.backgroundLoc = 1500

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
                        return
                    elif self.selection==3:
                        return
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_w
                    and self.selection > 1
                    and not self.showlogin):
                    self.selection -= 1
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_s
                    and self.selection < len(self.menuDict)
                    and not self.showlogin):
                    self.selection += 1

            self.selectPos = self.selectText.get_rect(topright=self.menuDict[self.selection].topleft)
            self.textOverlays = zip([self.loginText, self.signText,self.quitText,self.selectText],
                                [self.loginPos, self.signPos,self.quitPos,self.selectPos])
            self.screen.blit(self.title, self.titleRect)

            for txt, pos in self.textOverlays:
                self.screen.blit(txt, pos)
            pygame.display.flip()
    
    def login_page(self):
        #print("함수 호출 성공")
        #self.log_test=["jiyyon","zz"]
        #print(self.log_test)
        self.showlogin=True
        self.ininitalMenu=False
        while self.showlogin:
            self.clock.tick(self.clockTime) 
            self.screen.blit(
                self.background, (0, 0), area=pygame.Rect(
                    0, self.backgroundLoc, 500, 500))
            self.backgroundLoc -= self.speed
            if self.backgroundLoc - self.speed <= self.speed:
                self.backgroundLoc = 1500
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    return
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_RETURN):
                    # if self.ininitialMenu:
                    #     self.ininitalMenu=False
                    if self.selection == 1:
                        print("ID 쓰기 성공")
                        return
                    elif self.selection == 2:
                        print("PWD 쓰기 성공")
                        return 
                    elif self.selection == 3:
                        print("SIGN UP 성공")
                        return 
                    elif self.selection == 4:
                        print("QUIT 성공")
                        return 
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_w
                    and self.selection > 1):
                    self.selection -= 1
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_s
                    and self.selection < len(self.loginDict)):
                    self.selection += 1

            self.selectPos = self.selectText.get_rect(topright=self.loginDict[self.selection].topleft)
            self.textOverlays = zip([self.idText, self.pwdText,self.signText2,self.quitText2,self.selectText],
                                [self.idPos, self.pwdPos,self.signPos2,self.quitPos2,self.selectPos])
            self.screen.blit(self.title, self.titleRect)

            for txt, pos in self.textOverlays:
                self.screen.blit(txt, pos)
            pygame.display.flip()


    
    
        

    
 