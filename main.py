'''
Author: Ali Asgar Khawasawala
Description: A simple ball shooting game developed with Python and PyGame for building the concentration power and the knowledge of even and odd numbers in kids.
'''

import sys
import random
import math
import time
import pygame

# Class for creating Background Tiles.
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, picture_path):
        super().__init__() # Initializing Base Class
        self.image = pygame.image.load(picture_path) # Loading Image
        self.rect = self.image.get_rect() # Creating Rect Object
        self.rect.topleft = (pos_x, pos_y) # Positioning Rect Object


# Class for UI Elements
class UI_Element(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, imgList, label, type):
        super().__init__()
        self.x = pos_x
        self.y = pos_y
        self.type = type
        self.imgIndex = 0 
        self.images = []

        for i in imgList:
            self.images.append(pygame.image.load(i)) 

        self.image = self.images[self.imgIndex]

        self.imgWidth = self.image.get_width()
        self.imgHeight = self.image.get_height()

        font = pygame.font.Font("assets/KenneyFutureNarrow.ttf", 20)
        self.label = label
        self.labelFont = font.render(self.label, True, (255,255,255))
        self.labelWidth = self.labelFont.get_width()
        self.labelHeight = self.labelFont.get_height()
        
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        mousePos = pygame.mouse.get_pos()
        # print(f"Mouse x: {mousePos[0]}")
        # print(f"Mouse y: {mousePos[1]}")
        if mousePos[0] >= self.rect.x and mousePos[0] <= (self.rect.x + self.rect.width) and mousePos[1] >= self.rect.y and mousePos[1] <= (self.rect.y + self.rect.height):
            self.imgIndex = 1
        else:
            self.imgIndex = 0

        if self.imgIndex >= len(self.images):
            self.imgIndex = 0
        
        self.image = self.images[self.imgIndex]
        self.image.blit(self.labelFont, (int(self.imgWidth/2 - self.labelWidth/2), int(self.imgHeight/2 - self.labelHeight/2)))
        
