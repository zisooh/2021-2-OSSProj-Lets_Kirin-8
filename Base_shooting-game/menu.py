import pygame
from load import load_image, load_sound, load_music
from collections import deque
import random

BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

class Menu:
    def __init__(self):
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
        self.screen = pygame.display.set_mode((500, 500))
        self.font = pygame.font.Font(None, 36)
        self.title, self.titleRect = load_image('title.png')
        self.titleRect.midtop = self.screen.get_rect().inflate(0, -200).midtop
        self.loginText = self.font.render('log in', 1, BLUE)
        self.loginPos = self.loginText.get_rect(midtop=self.titleRect.inflate(0, 100).midbottom)
        self.signText=self.font.render('sign up',1,BLUE)
        self.signPos=self.signText.get_rect(topleft=self.loginPos.bottomleft)

        self.speed = 1.5
        self.clockTime = 60  # maximum FPS
        self.clock = pygame.time.Clock()
        self.selectText = self.font.render('*', 1, BLUE)
        self.selectPos = self.selectText.get_rect(topright=self.loginPos.topleft)
        self.ininitalMenu=True
        self.menuDict = {1: self.loginPos, 2: self.signPos}
        self.selection = 1
        self.showlogin=False
        self.selectPos =self.selectText.get_rect(topright=self.menuDict[self.selection].topleft)
        self.textOverlays=0

    def login(self):
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
                    elif self.selection == 2:
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

            if self.showlogin:
                self.textOverlays = zip(self.loginText, self.loginPos)
            else:
                self.textOverlays = zip([self.loginText, self.signText,self.selectText],
                                [self.loginPos, self.signPos,self.selectPos])
                self.screen.blit(self.title, self.titleRect)
            for txt, pos in self.textOverlays:
                self.screen.blit(txt, pos)
            pygame.display.flip()