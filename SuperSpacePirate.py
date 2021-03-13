"""
This Game was originally created as part of a homework assignment for "importing modules" on pirple.com 

Make sure you install python3.6 with the "Add python 3.6 to PATH" option selected. This means that python, and pip will work for you from the command line.
PLEASE INSTALL PYGAME in your python scripts folder using "pip install" before running!
There is documentation with python for the "windows installation steps"

to do so please follow these instructions:
1. Start by opening a command line. You can do this by pressing the windows key and then typing cmd and then pressing enter.
2. Put in the following code into the command line:

py -m pip install -U pygame==1.9.6 --user

3. If it succeeds, make sure to restart any IDLE windows you have open before running this game.

"""
#TO DO LIST:
# 1 - Create a 3rd Enemy state where the enemy attempts to move away from the player
# 2 - Use the 3rd state to attempt to trick the player into flying into enemy fire 

import pygame
import random
import math
import os

Screen_Width = 800
Screen_Height = 800
Screen_Title = "Super Space Pirate" #Sets name on gamewindow 
White_Colour = (255,255,255) #colours set according to RGB - R 255 G 255  B 255
Black_Colour = (0,0,0)
Red_Colour = (255,0,0)
Green_Colour = (0,255,0)
Blue_Colour = (0,0,255)
Grey_Colour = (100,100,100)
LightGrey_Colour = (200,200,200)
ship_Width = 75
ship_Height = 75
Clock = pygame.time.Clock()

TotalStars = 250 #  - USED TO Create randomly generated night sky
StarListX_pos = random.sample(range(1, 800), TotalStars ) #  - USED TO Create randomly generated night sky
StarListY_pos = random.sample(range(1, 800), TotalStars ) #  - USED TO Create randomly generated night sky
StarListSpeed = [] #used to generate speed for stars that seem closer
FarStarListSpeed = []
StarListBool = [] #list used to determine if a star is near or far
for i in range(len(StarListY_pos)): #generates bool values for the star list
    RandomBool = random.randint(0,1)
    if RandomBool == 1:
        StarListBool.append(True)
    elif RandomBool == 0:
        StarListBool.append(False)

for i in range(len(StarListY_pos)): #generates an int values for the star list
    RandomSpeed = random.randint(4,6)
    StarListSpeed.append(RandomSpeed)
for i in range(len(StarListY_pos)): #generates an int values for the star list
    RandomSpeed = random.randint(1,3)
    FarStarListSpeed.append(RandomSpeed)
   



class GameObject: #class for defining game objects that will be drawn onto the game screen and moved arround
    def __init__(self, image_path, X_pos, Y_pos, Width, Height):
        Object_Image = pygame.image.load(image_path) #Loads image to be set
        self.Image = pygame.transform.scale(Object_Image, (Width, Height)) #Scales the image that's been loaded in 
        self.X_pos = X_pos
        self.Y_pos = Y_pos
        self.Width = Width
        self.Height = Height
    
    def Draw (self,background): #This function is used to draw the object on the game screen
        background.blit(self.Image,(self.X_pos,self.Y_pos)) #Blit funtion is used to draw imaghes to the game screen/ surface selected along with the X and Y Pos taken in the form of a tuple 
        

class PlayerCharacter(GameObject):
    
    Speed = 10 

    def __init__ (self, image_path, X_pos, Y_pos, Width, Height):
       GameObject.__init__(self, image_path, X_pos, Y_pos, Width, Height)
    
    def Move(self, X_direction, Y_direction, Max_Height, Max_Width): #Checks input for player
        if Y_direction > 0 and X_direction == 0:
            self.Y_pos = self.Y_pos - self.Speed #used to make the Ship go up
        elif Y_direction > 0 and X_direction > 0: #Up and left combined (Combined movement devided to match regular speed)
            self.Y_pos = self.Y_pos - self.Speed /1.5
            self.X_pos = self.X_pos - self.Speed /1.5
        elif Y_direction > 0 and X_direction < 0: #Up and right combined (Combined movement devided to match regular speed)
            self.Y_pos = self.Y_pos - self.Speed /1.5
            self.X_pos = self.X_pos + self.Speed /1.5

        elif Y_direction < 0 and X_direction == 0:
            self.Y_pos = self.Y_pos + self.Speed #used to make the Ship go down
        elif Y_direction < 0 and X_direction > 0: #Down and left combined (Combined movement devided to match regular speed)
            self.Y_pos = self.Y_pos + self.Speed /1.5
            self.X_pos = self.X_pos - self.Speed /1.5
        elif Y_direction < 0 and X_direction < 0: #Down and right combined (Combined movement devided to match regular speed)
            self.Y_pos = self.Y_pos + self.Speed /1.5 
            self.X_pos = self.X_pos + self.Speed /1.5 

        elif X_direction > 0 and Y_direction == 0:
            self.X_pos = self.X_pos - self.Speed #used to make the Ship go left
        elif X_direction < 0 and Y_direction == 0:
            self.X_pos = self.X_pos + self.Speed #used to make the Ship go right 
           
        
        if self.Y_pos >= Max_Height - 120: #sets collision detection for bottom of the screen for player to make sure they don't go over the health bar or off the screen 
            self.Y_pos = Max_Height - 120
        if self.Y_pos <= 50: #sets collision detection for top of the screen for player to make sure they don't go over the health bar or off the screen 
            self.Y_pos = 50
        if self.X_pos >= Max_Width - 80:
            self.X_pos = Max_Width - 80
        if self.X_pos <= 5:
            self.X_pos = 5

   
