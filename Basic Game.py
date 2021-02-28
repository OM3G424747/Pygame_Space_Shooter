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
        
        if self.Y_pos >= Max_Height - 110: #sets collision detection for top and bottom of the screen for player to make sure they don't go over the health bar or off the screen 
            self.Y_pos = Max_Height - 110
        if self.Y_pos <= 5:
            self.Y_pos = 5
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
    def __init__ (self, image_path, X_pos, Y_pos, Width, Height):
       GameObject.__init__(self, image_path, X_pos, Y_pos, Width, Height)
    
    def Move(self,game_screen): #moves non-player character from left to right based on the size of the game screen
        if self.X_pos <= 10:
            self.Speed = abs(self.Speed)
        elif self.X_pos >= game_screen - 80:
            self.Speed = -abs(self.Speed)
        self.X_pos += self.Speed  

    def Panic(self, Danger, game_screen): #moves non-player character from left to right based on the size of the game screen
        if Danger == True and self.Speed < 11:
            if self.X_pos <= 10:
                self.Speed = abs(self.Speed)
            elif self.X_pos >= game_screen - 80:
                self.Speed = -abs(self.Speed)
            self.X_pos += self.Speed + 1   

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
        Blocks = 3
        EnemyHit = False #used to detect if the enemy ship is hit
        PlayerHit = False #used to detect if the player ship is hit

        FireOkay = True
        Player1 = PlayerCharacter("ship.png", 660,600,75,75) #creates player 1 ship character 
        Enemy = NonPlayerCharacter("enemy.png",160,200,75,75)
        Lazer = LazerFire("Lazer.png",Player1.X_pos, Player1.Y_pos,10,60)
        Enemy_Lazer = LazerFire("Lazer2.png",Enemy.X_pos +35, Enemy.Y_pos,10,60)
        Explode = LazerFire ("boom.png",Enemy.X_pos -15, Enemy.Y_pos,75,75)
        Enemy_Health = HealthBar(0,0,Blocks)
        Player1_Health = HealthBar(0,770,Blocks)
        Danger = False

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
            
            if FireLazar == True:
                if Lazer.X_pos >= Enemy.X_pos - 60 and Lazer.X_pos <= Enemy.X_pos + 135 and Lazer.Y_pos >= Enemy.Y_pos:
                    Danger = True
                    Enemy.Panic(Danger, Screen_Width)
                else:
                    Danger = False
            if Danger == False:
                Enemy.Move(Screen_Width)

            else:
                Enemy.Move(Screen_Width)
            
            Player1_Health.Draw(self.Game_Screen)
            Enemy_Health.Draw(self.Game_Screen)
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