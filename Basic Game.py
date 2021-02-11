import pygame

pygame.init()

Screen_Width = 800
Screen_Height = 800
Screen_Title = "Random Game"
White_Colour = (255,255,255) #RGB - R 255 G 255  B 255
Black_Colour = (0,0,0)
Red_Colour = (255,0,0)
Green_Colour = (0,255,0)
Blue_Colour = (0,0,255)
Clock = pygame.time.Clock()
Tick_Rate = 60 
Is_Game_Over = False

Game_Screen = pygame.display.set_mode((Screen_Width, Screen_Height)) #Creates the window being displayed 
Game_Screen.fill(White_Colour) #Sets the default colour of the displayed window 
pygame.display.set_caption(Screen_Title)

while Is_Game_Over == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Is_Game_Over = True
        print(event)

    pygame.display.update()
    Clock.tick(Tick_Rate)


pygame.quit()
quit()