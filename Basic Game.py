import pygame

Screen_Width = 800
Screen_Height = 800
Screen_Title = "Space Flight Pygame" #Sets name on gamewindow 
White_Colour = (255,255,255) #colours set according to RGB - R 255 G 255  B 255
Black_Colour = (0,0,0)
Red_Colour = (255,0,0)
Green_Colour = (0,255,0)
Blue_Colour = (0,0,255)
Clock = pygame.time.Clock()

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
        while Is_Game_Over == False: #game loop checks if the game is over and will repeat until the condition is met and the game over state is set to True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Is_Game_Over = True
                print(event)
            pygame.display.update() #Updates the current frame after completing the loop
            Clock.tick(self.Tick_Rate) #Sets the frame rate per second
    
class GameObject: #class for defining game objects that will be drawn onto the game screen and moved arround
    def __init__(self, image_path, X_pos, Y_pos, Width, Height):
        Object_Image = pygame.image.load(image_path) #Loads image to be set
        self.Image = pygame.transform.scale(Object_Image, (Width, Height)) #Scales the image that's been loaded in 
        self.X_pos = X_pos
        self.Y_pos = Y_pos
    
    def draw (self,background):
        background.blit(self.Image,(self.X_pos,self.Y_pos)) #Blit funtion is used to draw imaghes to the game screen/ surface selected along with the X and Y Pos taken in the form of a tuple 
       
Player1 = GameObject("ship.png", 375,300,75,75) #creates player 1 ship character a




pygame.init()

new_game = Game(Screen_Title,Screen_Width,Screen_Height) #creates a new game part of the "game class"


Player1.draw (new_game.Game_Screen)

new_game.run_game_loop() #Starts the game loop as defined in the class to continue looping until the game over state becomes true 


pygame.quit()
quit()

"""
below are some examples of how to draw shapes

pygame.draw.rect(Game_Screen, Red_Colour, [400,100,100,100]) #sets surface, colour and X-pos,Y-pos+size for the rectangle to be drawn
pygame.draw.circle(Game_Screen, Green_Colour, (400, 300), 50) #sets surface, colour and X-pos,Y-pos+size for the circle to be drawn
"""