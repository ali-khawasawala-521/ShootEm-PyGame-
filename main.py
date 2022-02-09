'''
Author: Ali Asgar Khawasawala
Description: A Simple yet Educational Ball Shooting Game for testing the knowledge of Number System.
'''

import sys # Provide System related functionality.
import random # Provide Functionality for Randomness.
import math # Provide Essential Math Funtionality.
import pygame # Provide Game Related Functions.


# Class for creating Background Tiles.
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, picture_path):
        super().__init__() # Initializing Base Class
        self.image = pygame.image.load(picture_path) # Loading Image
        self.rect = self.image.get_rect() # Creating Rect Object
        self.rect.topleft = (pos_x, pos_y) # Positioning Rect Object


# Class for UI Elements
class UI_Element(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, imgPath, type):
        super().__init__()
        self.x = pos_x
        self.y = pos_y
        self.type = type
        self.image = pygame.image.load(imgPath)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

# Class for Head over Display
class HUD():
    pass


# Class for creating Crosshair like Mouse Pointer.
class Crosshair(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__() # Initializing Base Class
        self.image = pygame.image.load(picture_path) # Loading Image 
        self.rect = self.image.get_rect() # Creating Rect Object
    
    # Defining what to do if crosshair collide with ball and shoot.
    def shoot(self):
        global totalEvenBalls # Global Variable for Tracking total number of even balls.

        # Checking whether crosshair is on ball while shooting.
        ball = pygame.sprite.spritecollide(crosshair, ball_group, False)
        
        # Checking if ball is even or odd.
        if ball and ball[0].is_even:
            totalEvenBalls -= 1
            ball_group.remove(ball[0])
    
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
        self.current_screen = "Game"
        self.totalBalls = 0
        self.totalEvenBalls = 0
        self.ball_group = []
    
    def createBall(self):
        # Resetting Ball Counts
        self.totalBalls = 0
        self.totalEvenBalls = 0
        
        # Ball Sprite Group
        self.ball_group = pygame.sprite.Group()

        # Creating and adding balls in ball group.
        for i in range(20):
            self.ball_group.add(Ball(random.randrange(64, screenWidth-64), random.randrange(64, screenHeight-64)))

        # Finding total number of even ball and assign it to totalEvenBalls.
        for ball in self.ball_group:
            self.totalBalls += 1
            if ball.is_even:
                self.totalEvenBalls += 1

        # Drawing and Updating Balls and its position on screen. 
        self.ball_group.draw(screen)
        self.ball_group.update()





## Game Setup
# Initializing PyGame Module
pygame.init()

# Clock for controlling game speed.
clock = pygame.time.Clock()

# Screen Dimension Related Variables.
screenWidth  =  1200
screenHeight =  600

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

# Variable for tracking total number of Even Balls.
totalEvenBalls = 0



## Game Loop
while True:
    # Checking Events
    for event in pygame.event.get():
    
        # Checking if close button is pressed or not, if pressed then quit the game.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # Checking mousebutton is clicked or not.
        if event.type == pygame.MOUSEBUTTONDOWN:
            crosshair.shoot()

    # Drawing Background using Tiles  
    tile_group.draw(screen)

    # Drawing and updating Crosshair and its position on screen.
    crosshair_group.draw(screen)
    crosshair_group.update()

    # updating all graphics on screen.
    pygame.display.flip()

    # Controlling Game Speed. The Number under bracket define FPS (Frame Rate per Second), higher the number faster the game will be and vice versa. 60 is a standard FPS for games.
    clock.tick(60)