class LazerFire(GameObject):
    Speed = 10
    
    def __init__(self, image_path, X_pos, Y_pos, Width, Height):
        GameObject.__init__(self, image_path, X_pos, Y_pos, Width, Height)   
    
    def Fire (self, Fire, Direction, Height, Game_Screen):
        if Fire == True:
            self.Draw(Game_Screen)
            if Direction == "Up":
                if self.Y_pos >= 0:
                    self.Y_pos = self.Y_pos - self.Speed
                    
            elif Direction == "Down":
                if self.Y_pos <= Height:
                    self.Y_pos = self.Y_pos + self.Speed
                    
    
    def Damage (self, enemy_X_Pos, enemy_Y_Pos): #Colision detection for Lazer on Enemy ship
        if enemy_X_Pos - 5 < self.X_pos and enemy_X_Pos + 75 > self.X_pos and enemy_Y_Pos - 50 < self.Y_pos and enemy_Y_Pos + 50 > self.Y_pos:
            return True
        else:
            return False
        
       
class NonPlayerCharacter(GameObject):
    
    #Speed = random.randint(5, 7) #program AI to change speed at random when fired at
    Speed = 5
    Stop = 0
    Away_From_Border = 150 #used to check if enemy ship is away from the border to help clear it from moving into the border
    def __init__ (self, image_path, X_pos, Y_pos, Width, Height):
       GameObject.__init__(self, image_path, X_pos, Y_pos, Width, Height)
    
    def Move(self, TargetX_Pos, TargetY_pos, game_screen): #moves non-player in the direction of the player's current location on the X axis 
        self.Speed = 4 #reset Speed movement back 
        if self.X_pos <=  TargetX_Pos - 10:
            self.Speed = abs(self.Speed)
            self.X_pos += self.Speed #moves ship right if it's not in line
            if self.X_pos >= TargetX_Pos -10:
                self.X_pos += self.Stop #stops ship once it's lined up

        elif self.X_pos >= TargetX_Pos + 10: 
            self.Speed = -abs(self.Speed)
            self.X_pos += self.Speed #moves ship left if it's not in line
            if self.X_pos >= TargetX_Pos +10: 
                self.X_pos += self.Stop #stops ship once it's lined up
         
    def LurePlayer (self,NewMoveX_pos,NewMoveY_pos): #creat a function to make the AI lure the player to attempt to attack it
        pass



    def Panic(self, Danger, DangerX_pos, game_screen): #causes non-player character to move at a faster pace away from player's lazer to try and escape danger 
        self.Speed = 6 #boosts movement speed when it panic mode
        DangerX_pos = DangerX_pos - 35 #Calibrates lazer Xpos to check with the center of the ship

        if Danger == True and self.X_pos <= DangerX_pos: #Checks if enemy ship is to the left side of the Lazer and moves the ship right if it is 
            if self.X_pos <= self.Away_From_Border and DangerX_pos < self.Away_From_Border:
                self.Speed = abs(self.Speed)
                self.X_pos += self.Speed
            else:
                self.Speed = -abs(self.Speed)
                self.X_pos += self.Speed 
        
        elif Danger == True and self.X_pos >= DangerX_pos: #Checks if enemy ship is to the right side of the Lazer and moves the ship right if it is 
            if self.X_pos > game_screen - self.Away_From_Border and DangerX_pos > game_screen - self.Away_From_Border: 
                self.Speed = -abs(self.Speed)
                self.X_pos += self.Speed
            elif self.X_pos < game_screen - self.Away_From_Border: 
                self.Speed = abs(self.Speed)
                self.X_pos += self.Speed
            
        
     

