import pygame
import random

Screen_Width = 800
Screen_Height = 800
Screen_Title = "Space Shooter Pygame" #Sets name on gamewindow 
White_Colour = (255,255,255) #colours set according to RGB - R 255 G 255  B 255
Black_Colour = (0,0,0)
Red_Colour = (255,0,0)
Green_Colour = (0,255,0)
Blue_Colour = (0,0,255)
Clock = pygame.time.Clock()


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
    
    def Move(self, X_direction, Y_direction, Max_Height, Max_Width):
        if Y_direction > 0:
            self.Y_pos = self.Y_pos - self.Speed 
        elif Y_direction < 0:
            self.Y_pos = self.Y_pos + self.Speed
        elif X_direction > 0:
            self.X_pos = self.X_pos - self.Speed
        elif X_direction < 0:
            self.X_pos = self.X_pos + self.Speed
        
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
    def __init__ (self, image_path, X_pos, Y_pos, Width, Height):
       GameObject.__init__(self, image_path, X_pos, Y_pos, Width, Height)
    
    def Move(self, TargetX_Pos, TargetY_pos, game_screen): #moves non-player in the direction of the player's current location on the X axis 
        self.Speed = 5 #reset Speed movement back to 5
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
         

    def Panic(self, Danger, DangerX_pos, game_screen): #causes non-player character to move at a faster pace away from player's lazer to try and escape danger 
        self.Speed = 7 #boosts movement speed 
        DangerX_pos = DangerX_pos - 37 #Calibrates lazer Xpos to check with the center of the ship
        if Danger == True:
            if self.X_pos >= DangerX_pos: #Checks if enemy ship is to the right side of the Lazer and moves the ship right if it is 
                self.Speed = abs(self.Speed)
                self.X_pos += self.Speed  
                if self.X_pos >= game_screen - 80: 
                    self.Speed = -abs(self.Speed)
                    self.X_pos += self.Speed  
            
            elif self.X_pos <= DangerX_pos: #Checks if enemy ship is to the left side of the Lazer and moves the ship right if it is 
                self.Speed = -abs(self.Speed)
                self.X_pos += self.Speed  
                if self.X_pos <= 5:
                    self.Speed = abs(self.Speed)
                    self.X_pos += self.Speed  
            #self.X_pos += self.Speed  
     

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
        draw = pygame.draw.rect(Game_Screen, self.colour, [self.X_pos,self.Y_pos,self.TotalBlocks,25]) #sets surface, colour and X-pos,Y-pos+size for the bar to be drawn.

"""
class Stars:
    def __init__(self, TotalStars):
        self.TotalStars = TotalStars
        self.StarListX_pos = random.sample(range(1, 800), TotalStars)
        self.StarListY_pos = random.sample(range(1, 800), TotalStars)

    def Draw (self, X_Pos, Y_Pos, Game_Screen):
        for i in range (self.TotalStars):
            counter = 0
            pygame.draw.circle(Game_Screen, Green_Colour, (self.StarListX_pos[counter],self.StarListY_pos[counter]), 2)
            counter + 1
"""

        
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
        Y_direction = 0
        X_direction = 0
        LazerCount = 0
        FireLazar = False
        EnemyLazar = True
        Blocks = 4 #Sets the number of hits the ships can take before it's game over
        EnemyHit = False #used to detect if the enemy ship is hit
        PlayerHit = False #used to detect if the player ship is hit
        
        TotalStars = 50 #  - USED TO Create randomly generated night sky
        StarListX_pos = random.sample(range(1, 800), TotalStars+100) #  - USED TO Create randomly generated night sky
        StarListY_pos = random.sample(range(1, 800), TotalStars+100) #  - USED TO Create randomly generated night sky
        StarCounter = 0 #  - USED TO Create randomly generated night sky
        
    
        FireOkay = True
        Player1 = PlayerCharacter("ship.png", 660,600,75,75) #creates player 1 ship character 
        Enemy = NonPlayerCharacter("enemy.png",160,200,75,75)
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
        #StarsInSky = Stars(50)
        Danger = False
        Random_Mistake = random.randint(1,10) #Determines if the AI will make a mistake 
        
        

        while Is_Game_Over == False: #game loop checks if the game is over and will repeat until the condition is met and the game over state is set to True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Is_Game_Over = True
                elif event.type == pygame.KEYDOWN: #Checks when the up or down key is pressed by the user 
                    if event.key == pygame.K_UP:
                        Y_direction = 1
                    elif event.key == pygame.K_DOWN:
                        Y_direction = -1 
                    elif event.key == pygame.K_LEFT:
                        X_direction = 1
                    elif event.key == pygame.K_RIGHT:
                        X_direction = -1
                elif event.type == pygame.KEYUP: #Checks when the key is released 
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        Y_direction = 0
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        X_direction = 0
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        if FireLazar == False:
                            FireLazar = True
                            Lazer.Y_pos = Player1.Y_pos
                            Lazer.X_pos = Player1.X_pos + 32
              

                print(event)
            self.Game_Screen.fill(Black_Colour)
            Enemy.Draw (self.Game_Screen) 
            
            #continue here - Create randomly generated stars 
            pygame.draw.circle(self.Game_Screen, Green_Colour, (StarListX_pos[StarCounter],StarListY_pos[StarCounter]), 2)
                

                

            if FireLazar == True:
                if Lazer.X_pos >= Enemy.X_pos - 65 and Lazer.X_pos <= Enemy.X_pos + 140 and Lazer.Y_pos >= Enemy.Y_pos: 
                    if Random_Mistake >= 4:
                        Danger = True
                        Enemy.Panic(Danger,Lazer.X_pos, Screen_Width)
                    if Random_Mistake <= 4: #Sets Enemy AI's ability to make a random mistake and give the player an oppertunity to hit them (Value needs to be between 1 and 10. 2 = Hard and 9 = Easy )
                        Danger = False
                        Enemy.Move(Player1.X_pos, Player1.Y_pos, Screen_Width)
                elif Lazer.X_pos <= Enemy.X_pos - 75 and Lazer.X_pos >= Enemy.X_pos + 150:
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
            Player1.Move(X_direction, Y_direction, Screen_Height, Screen_Width)
            Player1.Draw (self.Game_Screen)
            if FireLazar == True:
                Lazer.Fire(FireLazar,"Up",Screen_Height, self.Game_Screen)
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
            if Lazer.Y_pos <= 2:  
                FireLazar = False

        
            if LazerCount == 1: #detects if lazer fire was queued by the AI due to the player being in range
                EnemyLazar = True #sets coditions to True for enemy lazer fire
                if EnemyLazar == True : 
                    Enemy_Lazer.Fire(EnemyLazar,"Down",Screen_Height, self.Game_Screen)
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