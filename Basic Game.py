import pygame
import random

Screen_Width = 800
Screen_Height = 800
Screen_Title = "Space Lander Pygame" #Sets name on gamewindow 
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
    
    def Move(self, Y_direction, X_direction, Max_Height, Max_Width):
        if Y_direction > 0:
            self.Y_pos = self.Y_pos - self.Speed 
        elif Y_direction < 0:
            self.Y_pos = self.Y_pos + self.Speed
        elif X_direction > 0:
            self.X_pos = self.X_pos - self.Speed
        elif X_direction < 0:
            self.X_pos = self.X_pos + self.Speed
        
        if self.Y_pos >= Max_Height - 80:
            self.Y_pos = Max_Height - 80
        if self.Y_pos <= 5:
            self.Y_pos = 5
        if self.X_pos >= Max_Width - 80:
            self.X_pos = Max_Width - 80
        if self.X_pos <= 5:
            self.X_pos = 5

class NonPlayerCharacter(GameObject):
    
    Speed = 5 
    def __init__ (self, image_path, X_pos, Y_pos, Width, Height):
       GameObject.__init__(self, image_path, X_pos, Y_pos, Width, Height)
    
    def Move(self, game_screen): #moves non-player character from left to right based on the size of the game screen
        if self.X_pos <= 10:
            self.Speed = abs(self.Speed)
        elif self.X_pos >= game_screen - 80:
            self.Speed = -abs(self.Speed)
        self.X_pos += self.Speed  


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
        Player1 = PlayerCharacter("ship.png", 360,700,75,75) #creates player 1 ship character 
        Enemy = NonPlayerCharacter("enemy.png",360,200,75,75)

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

                print(event)
            self.Game_Screen.fill(Black_Colour)
            Enemy.Draw (self.Game_Screen) 
            Enemy.Move(Screen_Width)
            Player1.Move(Y_direction, X_direction, Screen_Height, Screen_Width)
            Player1.Draw (self.Game_Screen)
         

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