# Class for creating Crosshair like Mouse Pointer.
class Crosshair(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__() # Initializing Base Class
        self.image = pygame.image.load(picture_path) # Loading Image
        self.rect = self.image.get_rect() # Creating Rect Object
    
    # Defition for Play and Exit Button
    def gameUI(self):
        uiCollide = pygame.sprite.spritecollide(crosshair, stage.ui_group, False)
        btnSound = pygame.mixer.Sound('assets/btn.ogg')
        
        if uiCollide and uiCollide[0].type == "button":
            btnSound.play()
            time.sleep(0.4)

        if uiCollide and uiCollide[0].label == "PLAY" or uiCollide[0].label == "REPLAY":
            stage.createBall()
            stage.currentScreen = "Game Screen" # Changing screen to Game Play

        elif uiCollide and uiCollide[0].label == "EXIT":
            pygame.quit()
            sys.exit()

    # Defining what to do if crosshair collide with ball and shoot.
    def shoot(self):
        # Checking whether crosshair is on ball while shooting
        ball = pygame.sprite.spritecollide(crosshair, stage.ball_group, False)
        shootSound = pygame.mixer.Sound('assets/shoot.ogg') 
        # Checking if ball is even or odd.
        if ball and ball[0].is_even:
            shootSound.play()
            stage.totalEvenBalls -= 1
            stage.ball_group.remove(ball[0])
            if stage.totalEvenBalls <= 0:
                stage.currentScreen = "Game Over" # Changing screen to Game Over
                stage.lastTimer = stage.timer//60
                stage.timer = 0

    # Updating Position of crosshair on basis of Mouse Cursor Position on Game Screen.
    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        

# Class for Creating Ball Objects
class Ball(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.x = pos_x 
        self.y = pos_y
        
        # Creating a list of colors for randomly coloring the ball
        ball_colors = ('blue','red')

        # Loading Ball Image of respective color
        self.image = pygame.image.load(f'assets/ball_{random.choice(ball_colors)}.png')

        # Ball image dimension (height and width)
        imageWidth = self.image.get_width()
        imageHeight = self.image.get_height()
        
        # List of Numbers from 0 to 9 to be pick at random.
        numbers = [0,1,2,3,4,5,6,7,8,9]
        self.selected_num = random.choice(numbers)
        
        # Loading Selected Number Image
        self.numberImg = pygame.image.load(f'assets/number_{self.selected_num}.png')

        # Number Image Dimension (height and width)
        numberImgWidth = self.numberImg.get_width()
        numberImgHeight = self.numberImg.get_height()

        # Checking if selected Number is Even or Odd
        # Divide the selected number by two, if remainder is 0 than it is even else odd.
        self.is_even = self.selected_num % 2 == 0

        # Draw Number Image on Top of Ball Image
        self.image.blit(self.numberImg, (int((imageWidth/2) - (numberImgWidth/2)), int((imageHeight/2) - (numberImgHeight/2))))
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)

        # Ball Speed
        self.speed_x = random.randint(1,4)
        self.speed_y = random.randint(1,4)

    # Updating Position of Ball on Game Screen and bounce on colliding with Screen Edges.
    def update(self):
        # If Ball is on left or right margin, bounce it back by changing direction. 
        if (self.rect.left <= (self.rect.w/2)/2 or self.rect.right >= screenWidth):
            self.speed_x *= -1

        # If Ball is on bottom or top margin, bounce it back by changing y direction.
        if (self.rect.top <= (self.rect.h/2)/2 or self.rect.bottom >= screenHeight):
            self.speed_y *= -1

        # Changing x and y point of Ball for moving the ball on Game Screen.
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

# Class for managing screens
class Stage():
    def __init__(self):
        self.currentScreen = "Main Menu"
        self.timer = 0
        self.lastTimer = 0

        self.totalBalls = 0
        self.totalEvenBalls = 0
        self.ball_group = []

        self.buttons = ["assets/button_grey.png", "assets/button_yellow.png"]

        self.font = pygame.font.Font("assets/KenneyFutureNarrow.ttf", 20)
        self.font_two = pygame.font.Font("assets/KenneyFutureNarrow.ttf", 40)
        self.title = UI_Element(int(screenWidth/2), 50, ["assets/title.png"], "", "title")
        self.playButton = UI_Element(int(screenWidth/2 - 100), int(screenHeight/2), self.buttons, "PLAY", "button")
        self.exitButton = UI_Element(int(screenWidth/2 + 100), int(screenHeight/2), self.buttons, "EXIT", "button")
        self.replayButton =  UI_Element(int(screenWidth/2 - 100), int(screenHeight/2), self.buttons, "REPLAY", "button")
        
        self.ui_group = pygame.sprite.Group()
        self.ui_group.add(self.title)
        self.ui_group.add(self.playButton) 
        self.ui_group.add(self.exitButton)

    def createBall(self):
        # Resetting Ball Counts
        self.totalBalls = 0
        self.totalEvenBalls = 0
        
        # Ball Sprite Group
        self.ball_group = pygame.sprite.Group()

        # Creating and adding balls in ball group.
        for i in range(80):
            self.ball_group.add(Ball(random.randrange(64, screenWidth-64), random.randrange(64, screenHeight-64)))

        # Finding total number of even ball and assign it to totalEvenBalls.
        for ball in self.ball_group:
            self.totalBalls += 1
            if ball.is_even:
                self.totalEvenBalls += 1

    def crossHairRender(self):
        # Drawing and updating Crosshair and its position on screen.
        crosshair_group.draw(screen)
        crosshair_group.update()

    def ballRender(self):
        # Drawing and updating Ball and its position on screen.
        self.ball_group.draw(screen)
        self.ball_group.update()

    def commonEvents(self, btnPressed):
        # Checking Events
        for event in pygame.event.get():
        
            # Checking if close button is pressed or not, if pressed then quit the game.
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Checking mousebutton is clicked or not.
            if event.type == pygame.MOUSEBUTTONDOWN:
                btnPressed()

    def menuScreen(self, type):
        self.commonEvents(crosshair.gameUI)
        pygame.mixer.music.stop()
        
        if type == "Main Menu":
            if self.ui_group.sprites()[1].label != "PLAY":
                self.ui_group = pygame.sprite.Group()
                self.ui_group.add(self.title)
                self.ui_group.add(self.playButton)
                self.ui_group.add(self.exitButton)

        elif type == "Game Over":
            won = self.font_two.render(f"Bravo! You Did It. You Take {self.lastTimer} seconds.", True, (255,255,255))
            screen.blit(won, (int(screenWidth/2 - won.get_width()/2), int(screenHeight/4)))
            if self.ui_group.sprites()[1].label != "REPLAY":
                self.ui_group = pygame.sprite.Group()
                self.ui_group.add(self.title)
                self.ui_group.add(self.replayButton)
                self.ui_group.add(self.exitButton)
        
        self.ui_group.draw(screen)
        self.ui_group.update()
        self.crossHairRender()    

    def gameScreen(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

        self.commonEvents(crosshair.shoot)
        timer = self.timer // 60
        self.timerText = self.font.render(f"TIMER: {timer}", True, (255,255,255))
        self.ballRender()
        screen.blit(self.timerText, (10,10))
        self.crossHairRender()
        self.timer += 1

    def screenManager(self):
        if self.currentScreen == "Game Over":
            self.menuScreen("Game Over")
        elif self.currentScreen == "Game Screen":
            self.gameScreen()
        else:
            self.menuScreen("Main Menu")

## Game Setup
# Initializing PyGame Module
pygame.init()

# Clock for controlling game speed.
clock = pygame.time.Clock()

# Screen Dimension Related Variables.
screenWidth  =  1360 #1200
screenHeight =  700 #600

# Game Window
screen = pygame.display.set_mode((screenWidth, screenHeight))

# Game Window Title
pygame.display.set_caption("Shoot 'Em")

# Making Mouse Pointer Invisible in Game.
pygame.mouse.set_visible(False)

# Background Tiles Sprite Group
tile_group = pygame.sprite.Group()

# Calculating Total number of Rows & Columns for Tiles
tile_row = math.ceil(screenWidth/64)
tile_col = math.ceil(screenHeight/64)

# Creating Tiles
for row in range(tile_row):
    for col in range(tile_col):
        tile_group.add(Tile(row*64, col*64, 'assets/background_brown.png'))

#Crosshair Mouse Pointer
crosshair = Crosshair('assets/crosshair.png')
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

pygame.mixer.music.load("assets/backMusic.mp3")

stage = Stage()

## Game Loop
while True:
    # Drawing Background using Tiles  
    tile_group.draw(screen)

    # screen management
    stage.screenManager()

    # updating all graphics on screen.
    pygame.display.flip()

    # Controlling Game Speed. The Number under bracket define FPS (Frame Rate per Second), higher the number faster the game will be and vice versa. 60 is a standard FPS for games.
    clock.tick(60)