class HealthBar:
    FullColour = 255
    Chunks = 100
    Final_shot = 25
    def __init__ (self, X_pos, Y_pos, TotalBlocks):
        self.DamageTaken = 0
        self.TotalBlocks = self.Final_shot + TotalBlocks * self.Chunks #Total lenght the bar will be drawn in the X axis. (Final_shot is used for the size of the final health bar size, Total blocks determines the number of hits the ship can take, Chunks determins the size of the bar proportunate to the Blocks)
        self.X_pos = X_pos
        self.Y_pos = Y_pos
        self.colour = (0,self.FullColour,self.FullColour) #Sets colour of "full health" health bar

    def ColourAdjust (self, TotalBlocks): #Changes colour of the enemy health bar from an initial light blue to green after being hit, and then gradually from green to red based on the number of hits and health left
            ColourReduction = self.FullColour / TotalBlocks #determines the percetentage of the colour to be reduced according to the number of blocks selected
            green = self.FullColour - ColourReduction * self.DamageTaken #Used to calculate by how much green will be reduced on the RGB scale
            red = ColourReduction * self.DamageTaken #Determines how much red will be added on the RGB scale 
            self.colour = (red,green,0)
     
    def Draw (self, Game_Screen):
        pygame.draw.rect(Game_Screen, self.colour, [self.X_pos,self.Y_pos,self.TotalBlocks,25]) #sets surface, colour and X-pos,Y-pos+size for the bar to be drawn.

class LazarBar:
    Length = 120 
    def __init__ (self ,X_pos ,Y_pos ,CurrentLazarY_pos, EndPos, Colour):
        self.X_pos = X_pos
        self.Y_pos = Y_pos
        self.EndPos = EndPos
        self.colour = Colour
        self.Chunks = self.EndPos / CurrentLazarY_pos
        self.StartPos = CurrentLazarY_pos
        
        
    def EnemyDraw (self, CurrentLazerY_pos ,Game_Screen):
        EnemyTotalLength = CurrentLazerY_pos / self.EndPos * self.Length 
        pygame.draw.rect(Game_Screen, self.colour, [self.X_pos,self.Y_pos,EnemyTotalLength,25])

    def PlayerDraw (self, CurrentLazerY_pos ,Game_Screen):
        TotalLength = CurrentLazerY_pos / self.StartPos * self.Length
        self.PlayerTotalLength = self.Length - TotalLength
        pygame.draw.rect(Game_Screen, self.colour, [self.X_pos,self.Y_pos,self.PlayerTotalLength,25])
        
class Game:
    Tick_Rate = 60 #Change to set framerate
    
    def __init__ (self, title, width, height):
        self.title = title
        self.width = width
        self.height = height 
        self.Game_Screen = pygame.display.set_mode((width, height)) #Creates the window being displayed 
        self.Game_Screen.fill(Black_Colour) #Sets the default colour of the displayed window 
        pygame.display.set_caption(title)
    
    
    def run_game_loop (self):
        Is_Game_Over = False
        PlayerWon = False
        CPUWon = False
        Menu = True
        altMenu = 0
        Fight = False
        Y_direction = 0
        X_direction = 0
        LazerCount = 0
        FireLazar = False
        EnemyLazar = False
        Blocks = 4 #Sets the number of hits the ships can take before it's game over
        EnemyHit = False #used to detect if the enemy ship is hit
        PlayerHit = False #used to detect if the player ship is hit
        EnemyLazarStatusPNG = "EnemyLazerReadyStatus.png"
        Danger = False
        Random_Mistake = random.randint(1,10) #Determines if the AI will make a mistake 
    
    
        FireOkay = True
        Player1 = PlayerCharacter("ship.png", 660,600,ship_Width,ship_Height) #creates player 1 ship character 
        Enemy = NonPlayerCharacter("enemy.png",160,200,ship_Width,ship_Height)
        Lazer = LazerFire("Lazer.png",Player1.X_pos, Player1.Y_pos,10,60)
        Enemy_Lazer = LazerFire("Lazer2.png",Enemy.X_pos +35, Enemy.Y_pos,10,60)
        Explode = LazerFire ("boom.png",Enemy.X_pos -15, Enemy.Y_pos,75,75)
        Enemy_Health = HealthBar(10,0,Blocks)
        EnemyHealthBorder = NonPlayerCharacter("EnemyHealthBorder.png",0,0,180,55 ) 
        EnemyHealthCorner = NonPlayerCharacter("EnemyBorderCorner.png",Blocks * Enemy_Health.Chunks - 40,-10,80,40 )
        Player1_Health = HealthBar(470,770,Blocks)
        Player1_Health.X_pos = Screen_Width - Blocks * Player1_Health.Chunks #sets initial starting postion of player healthbar so it's adjusted according to the number of blocks selected and the size of the chunks selected
        PlayerHealthBorder = NonPlayerCharacter("PlayerHealthBorder.png",620,740,180,55 ) 
        PlayerHealthCorner = NonPlayerCharacter("PlayerBorderCorner.png",Screen_Width - Blocks * Player1_Health.Chunks - 6 ,765,80,40 )
        EnemyLazarHud = NonPlayerCharacter("EnemyLazerHud.png",EnemyHealthCorner.X_pos + 100, EnemyHealthBorder.Y_pos, 140,30)
        EnemyLazarStatus = NonPlayerCharacter(EnemyLazarStatusPNG,EnemyLazarHud.X_pos + 150, EnemyHealthBorder.Y_pos, 120,30)
        EnemyCharge = LazarBar(EnemyLazarHud.X_pos + 150 ,EnemyHealthBorder.Y_pos ,Enemy_Lazer.X_pos, 730, Red_Colour)
        PlayerLazarHud = NonPlayerCharacter("PlayerLazerHud.png",PlayerHealthCorner.X_pos - 290, PlayerHealthBorder.Y_pos + 25, 140,30)
        PlayerLazarStatus = NonPlayerCharacter("PlayerLazerReadyStatus.png",PlayerLazarHud.X_pos + 150, PlayerLazarHud.Y_pos, 120,30)
        PlayerCharge = LazarBar(PlayerLazarHud.X_pos + 150, PlayerLazarHud.Y_pos ,Lazer.X_pos, 2, Blue_Colour)
        GameOverScreen = NonPlayerCharacter("GameOver.png", 100, 300, 600, 200)
        WinScreen = NonPlayerCharacter("win.png", 100, 300, 600, 200)
        Logo = NonPlayerCharacter("Logo.png", 0, 0, 800, 800)
        EndGame = NonPlayerCharacter("Quit.png", 300, 750, 200, 20)
        ControlMenu = NonPlayerCharacter("ControlMenu.png", 225, 680, 350, 20 )
        RuturnToMainMenu = NonPlayerCharacter("ReturnMain.png", 100, 680, 625, 20)
        ControlList = NonPlayerCharacter("controls.png", 55, 220, 695, 200)
        
        
        

        while Is_Game_Over == False: #game loop checks if the game is over and will repeat until the condition is met and the game over state is set to True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Is_Game_Over = True
                
                keys = pygame.key.get_pressed()

                if keys[pygame.K_UP] == True: #Checks for Up arrow key
                    Y_direction = 1
                    if keys[pygame.K_UP] == True and keys[pygame.K_LEFT] == True: #Checks for combined Up and Left arrow key 
                        Y_direction = 1
                        X_direction = 1
                    elif keys[pygame.K_UP] == True and keys[pygame.K_RIGHT] == True: #Checks for combined Up and Right arrow key 
                        Y_direction = 1
                        X_direction = -1
                elif keys[pygame.K_DOWN] == True: #Checks for Down arrow key
                    Y_direction = -1
                    if keys[pygame.K_DOWN] == True and keys[pygame.K_LEFT] == True: #Checks for combined Down and Left arrow key 
                        Y_direction = -1
                        X_direction = 1
                    elif keys[pygame.K_DOWN] == True and keys[pygame.K_RIGHT] == True: #Checks for combined Down and Right arrow key 
                        Y_direction = -1
                        X_direction = -1
                elif keys[pygame.K_RIGHT] == True: #Checks for Right arrow key
                    X_direction = -1
                elif keys[pygame.K_LEFT] == True: #Checks for Left arrow key
                    X_direction = 1

                #reduces direction to 0 after keys are released        
                elif keys[pygame.K_UP] == False or keys[pygame.K_LEFT] == False or keys[pygame.K_RIGHT] == False or keys[pygame.K_DOWN]:
                    Y_direction = 0
                    X_direction = 0
                
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP: #Checks for space bar being pressed to fire lazer 
                    if event.key == pygame.K_SPACE:
                        if FireLazar == False:
                            FireLazar = True
                            Lazer.Y_pos = Player1.Y_pos
                            Lazer.X_pos = Player1.X_pos + 32

            def particles(Hit, lazerX, lazerY, lazerMovement, shipY, shipX): #funtion for testing particles 
                lazerX = int(lazerX)
                lazerY = int(lazerY)
                shipX = int(shipX)
                shipY = int(shipY)
                shipHit = True  
                HitCount = 0
                if Hit == True:
                    HitCount += 1
                particleFade =(255,255,0) #RGB 
                numberOfParticles = 10
                particlesStartX_pos = []
                particlesStartY_pos = []
                particlesEndX_pos = []
                particlesEndY_pos = []
                particlesSpeed = []
                if lazerMovement == "Up" and HitCount == 0: #up keeps refreshing lists, rework so it only updates on impact
                    for i in range (numberOfParticles):
                        randomSpeed = random.randint(6,10)
                        particlesSpeed.append(randomSpeed)
                        particlesStartY_pos.append(int(shipX))
                        particlesStartX_pos.append(int(shipY))
                        destinationX_pos = random.randint(0, Screen_Width)
                        destinationY_pos = random.randint(lazerY, lazerY + 300)
                        particlesEndY_pos.append(int(destinationY_pos))
                        particlesEndX_pos.append(int(destinationX_pos)) 
                elif lazerMovement == "Up" and HitCount > 0:    
                    for i in range (len(particlesEndY_pos)):
                        pygame.draw.circle(self.Game_Screen, particleFade, (particlesStartX_pos[i - 1],particlesStartY_pos[i - 1]), 1)
                        if particlesStartY_pos[i - 1] < particlesEndY_pos[i - 1]:
                            particlesStartY_pos[i - 1] = particlesStartY_pos[i - 1] + particlesSpeed[i - 1]
                elif lazerMovement == "Down":
                    pass #to be added after tests 

                
               

                        






            def StarGenerator(PlayerY_direction, PlayerX_direction): #create funtion to generate and move stars based on player movement 
                for i in range (len(StarListX_pos)): #used to generate stars based on the number selected 
                    if StarListBool[i -1] == True:
                        Nearfickercolour = random.randint(120,180) #used to make the stars flicker brighter to make them seem closer
                        Nearflickerstar = (Nearfickercolour,Nearfickercolour,Nearfickercolour) #sets new colour for the specified star in the loop
                        pygame.draw.circle(self.Game_Screen, Nearflickerstar, (StarListX_pos[i - 1],StarListY_pos[i - 1]), 1)
                    elif StarListBool[i -1] == False:
                        Farfickercolour = random.randint(50,100) #used to make the stars flicker more dim to make them seem far
                        Farflickerstar = (Farfickercolour,Farfickercolour,Farfickercolour) #sets new colour for the specified star in the loop
                        pygame.draw.circle(self.Game_Screen, Farflickerstar, (StarListX_pos[i - 1],StarListY_pos[i - 1]), 1)
                    if Clock.tick() == 1:
                        for i in range (len(StarListX_pos)):
                            if StarListBool[i] == True:
                                if PlayerY_direction == 1: #Checks for Up movement from player to make the stars move down 
                                    StarListY_pos[i] = StarListY_pos[i] + StarListSpeed[i]
                                    if PlayerY_direction == 1 and PlayerX_direction == 1:
                                        StarListY_pos[i] = StarListY_pos[i] + math.floor(StarListSpeed[i] /2)
                                        StarListX_pos[i] = StarListX_pos[i] + math.floor(StarListSpeed[i] /2)
                                    elif PlayerY_direction == 1 and PlayerX_direction == -1:
                                        StarListY_pos[i] = StarListY_pos[i] + math.floor(StarListSpeed[i] /2)
                                        StarListX_pos[i] = StarListX_pos[i] - math.floor(StarListSpeed[i] /2)
                                elif PlayerY_direction == -1: #Checks for Up movement from player to make the stars move down 
                                    StarListY_pos[i] = StarListY_pos[i] - StarListSpeed[i]
                                    if PlayerY_direction == -1 and PlayerX_direction == 1:
                                        StarListY_pos[i] = StarListY_pos[i] - math.floor(StarListSpeed[i] /2)
                                        StarListX_pos[i] = StarListX_pos[i] + math.floor(StarListSpeed[i] /2)
                                    elif PlayerY_direction == -1 and PlayerX_direction == -1:
                                        StarListY_pos[i] = StarListY_pos[i] - math.floor(StarListSpeed[i] /2)
                                        StarListX_pos[i] = StarListX_pos[i] - math.floor(StarListSpeed[i] /2)
                                elif PlayerX_direction == -1: #Checks for Right arrow key to make the stars move left 
                                    StarListX_pos[i] = StarListX_pos[i] - StarListSpeed[i]
                                elif PlayerX_direction == 1: #Checks for Left arrow key to make the stars move right 
                                    StarListX_pos[i] = StarListX_pos[i] + StarListSpeed[i]

                            elif StarListBool[i] == False:
                                if PlayerY_direction == 1:
                                    StarListY_pos[i] = StarListY_pos[i] + FarStarListSpeed[i]
                                    if PlayerY_direction == 1 and PlayerX_direction == 1:
                                        StarListY_pos[i] = StarListY_pos[i] + math.floor(FarStarListSpeed[i] /2)
                                        StarListX_pos[i] = StarListX_pos[i] + math.floor(FarStarListSpeed[i] /2)
                                    elif PlayerY_direction == 1 and PlayerX_direction == -1:
                                        StarListY_pos[i] = StarListY_pos[i] + math.floor(FarStarListSpeed[i] /2)
                                        StarListX_pos[i] = StarListX_pos[i] - math.floor(FarStarListSpeed[i] /2)
                                elif PlayerY_direction == -1:
                                    StarListY_pos[i] = StarListY_pos[i] - FarStarListSpeed[i]
                                    if PlayerY_direction == -1 and PlayerX_direction == 1:
                                        StarListY_pos[i] = StarListY_pos[i] - math.floor(FarStarListSpeed[i] /2)
                                        StarListX_pos[i] = StarListX_pos[i] + math.floor(FarStarListSpeed[i] /2)
                                    elif PlayerY_direction == -1 and PlayerX_direction == -1:
                                        StarListY_pos[i] = StarListY_pos[i] - math.floor(FarStarListSpeed[i] /2)
                                        StarListX_pos[i] = StarListX_pos[i] - math.floor(FarStarListSpeed[i] /2)
                                elif PlayerX_direction == -1:
                                    StarListX_pos[i] = StarListX_pos[i] - FarStarListSpeed[i]
                                elif PlayerX_direction == 1:
                                    StarListX_pos[i] = StarListX_pos[i] + FarStarListSpeed[i]
                                
                            if StarListY_pos[i] >= Screen_Height:
                                    StarListY_pos[i] = 0
                            elif StarListX_pos[i] >= Screen_Width:
                                    StarListX_pos[i] = 0
                            elif StarListX_pos[i] <= 0:
                                    StarListX_pos[i] = Screen_Height    
                            elif StarListY_pos[i] <= 0:
                                    StarListY_pos[i] = Screen_Width

            
            if Menu == True and altMenu == 0:
                self.Game_Screen.fill(Black_Colour)
                StarGenerator(0,-1) #used to make the stars move down while on the main screen
                EndGame.Draw(self.Game_Screen)
                ControlMenu.Draw(self.Game_Screen)
                                  
                Logo.Draw(self.Game_Screen) #PlaceHolder Logo for Main Menu
                if keys[pygame.K_RETURN] == True: #PlaceHolder for Start input 
                    Menu = False
                    Fight = True
                if keys[pygame.K_c] == True:
                    altMenu = 1
                if keys[pygame.K_ESCAPE] == True:
                    Is_Game_Over = True

            elif Menu == True and altMenu == 1:
                self.Game_Screen.fill(Black_Colour)
                StarGenerator(1,0) #used to make the stars move down while on the main screen
                ControlList.Draw(self.Game_Screen)
                RuturnToMainMenu.Draw(self.Game_Screen)
               
                if keys[pygame.K_BACKSPACE] == True: #PlaceHolder for Start input 
                    altMenu = 0


                


            elif Player1_Health.DamageTaken == 4: #sets the number of shots the player can take before it's game over
                CPUWon = True
                Fight = False
                
                
                self.Game_Screen.fill(Black_Colour)
                GameOverScreen.Draw(self.Game_Screen)
                pygame.display.update() #Updates the current frame after completing the loop
                if keys[pygame.K_RETURN] == True: #PlaceHolder for Start input 
                    Menu = False
                    Fight = True
                    CPUWon = False
                    self.run_game_loop()
                    
                
            elif Enemy_Health.DamageTaken == 10: #sets the number of shots the enemy can take before it's game over
                PlayerWon = True
                Fight = False  
                self.Game_Screen.fill(Black_Colour)
                WinScreen.Draw(self.Game_Screen)
                pygame.display.update() #Updates the current frame after completing the loop
                if keys[pygame.K_RETURN] == True: #PlaceHolder for Start input 
                    Menu = False
                    Fight = True
                    CPUWon = False
                    self.run_game_loop()

            elif Menu == False and Fight == True:    #print(event) - remove as comment to see current events being logged 
                self.Game_Screen.fill(Black_Colour)
                StarGenerator(Y_direction, X_direction) #Generates stars that move in the opposite direction to the player      
                
    
                Enemy.Draw (self.Game_Screen) 
                

                if FireLazar == True: #Enemy AI conditions used to check if the player has fired their lazer
                    if Lazer.X_pos >= Enemy.X_pos - 10 and Lazer.X_pos <= Enemy.X_pos + 85 and Lazer.Y_pos >= Enemy.Y_pos + 80: 
                        if Random_Mistake <= 1:
                            Danger = True
                            Enemy.Panic(Danger,Lazer.X_pos, Screen_Width)
                        elif Random_Mistake > 1: #Sets Enemy AI's ability to make a random mistake and give the player an oppertunity to hit them (Value needs to be between 1 and 10. 1 = Easy and 10 = Hard )
                            Danger = False
                            Enemy.Move(Player1.X_pos, Player1.Y_pos, Screen_Width)
                    elif Lazer.X_pos <= Enemy.X_pos - 75 or Lazer.X_pos >= Enemy.X_pos + 150:
                        Danger = False
                        Enemy.Move(Player1.X_pos, Player1.Y_pos, Screen_Width)
                else:
                    Enemy.Move( Player1.X_pos, Player1.Y_pos, Screen_Width)
                
            
                Player1_Health.Draw(self.Game_Screen)
                PlayerHealthBorder.Draw(self.Game_Screen)
                PlayerHealthCorner.Draw(self.Game_Screen)
                Enemy_Health.Draw(self.Game_Screen)
                EnemyHealthBorder.Draw(self.Game_Screen)
                EnemyHealthCorner.Draw(self.Game_Screen)
                EnemyLazarHud.Draw(self.Game_Screen)
                PlayerLazarHud.Draw(self.Game_Screen)
                
                Player1.Move(X_direction, Y_direction, Screen_Height, Screen_Width)
                Player1.Draw (self.Game_Screen)

                #Moved here for testing particles 
                particles(Lazer.Damage(Enemy.X_pos, Enemy.Y_pos), Lazer.X_pos, Lazer.Y_pos, "Up", Enemy.X_pos, Enemy.Y_pos)

                if FireLazar == True:
                    Lazer.Fire(FireLazar,"Up",Screen_Height, self.Game_Screen)    
                    PlayerCharge.PlayerDraw(Lazer.Y_pos ,self.Game_Screen)
                    if Lazer.Damage(Enemy.X_pos, Enemy.Y_pos) == True:
                        
                        Explode.Y_pos = Enemy.Y_pos
                        Explode.X_pos = Enemy.X_pos
                        Explode.Draw (self.Game_Screen)
                        
                        EnemyHit = True
                    elif EnemyHit == True and Lazer.Damage(Enemy.X_pos, Enemy.Y_pos) == False: #used to adjust the enemy health bar after being hit by the player's lazer
                        Enemy_Health.TotalBlocks = Enemy_Health.TotalBlocks - Enemy_Health.Chunks
                        Enemy_Health.DamageTaken = Enemy_Health.DamageTaken + 1 #Adjusts he colour of the health bar by incrementing the damage taken for comparison to the initial chunks 
                        if Enemy_Health.TotalBlocks > 1: #Temp argument to keep the game from crashing after the final shot is given 
                            Enemy_Health.ColourAdjust(Blocks)
                        Enemy_Health.Draw(self.Game_Screen)
                        EnemyHit = False
                if Lazer.Y_pos <= 25:  
                    FireLazar = False
                if FireLazar == False:
                    PlayerLazarStatus.Draw(self.Game_Screen)

                if EnemyLazar == False:
                    EnemyLazarStatus.Draw(self.Game_Screen)  
                if LazerCount == 1: #detects if lazer fire was queued by the AI due to the player being in range
                    EnemyLazar = True #sets coditions to True for enemy lazer fire
                    if EnemyLazar == True : 
                        Enemy_Lazer.Fire(EnemyLazar,"Down",Screen_Height, self.Game_Screen)
                        EnemyCharge.EnemyDraw(Enemy_Lazer.Y_pos ,self.Game_Screen)

                        if Enemy_Lazer.Y_pos >= 730:
                            EnemyLazar = False #removes the lazer from the screen 
                            Random_Mistake = random.randint(1,10) #Reset the Random int to give the AI a chance to mess up during their next shot. Only resets after enemy fire to avoid Enemy getting hit by "player lazer spam"
                            LazerCount = 0 #removes the queued lazer so the AI can add another
                        
                
                    if Enemy_Lazer.Damage(Player1.X_pos, Player1.Y_pos) == True: #Conditions for player taking damager by enemy ship
                        Explode.Y_pos = Player1.Y_pos
                        Explode.X_pos = Player1.X_pos
                        Explode.Draw (self.Game_Screen)
                        PlayerHit = True
                    elif PlayerHit == True and Enemy_Lazer.Damage(Player1.X_pos, Player1.Y_pos) == False: #used to adjust the enemy health bar after being hit by the player's lazer
                        Player1_Health.TotalBlocks = Player1_Health.TotalBlocks - Player1_Health.Chunks
                        Player1_Health.DamageTaken = Player1_Health.DamageTaken + 1 #Adjusts he colour of the health bar by incrementing the damage taken for comparison to the initial chunks 
                        if Player1_Health.TotalBlocks > 1: #Temp argument to keep the game from crashing after the final shot is given 
                            Player1_Health.ColourAdjust(Blocks)
                            Player1_Health.X_pos = Player1_Health.X_pos + Player1_Health.Chunks #Moves the player health bar to the right propotionately to the ammount that's been removed from it 
                        Player1_Health.Draw(self.Game_Screen)
                        PlayerHit = False

                    if Player1.X_pos >= Enemy.X_pos - 50 and Player1.X_pos <= Enemy.X_pos + 75 and Player1.Y_pos >= Enemy.Y_pos - 60 and Player1.Y_pos <= Enemy.Y_pos + 65: #Checks if the ships collide, numbers adjust to accomodate the shpe and size of the sprites
                        Explode.Y_pos = Player1.Y_pos
                        Explode.X_pos = Player1.X_pos
                        Explode.Draw (self.Game_Screen)
                        Explode.Y_pos = Enemy.Y_pos
                        Explode.X_pos = Enemy.X_pos
                        Explode.Draw (self.Game_Screen)
                        Player1_Health.TotalBlocks = Player1_Health.TotalBlocks - Player1_Health.Chunks
                        Player1_Health.DamageTaken = Player1_Health.DamageTaken + 1 #Adjusts he colour of the health bar by incrementing the damage taken for comparison to the initial chunks 
                        if Player1_Health.TotalBlocks > 1: #Temp argument to keep the game from crashing after the final shot is given 
                            Player1_Health.ColourAdjust(Blocks)
                        Player1_Health.Draw(self.Game_Screen)
                        

                elif Player1.X_pos - 35 <= Enemy.X_pos and Player1.X_pos + 25 >= Enemy.X_pos: #Used to queue lazer fire with the AI
                    Enemy_Lazer.Y_pos = Enemy.Y_pos
                    Enemy_Lazer.X_pos = Enemy.X_pos + 35
                    LazerCount = 1 #Queued lazer fire with the AI

                      
                
            

            pygame.display.update() #Updates the current frame after completing the loop
            Clock.tick(self.Tick_Rate) #Sets the frame rate per second
    


pygame.init()

new_game = Game(Screen_Title,Screen_Width,Screen_Height) #creates a new game part of the "game class"

new_game.run_game_loop() #Starts the game loop as defined in the class to continue looping until the game over state becomes true 

pygame.quit()
quit()

"""
below are some examples of how to draw shapes

pygame.draw.rect(Game_Screen, Red_Colour, [400,100,100,100]) #sets surface, colour and X-pos,Y-pos+size for the rectangle to be drawn
pygame.draw.circle(Game_Screen, Green_Colour, (400, 300), 50) #sets surface, colour and X-pos,Y-pos+size for the circle to be drawn
"""