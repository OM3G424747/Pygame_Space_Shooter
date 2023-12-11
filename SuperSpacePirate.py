"""
Make sure you install python3.6 with the "Add python 3.6 to PATH" option selected. 
PLEASE INSTALL PYGAME in your python scripts folder using "pip install" before running!

To install pygame on windows please follow these instructions:

1. Start by opening a command line. 
You can do this by pressing the windows key and then typing cmd and then pressing enter.

2. Put in the following code into the command line:
pip install pygame

3. If it succeeds, please restart any IDE you have open to ensure the changes take effect.

Dev Notes:
Below are some examples of how to draw basic shapes in pygame.

pygame.draw.rect(Game_Screen, Red_Colour, [400,100,100,100]) #sets surface, colour and X-pos,Y-pos+size for the rectangle to be drawn
pygame.draw.circle(Game_Screen, Green_Colour, (400, 300), 50) #sets surface, colour and X-pos,Y-pos+size for the circle to be drawn
"""

import pygame
import random
import math
import os

# Sets initial game states
screen_width = 800
screen_height = 800
screen_title = "Super Space Pirate"
white_colour = (255,255,255)
black_colour = (0,0,0)
red_colour = (255,0,0)
green_colour = (0,255,0)
blue_colour = (0,0,255)
grey_colour = (100,100,100)
lightgrey_colour = (200,200,200)
ship_width = 75
ship_height = 75
clock = pygame.time.Clock()

# Sets number of stars to be drawn in background
total_stars = 250

# Sets two lists with X and Y pos of stars to be drawn
starlist_xpos = random.sample(range(1, 800), total_stars )
starlist_ypos = random.sample(range(1, 800), total_stars )

# Stores speed of individual starts in a lists
starlist_speed = []

# List of boolean values used to determine if the star is near of far.
starlist_bool = [] 

def set_bool_to_list(num = 0, bool_list = []):
    """
    Used to set bool values in a list at random
    """
    for star in range(num):
        # Sets True for far stars and False for near stars
        random_bool = random.randint(0,1)
        if random_bool == 1:
            bool_list.append(True)
        elif random_bool == 0:
            bool_list.append(False)
    return bool_list


def set_star_speed(star_num = 0, speed_list = [], bool_list = []):
    """
    Used to set speed of individual stars
    """
    if bool_list[star_num]:
        random_speed = random.randint(4,6)
        speed_list[star_num] = random_speed
    else:
        random_speed = random.randint(1,3)
        speed_list[star_num] = random_speed


def set_init_star_speed(num = 0, speed_list = [], bool_list = []):

    """
    Used to set initial speed list in for stars
    """

    # Checks if star in near of far to set initial speed list
    for near_star in bool_list:

        if near_star:
            random_speed = random.randint(4,6)
            speed_list.append(random_speed)
        else:
            random_speed = random.randint(1,3)
            speed_list.append(random_speed)

starlist_bool = set_bool_to_list(num = total_stars, passed_list = starlist_bool)
starlist_speed = set_init_star_speed(num = total_stars, speed_list = starlist_speed , bool_list = starlist_bool)


class game_object: 
    """
    Class for defining game objects that will be drawn onto the game screen and moved arround
    """
    def __init__(self, image_path, x_pos, y_pos, width, height):
        
        object_image = pygame.image.load(image_path)
        # Scales the image that's been loaded in 
        self.image = pygame.transform.scale(object_image, (width, height)) 
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
    
    def draw (self,background):
        """
        Mehtod used to display the object on the game screen
        """
        background.blit(self.image,(self.x_pos,self.y_pos)) #Blit funtion is used to draw imaghes to the game screen/ surface selected along with the X and Y Pos taken in the form of a tuple 
        

class player_obj(game_object):
    
    """
    Sets player object with default behaviour and attributes
    """

    speed = 10 

    def __init__ (self, image_path, x_pos, y_pos, width, height):
        game_object.__init__(self, image_path, x_pos, y_pos, width, height)
    
    def move(self, x_direction, y_direction, max_height, max_width): #Checks input for player
        """
        Method used to check player input and to change direction
        """
        
        # TODO - Refactor after testing:
        # -- pos = pos + (speed * direction)
        
        if y_direction > 0 and x_direction == 0:
            self.y_pos = self.y_pos - self.speed #used to make the Ship go up
        
        elif y_direction > 0 and x_direction > 0: #Up and left combined (Combined movement devided to match regular speed)
            self.y_pos = self.y_pos - self.speed *0.5
            self.x_pos = self.x_pos - self.speed *0.5
        
        elif y_direction > 0 and x_direction < 0: #Up and right combined (Combined movement devided to match regular speed)
            self.y_pos = self.y_pos - self.speed *0.5
            self.s_pos = self.x_pos + self.speed *0.5

        elif y_direction < 0 and x_direction == 0:
            self.y_pos = self.y_pos + self.speed #used to make the Ship go down
        
        elif y_direction < 0 and x_direction > 0: #Down and left combined (Combined movement devided to match regular speed)
            self.y_pos = self.y_pos + self.speed *0.5
            self.x_pos = self.y_pos - self.speed *0.5
        
        elif y_direction < 0 and x_direction < 0: #Down and right combined (Combined movement devided to match regular speed)
            self.y_pos = self.y_pos + self.speed *0.5 
            self.x_pos = self.x_pos + self.speed *0.5 

        elif x_direction > 0 and y_direction == 0:
            self.x_pos = self.x_pos - self.speed #used to make the Ship go left
        
        elif x_direction < 0 and y_direction == 0:
            self.x_pos = self.x_pos + self.speed #used to make the Ship go right 


        if self.y_pos >= max_height - 120: #sets collision detection for bottom of the screen for player to make sure they don't go over the health bar or off the screen 
            self.y_pos = max_height - 120
        if self.y_pos <= 50: #sets collision detection for top of the screen for player to make sure they don't go over the health bar or off the screen 
            self.y_pos = 50
        if self.x_pos >= max_width - 80:
            self.x_pos = max_width - 80
        if self.x_pos <= 5:
            self.x_pos = 5


class lazer_obj(game_object):
    speed = 10

    def __init__(self, image_path, x_pos, y_pos, width, height):
        game_object.__init__(self, image_path, x_pos, y_pos, width, height)   

    def fire (self, fire, direction, height, game_screen):
        
        if fire == True:
            self.draw(game_screen)
            
            if direction == "Up":
                
                if self.y_pos >= 0:
                    self.y_pos = self.y_pos - self.speed
                    
            elif direction == "Down":
                
                if self.y_pos <= height:
                    self.y_pos = self.y_pos + self.speed
                    

    def damage (self, enemy_x_pos, enemy_y_pos): #Colision detection for Lazer on Enemy ship
        
        if enemy_x_pos - 5 < self.x_pos and enemy_x_pos + 75 > self.x_pos and enemy_y_pos - 15 < self.y_pos and enemy_y_pos + 80 > self.y_pos:
            return True
        
        else:
            return False


class nonplayer_obj(game_object):
    
    # Speed = random.randint(5, 7) #program AI to change speed at random when fired at
    speed = 6
    stop = 0
    away_from_border = 150 #used to check if enemy ship is away from the border to help clear it from moving into the border
    def __init__ (self, image_path, x_pos, y_pos, width, height):
        game_object.__init__(self, image_path, x_pos, y_pos, width, height)
    
    def move(self, target_x_pos, target_y_pos, game_screen): #moves non-player in the direction of the player's current location on the X axis 
        self.speed = 4 #reset Speed movement back 
        
        if self.x_pos <=  target_x_pos - 10:
            #self.Speed = abs(self.Speed)
            self.x_pos += self.speed #moves ship right if it's not in line
            
            if self.x_pos >= target_x_pos -10:
                self.x_pos += self.stop #stops ship once it's lined up

        elif self.x_pos >= target_x_pos + 10: 
            #self.Speed = -abs(self.Speed)
            self.x_pos -= self.speed #moves ship left if it's not in line
            
            if self.x_pos >= target_x_pos +10: 
                self.x_pos += self.stop #stops ship once it's lined up


    def panic(self, danger, danger_x_pos, game_screen): 
        # Causes non-player character to move at a faster pace away from player's lazer to try and escape danger 
        
        danger_x_pos = danger_x_pos - 35 # Calibrates lazer Xpos to check with the center of the ship

        if danger == True and self.x_pos <= danger_x_pos: # Checks if enemy ship is to the left side of the Lazer and moves the ship right if it is 
            self.speed = 7
            if self.x_pos <= self.away_from_border and danger_x_pos < self.away_from_border:
                self.speed = abs(self.speed)
                self.x_pos += self.speed
            else:
                self.speed = -abs(self.speed)
                self.x_pos += self.speed 
        
        elif danger == True and self.x_pos >= danger_x_pos: # Checks if enemy ship is to the right side of the Lazer and moves the ship right if it is 
            self.speed = 7
            if self.x_pos > game_screen - self.away_from_border and danger_x_pos > game_screen - self.away_from_border: 
                self.x_pos -= self.speed
            elif self.x_pos < game_screen - self.away_from_border: 
                self.x_pos += self.speed
                

    def lure_player (self,player_x_pos, player_y_pos, random_int): # Creat a function to make the AI lure the player to attempt to attack it
        if player_y_pos <= self.y_pos + 250 and self.y_pos >= 50: 
            self.y_pos -= self.speed # Panic function turns this into a charge where the ship attacks the player
            
            if self.y_pos < 150:
                self.y_pos += self.speed
        
        elif player_y_pos >= self.y_pos + 300:
            self.y_pos += self.speed
        # Use random int to change abs speed to negative and charge the player at random 


#TODO - Add variable and lists for spheres to simulate explosions         
class particles: #used to set the base stats and attributes for particles 
    def __init__ (self, game_screen): #funtion for testing particles 
        self.ship_hit = False  
        self.particle_fade =[] #list to hold colour value for yellow (start at 255) Red and Green
        self.particle_fade_alt=[] #list to hold colour value for blue to make the the yellow colour more white 
        self.particles_start_x_pos = []
        self.particles_start_y_pos = []
        self.particles_end_y_pos = []
        self.particles_end_y_pos = []
        self.particles_speed = []
        self.game_screen = game_screen     

class health_bar:
    
    full_colour = 255
    chunks = 100
    final_shot = 25
    
    def __init__ (self, x_pos, y_pos, total_blocks):
        self.damage_taken = 0
        self.total_blocks = self.final_shot + total_blocks * self.chunks #Total lenght the bar will be drawn in the X axis. (Final_shot is used for the size of the final health bar size, Total blocks determines the number of hits the ship can take, Chunks determins the size of the bar proportunate to the Blocks)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.colour = (0,self.full_colour,self.full_colour) #Sets colour of "full health" health bar

    def colour_adjust (self, total_blocks): #Changes colour of the enemy health bar from an initial light blue to green after being hit, and then gradually from green to red based on the number of hits and health left
        colour_reduction = self.full_colour / total_blocks #determines the percetentage of the colour to be reduced according to the number of blocks selected
        green = self.full_colour - colour_reduction * self.damage_taken #Used to calculate by how much green will be reduced on the RGB scale
        red = colour_reduction * self.damage_taken #Determines how much red will be added on the RGB scale 
        self.colour = (int(red),int(green),0)

    def Draw (self, game_screen):
        pygame.draw.rect(game_screen, self.colour, [self.x_pos,self.y_pos,self.total_blocks,25]) #sets surface, colour and X-pos,Y-pos+size for the bar to be drawn.

class lazer_bar:
    
    length = 120 
    
    def __init__ (self, x_pos, y_pos, lazer_y_pos, end_pos, colour):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.end_pos = end_pos
        self.colour = colour
        self.chunks = self.EndPos / lazer_y_pos
        self.start_pos = lazer_y_pos
        
        
    def enemy_draw (self, lazer_y_pos, game_screen):
        
        enemy_len = lazer_y_pos / self.end_pos * self.length 
        pygame.draw.rect(game_screen, self.colour, [self.x_pos,self.y_pos,enemy_len,25])

    def player_draw (self, lazer_y_pos, game_screen):
        
        total_len = lazer_y_pos / self.start_pos * self.length
        self.player_len = self.length - total_len
        pygame.draw.rect(game_screen, self.colour, [self.x_pos, self.y_pos, self.player_len, 25])


# GAME CLASS AND LOOP ====

class game:
    # Sets framerate for game
    tick_rate = 60
    
    def __init__ (self, title, width, height):
        self.title = title
        self.width = width
        self.height = height 
        self.game_screen = pygame.display.set_mode((width, height)) #Creates the window being displayed 
        self.game_screen.fill(black_colour) #Sets the default colour of the displayed window 
        pygame.display.set_caption(title)
    
    
    def run_game_loop (self):
        is_game_over = False
        player_won = False
        cpu_won = False
        menu = True
        alt_menu = 0
        fight = False
        y_direction = 0
        x_direction = 0
        lazer_count = 0
        fire_lazer = False
        enemy_lazer = False
        blocks = 4 #Sets the number of hits the ships can take before it's game over
        enemy_hit = False #used to detect if the enemy ship is hit
        player_hit = False #used to detect if the player ship is hit
        danger = False
        random_mistake = random.randint(1,10) #Determines if the AI will make a mistake 
        ai_difficulty = 6 # lower number = easy | Higher number = hard (select number between 1 and 10)
    
        FireOkay = True
        player1 = player_obj("assets/hud/ship.png", 660, 600, ship_width, ship_height) #creates player 1 ship character 
        enemy = nonplayer_obj("assets/hud/enemy.png", 160, 200, ship_width, ship_height)
        lazer = lazer_obj("assets/hud/Lazer.png", player1.x_pos, player1.y_pos, 10, 60)
        enemy_lazer = lazer_obj("assets/hud/Lazer2.png", enemy.x_pos +35, enemy.y_pos, 10, 60)
        explode = lazer_obj ("assets/hud/boom.png", enemy.x_pos -15, enemy.y_pos, 75, 75)
        enemy_health = health_bar(10, 0, blocks)
        enemy_hud_border = nonplayer_obj("assets/hud/EnemyHealthBorder.png", 0, 0, 180, 55 ) 
        enemy_hud_corner = nonplayer_obj("assets/hud/EnemyBorderCorner.png",blocks * enemy_health.chunks - 40, -10, 80, 40 )
        player1_health = health_bar(470, 770, blocks)
        player1_health.x_pos = screen_width - blocks * player1_health.chunks #sets initial starting postion of player healthbar so it's adjusted according to the number of blocks selected and the size of the chunks selected
        player_hud_border = nonplayer_obj("assets/hud/PlayerHealthBorder.png", 620, 740, 180, 55 ) 
        player_hud_corner = nonplayer_obj("assets/hud/PlayerBorderCorner.png", screen_width - blocks * player1_health.chunks - 6, 765, 80, 40 )
        enemy_lazer_hud = nonplayer_obj("assets/hud/EnemyLazerHud.png", enemy_hud_corner.x_pos + 100, enemy_hud_border.y_pos, 140, 30)
        enemy_lazer_status = nonplayer_obj("assets/hud/EnemyLazerReadyStatus.png", enemy_lazer_hud.x_pos + 150, enemy_hud_border.y_pos, 120, 30)
        enemy_charge = lazer_bar(enemy_lazer_hud.x_pos + 150, enemy_hud_border.y_pos, enemy_lazer.x_pos, 730, red_colour)
        player_lazer_hud = nonplayer_obj("assets/hud/PlayerLazerHud.png", player_hud_corner.x_pos - 290, player_hud_border.y_pos + 25, 140, 30)
        player_lazer_status = nonplayer_obj("assets/hud/PlayerLazerReadyStatus.png", player_lazer_hud.x_pos + 150, player_lazer_hud.y_pos, 120, 30)
        player_charge = lazer_bar(player_lazer_hud.x_pos + 150, player_lazer_hud.y_pos, lazer.x_pos, 2, blue_colour)
        gameover_screen = nonplayer_obj("assets/menu/GameOver.png", 100, 300, 600, 200)
        win_screen = nonplayer_obj("assets/menu/win.png", 100, 300, 600, 200)
        logo = nonplayer_obj("assets/menu/Logo.png", 0, 0, 800, 800)
        end_game = nonplayer_obj("assets/menu/Quit.png", 300, 750, 201, 14)
        control_menu = nonplayer_obj("assets/menu/ControlMenu.png", 255, 710, 284, 14 ) #Image, X, Y, Width, Height 
        settings_menu = game_object("assets/menu/SettingsMenu.png", 155, 660, 504, 18)
        ruturn_menu = nonplayer_obj("assets/menu/ReturnMain.png", 100, 680, 625, 20)
        control_list = game_object("assets/menu/controls.png", 55, 220, 695, 200)
        difficulty_header = game_object("assets/menu/DiffHeader.png", 100, 220, 485, 18)
        easy_setting = game_object("assets/menu/easy.png", 100, 320, 343, 18)
        medium_setting = game_object("assets/menu/Medium.png", 100, 420, 381, 18)
        hard_setting = game_object("assets/menu/Hard.png", 100, 520, 419, 18)


        sparks = particles(self.game_screen)


        # Game loop checks if the game is over and will repeat until the condition is met and the game over state is set to True
        while is_game_over == False: 
            
            for event in pygame.event.get():
                if event.type == pygame.quit:
                    is_game_over = True

                # CONTROLLS ------
                
                # Sets default directions
                y_direction = 0
                x_direction = 0

                keys = pygame.key.get_pressed()

                # Checks for Up arrow key
                if keys[pygame.K_UP]: 
                    y_direction = 1

                # Checks for Down arrow key
                elif keys[pygame.K_DOWN]: 
                    y_direction = -1
                
                # Checks for Right arrow key
                if keys[pygame.K_RIGHT]: 
                    x_direction = -1
                
                # Checks for Left arrow key
                elif keys[pygame.K_LEFT]: 
                    x_direction = 1

                # Spawns lazer if fired by player
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        if fire_lazer == False:
                            fire_lazer = True
                            lazer.y_pos = player1.y_pos
                            lazer.x_pos = player1.x_pos + 32

##################################################
#TODO -> Continue to refactor from this point on #
##################################################
            
            #StarGeneratorFunction ----------------------------------------
            
            def draw_star(bool_list = [], x_pos_list = [], y_pos_list = []):
                """
                Method that draws star based on if they should be near of far
                """
                for star_num in range(total_stars):

                    # Sets brighter flicker effect to nearby stars
                    if bool_list[star_num]:
                        star_colour = random.randint(120, 180)
                        full_colour = (star_colour, star_colour, star_colour)
                        star_size = 2

                    # Sets dim colour to far away stars
                    else:
                        star_colour = random.randint(50, 100)
                        full_colour = (star_colour, star_colour, star_colour)
                        star_size = 1
                        
                    pygame.draw.circle(self.game_screen, full_colour, (x_pos_list[star_num], y_pos_list[star_num]), star_size)
                    
                    # updates speed
                    # speed_list = set_star_speed(star_num, speed_list = [], bool_list = [])
                

            def StarGenerator(PlayerY_direction, PlayerX_direction): #create funtion to generate and move stars based on player movement 
                # Method used to draw stars

                for star_num in range (total_stars): #used to generate stars based on the number selected 
                    
                    draw_star(starlist_bool, starlist_xpos, starlist_ypos )

                    # TODO - Create method to move stars

                    # Confirms the frame ticked over by 1
                    if clock.tick() == 1:
                        
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

            #Menu Selections ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
            if Menu == True and altMenu == 0:
                self.game_screen.fill(Black_Colour)
                StarGenerator(0,-1) #used to make the stars move down while on the main screen
                EndGame.Draw(self.game_screen)
                ControlMenu.Draw(self.game_screen)
                SettingsMenu.Draw(self.game_screen)

                Logo.Draw(self.game_screen) #PlaceHolder Logo for Main Menu
                if keys[pygame.K_RETURN] == True: #PlaceHolder for Start input 
                    Menu = False
                    Fight = True
                #TODO add option for difficulty menu ******
                elif keys[pygame.K_c] == True:
                    altMenu = 1
                elif keys[pygame.K_s] == True:
                    altMenu = 2
                elif keys[pygame.K_ESCAPE] == True:
                    Is_Game_Over = True

            elif Menu == True and altMenu == 1:
                self.game_screen.fill(Black_Colour)
                StarGenerator(1,0) #used to make the stars move down while on the main screen
                ControlList.Draw(self.game_screen)
                RuturnToMainMenu.Draw(self.game_screen)
               
                if keys[pygame.K_BACKSPACE] == True: #PlaceHolder for Start input 
                    altMenu = 0

            elif Menu == True and altMenu == 2: #CONTINUE HERE -> add menu for AI difficulty 
                self.game_screen.fill(Black_Colour)
                StarGenerator(1,0)
                DifficultyHeader.Draw(self.game_screen)
                EasySetting.Draw(self.game_screen)
                MediumSetting.Draw(self.game_screen)
                HardSetting.Draw(self.game_screen)
                RuturnToMainMenu.Draw(self.game_screen)
                if keys[pygame.K_BACKSPACE] == True: #PlaceHolder for Start input 
                    altMenu = 0
                elif keys[pygame.K_e] == True:
                    AI_Difficulty = 2
                    pygame.draw.rect(self.game_screen, White_Colour, [EasySetting.X_pos,EasySetting.Y_pos + 30,450,25])
                elif keys[pygame.K_m] == True: #TODO Add function to draw a sqaure arround / behind the selected option ******
                    AI_Difficulty = 5
                    pygame.draw.rect(self.game_screen, White_Colour, [EasySetting.X_pos,MediumSetting.Y_pos + 30,450,25])
                elif keys[pygame.K_h] == True:
                    AI_Difficulty = 9
                    pygame.draw.rect(self.game_screen, White_Colour, [EasySetting.X_pos,HardSetting.Y_pos + 30,450,25])
                
            

            # Game Over Conditions ------------------------------------------------------------------------------------------------------------------
            elif Player1_Health.DamageTaken == 4: #sets the number of shots the player can take before it's game over
                CPUWon = True
                Fight = False
                self.game_screen.fill(Black_Colour)
                GameOverScreen.Draw(self.game_screen)
                pygame.display.update() #Updates the current frame after completing the loop
                if keys[pygame.K_RETURN] == True: #PlaceHolder for Start input 
                    Menu = False
                    Fight = True
                    CPUWon = False
                    self.run_game_loop()
                    
                
            elif Enemy_Health.DamageTaken == 5: #sets the number of shots the enemy can take before it's game over
                PlayerWon = True
                Fight = False  
                self.game_screen.fill(Black_Colour)
                WinScreen.Draw(self.game_screen)
                pygame.display.update() #Updates the current frame after completing the loop
                if keys[pygame.K_RETURN] == True: #PlaceHolder for Start input 
                    Menu = False
                    Fight = True
                    CPUWon = False
                    self.run_game_loop()


            # Game Start Conditions -----------------------------------------------------------------------------------------------------------------------------------------------------------
            elif Menu == False and Fight == True:    #print(event) - remove as comment to see current events being logged 
                self.game_screen.fill(Black_Colour)
                StarGenerator(Y_direction, X_direction) #Generates stars that move in the opposite direction to the player      
                
                Enemy.LurePlayer( Player1.X_pos, Player1.Y_pos, 1 ) #1 is a playerholder for a random int to be added 
                if FireLazar == True: #Enemy AI conditions used to check if the player has fired their lazer
                    if Lazer.X_pos >= Enemy.X_pos - 10 and Lazer.X_pos <= Enemy.X_pos + 85 and Lazer.Y_pos >= Enemy.Y_pos + 80: 
                        if Random_Mistake <= AI_Difficulty:
                            Danger = True
                            Enemy.Panic(Danger,Lazer.X_pos, Screen_Width)
                        elif Random_Mistake > AI_Difficulty: #Sets Enemy AI's ability to make a random mistake and give the player an oppertunity to hit them (Value needs to be between 1 and 10. 1 = Easy and 10 = Hard )
                            Danger = False
                            Enemy.Move(Player1.X_pos, Player1.Y_pos, Screen_Width)
                    elif Lazer.X_pos <= Enemy.X_pos - 75 or Lazer.X_pos >= Enemy.X_pos + 150:
                        Danger = False
                        Enemy.Move(Player1.X_pos, Player1.Y_pos, Screen_Width)
                else:
                    Enemy.Move( Player1.X_pos, Player1.Y_pos, Screen_Width)
                
                Enemy.Draw (self.game_screen) 
                Player1_Health.Draw(self.game_screen)
                PlayerHealthBorder.Draw(self.game_screen)
                PlayerHealthCorner.Draw(self.game_screen)
                Enemy_Health.Draw(self.game_screen)
                EnemyHealthBorder.Draw(self.game_screen)
                EnemyHealthCorner.Draw(self.game_screen)
                EnemyLazarHud.Draw(self.game_screen)
                PlayerLazarHud.Draw(self.game_screen)
                
                Player1.Move(X_direction, Y_direction, Screen_Height, Screen_Width)
                Player1.Draw (self.game_screen)
                    
                    ### commented out to rework particle system - create single block of code to append, blit and then remove all for the same "i" variable 
                    
                def Sparksfun (lazerMovement, shipX, shipY, lazerX, lazerY, Hit):    
                    shipXPos = lazerX
                    shipYPos = lazerY
                    count = 0
                    if Hit == True: 
                        sparks.shipHit = True 
                    elif Hit == False:
                        sparks.shipHit = False

                    if sparks.shipHit == True:
                        for i in range (3):
                            sparks.particlesSpeed.append(abs(int(random.randint(1, 3))))
                            sparks.particleFade.append(255) #appends list with max colour for Red and green
                            sparks.particleFadeAlt.append(175) #appends list with colour used for blue to make yellow more white 
                            sparks.particlesStartY_pos.append(int(shipYPos))
                            sparks.particlesStartX_pos.append(int(shipXPos))
                            if lazerMovement == "Up":
                                destinationY_pos = random.randint(int(shipY), int(shipY) + 400)
                            elif lazerMovement == "Down":
                                destinationY_pos = random.randint(int(shipY) - 400, int(shipY))
                            sparks.particlesEndY_pos.append(int(destinationY_pos))
                            if shipX + 38 > lazerX: #checks if the lazer it the left side of the ship
                                sparks.particlesEndX_pos.append(random.randint(int(shipX - 800), int(shipX + 37)))
                            elif shipX + 36 < lazerX: #checks if the lazer it the rigth side of the ship
                                sparks.particlesEndX_pos.append(random.randint(int(shipX), int(shipX + 800)))

                    elif sparks.shipHit == False:
                        if len(sparks.particlesStartX_pos) > 1: #adjust so it continues to delete the list even if shipHit is false
                            if sparks.particlesStartX_pos[-1] <= sparks.particlesEndX_pos[-1]:
                                del sparks.particlesSpeed[-1]
                                del sparks.particleFade[-1]
                                del sparks.particleFadeAlt[-1]
                                del sparks.particlesEndY_pos[-1]
                                del sparks.particlesEndX_pos[-1]
                                del sparks.particlesStartY_pos[-1]
                                del sparks.particlesStartX_pos[-1]
                            else:
                                del sparks.particlesSpeed[0]
                                del sparks.particleFade[0]
                                del sparks.particleFadeAlt[0]
                                del sparks.particlesEndY_pos[0]
                                del sparks.particlesEndX_pos[0]
                                del sparks.particlesStartY_pos[0]
                                del sparks.particlesStartX_pos[0]

                    
#TODO add spheres to simulate an explosions, changing from small bright yello, so orrange, red and grey - (replace regular explosions )
                    if lazerMovement == "Up":
                        for i in range (len(sparks.particlesStartX_pos)): # used for calculating the colour fade and movement of the particles 
                            if len(sparks.particlesStartX_pos) >= 1: 
                                if sparks.particlesStartY_pos[i - 1] < sparks.particlesEndY_pos[i - 1]:
                                    if sparks.particlesStartX_pos[i - 1] <= sparks.particlesEndX_pos[i - 1] and sparks.particlesStartY_pos[i - 1] < sparks.particlesEndY_pos[i - 1]:
                                        fadeChunk = random.randint(1,6) #used to randomly calculate the amount the sparks will fade by
                                        if sparks.particleFade[i - 1] > fadeChunk and sparks.particleFadeAlt[i - 1] > fadeChunk:
                                            sparks.particleFade[i - 1] -= fadeChunk
                                            sparks.particleFadeAlt[i - 1] -= fadeChunk
                                        elif sparks.particleFade[i - 1] > fadeChunk and sparks.particleFadeAlt[i - 1] < fadeChunk:
                                            sparks.particleFade[i - 1] -= fadeChunk
                                            sparks.particleFadeAlt[i - 1] = 0
                                        elif sparks.particleFade[i - 1] < fadeChunk:
                                            sparks.particleFade[i - 1] = 0
                                        sparks.particlesStartX_pos[i - 1] = sparks.particlesStartX_pos[i - 1] + sparks.particlesSpeed[i - 1] - random.randint(0,5)
                                        sparks.particlesStartY_pos[i - 1] = sparks.particlesStartY_pos[i - 1] + sparks.particlesSpeed[i - 1] - random.randint(0,3)
                                        pygame.draw.circle(sparks.game_screen, (sparks.particleFade[i - 1],sparks.particleFade[i - 1],sparks.particleFadeAlt[i - 1]), (sparks.particlesStartX_pos[i - 1],sparks.particlesStartY_pos[i - 1]), 1)
                                                        
                                    elif sparks.particlesStartX_pos[i - 1] >= sparks.particlesEndX_pos[i - 1] and sparks.particlesStartY_pos[i - 1] < sparks.particlesEndY_pos[i - 1]:
                                        fadeChunk = random.randint(2,7)
                                        if sparks.particleFade[i - 1] > fadeChunk and sparks.particleFadeAlt[i - 1] > fadeChunk:
                                            sparks.particleFade[i - 1] -= fadeChunk
                                            sparks.particleFadeAlt[i - 1] -= fadeChunk
                                        elif sparks.particleFade[i - 1] > fadeChunk and sparks.particleFadeAlt[i - 1] < fadeChunk:
                                            sparks.particleFade[i - 1] -= fadeChunk
                                            sparks.particleFadeAlt[i - 1] = 0
                                        elif sparks.particleFade[i - 1] < fadeChunk:
                                            sparks.particleFade[i - 1] = 0

                                        sparks.particlesStartX_pos[i - 1] = sparks.particlesStartX_pos[i - 1] - sparks.particlesSpeed[i - 1] + random.randint(0,5)
                                        sparks.particlesStartY_pos[i - 1] = sparks.particlesStartY_pos[i - 1] + sparks.particlesSpeed[i - 1] - random.randint(0,3)
                                        pygame.draw.circle(sparks.game_screen, (sparks.particleFade[i - 1],sparks.particleFade[i - 1],sparks.particleFadeAlt[i - 1]), (sparks.particlesStartX_pos[i - 1],sparks.particlesStartY_pos[i - 1]), 1)
                                   

                    elif lazerMovement == "Down":
                        for i in range (len(sparks.particlesStartX_pos)): # used for calculating the colour fade and movement of the particles 
                            if len(sparks.particlesStartX_pos) >= 1: 
                                if sparks.particlesStartY_pos[i - 1] > sparks.particlesEndY_pos[i - 1]:
                                    if sparks.particlesStartX_pos[i - 1] <= sparks.particlesEndX_pos[i - 1] and sparks.particlesStartY_pos[i - 1] > sparks.particlesEndY_pos[i - 1]:
                                        fadeChunk = random.randint(1,6) #used to randomly calculate the amount the sparks will fade by
                                        if sparks.particleFade[i - 1] > fadeChunk and sparks.particleFadeAlt[i - 1] > fadeChunk:
                                            sparks.particleFade[i - 1] -= fadeChunk
                                            sparks.particleFadeAlt[i - 1] -= fadeChunk
                                        elif sparks.particleFade[i - 1] > fadeChunk and sparks.particleFadeAlt[i - 1] < fadeChunk:
                                            sparks.particleFade[i - 1] -= fadeChunk
                                            sparks.particleFadeAlt[i - 1] = 0
                                        elif sparks.particleFade[i - 1] < fadeChunk:
                                            sparks.particleFade[i - 1] = 0
                                        sparks.particlesStartX_pos[i - 1] = sparks.particlesStartX_pos[i - 1] + sparks.particlesSpeed[i - 1] - random.randint(0,5)
                                        sparks.particlesStartY_pos[i - 1] = sparks.particlesStartY_pos[i - 1] + sparks.particlesSpeed[i - 1] - random.randint(0,3)
                                        pygame.draw.circle(sparks.game_screen, (sparks.particleFade[i - 1],sparks.particleFade[i - 1],sparks.particleFadeAlt[i - 1]), (sparks.particlesStartX_pos[i - 1],sparks.particlesStartY_pos[i - 1]), 1)
                                                        
                                    elif sparks.particlesStartX_pos[i - 1] >= sparks.particlesEndX_pos[i - 1] and sparks.particlesStartY_pos[i - 1] > sparks.particlesEndY_pos[i - 1]:
                                        fadeChunk = random.randint(2,7)
                                        if sparks.particleFade[i - 1] > fadeChunk and sparks.particleFadeAlt[i - 1] > fadeChunk:
                                            sparks.particleFade[i - 1] -= fadeChunk
                                            sparks.particleFadeAlt[i - 1] -= fadeChunk
                                        elif sparks.particleFade[i - 1] > fadeChunk and sparks.particleFadeAlt[i - 1] < fadeChunk:
                                            sparks.particleFade[i - 1] -= fadeChunk
                                            sparks.particleFadeAlt[i - 1] = 0
                                        elif sparks.particleFade[i - 1] < fadeChunk:
                                            sparks.particleFade[i - 1] = 0

                                        sparks.particlesStartX_pos[i - 1] = sparks.particlesStartX_pos[i - 1] - sparks.particlesSpeed[i - 1] + random.randint(0,5)
                                        sparks.particlesStartY_pos[i - 1] = sparks.particlesStartY_pos[i - 1] + sparks.particlesSpeed[i - 1] - random.randint(0,3)
                                        pygame.draw.circle(sparks.game_screen, (sparks.particleFade[i - 1],sparks.particleFade[i - 1],sparks.particleFadeAlt[i - 1]), (sparks.particlesStartX_pos[i - 1],sparks.particlesStartY_pos[i - 1]), 1)
                   

                #Moved here for testing particles 
                
                Sparksfun ("Up", Enemy.X_pos, Enemy.Y_pos, Lazer.X_pos, Lazer.Y_pos, Lazer.Damage(Enemy.X_pos, Enemy.Y_pos))
              

                if FireLazar == True:
                    Lazer.Fire(FireLazar,"Up",Screen_Height, self.game_screen) 
                    PlayerCharge.PlayerDraw(Lazer.Y_pos ,self.game_screen)
                    if Lazer.Damage(Enemy.X_pos, Enemy.Y_pos) == True:
                       
                        Explode.Y_pos = Enemy.Y_pos
                        Explode.X_pos = Enemy.X_pos
                        Explode.Draw (self.game_screen)

#TODO - adjust so that the ammount reduced in chunks is caculated by the value of damage ... EG - 1 damage = 100 blocks, 0.5 damage - 50 blocks                        
                        EnemyHit = True
                    elif EnemyHit == True and Lazer.Damage(Enemy.X_pos, Enemy.Y_pos) == False: #used to adjust the enemy health bar after being hit by the player's lazer
                        Enemy_Health.TotalBlocks = Enemy_Health.TotalBlocks - Enemy_Health.Chunks
                        Enemy_Health.DamageTaken = Enemy_Health.DamageTaken + 1 #Adjusts he colour of the health bar by incrementing the damage taken for comparison to the initial chunks 
                        if Enemy_Health.TotalBlocks > 1: #Temp argument to keep the game from crashing after the final shot is given 
                            Enemy_Health.ColourAdjust(Blocks)
                        Enemy_Health.Draw(self.game_screen)
                        EnemyHit = False
                if Lazer.Y_pos <= 25:  
                    FireLazar = False
                if FireLazar == False:
                    PlayerLazarStatus.Draw(self.game_screen)

                
                if EnemyLazar == False:
                    EnemyLazarStatus.Draw(self.game_screen)  
                if LazerCount == 1: #detects if lazer fire was queued by the AI due to the player being in range
                    EnemyLazar = True #sets coditions to True for enemy lazer fire
                    if EnemyLazar == True : 
                        Enemy_Lazer.Fire(EnemyLazar,"Down",Screen_Height, self.game_screen)
                        EnemyCharge.EnemyDraw(Enemy_Lazer.Y_pos ,self.game_screen)

                        if Enemy_Lazer.Y_pos >= 730:
                            EnemyLazar = False #removes the lazer from the screen 
                            Random_Mistake = random.randint(1,10) #Reset the Random int to give the AI a chance to mess up during their next shot. Only resets after enemy fire to avoid Enemy getting hit by "player lazer spam"
                            LazerCount = 0 #removes the queued lazer so the AI can add another
                        
                    Sparksfun("Down", Player1.X_pos, Player1.Y_pos, Enemy_Lazer.X_pos, Enemy_Lazer.Y_pos, Enemy_Lazer.Damage(Player1.X_pos, Player1.Y_pos))
                    if Enemy_Lazer.Damage(Player1.X_pos, Player1.Y_pos) == True: #Conditions for player taking damager by enemy ship
                        Explode.Y_pos = Player1.Y_pos
                        Explode.X_pos = Player1.X_pos
                        Explode.Draw (self.game_screen)
                        PlayerHit = True
                    elif PlayerHit == True and Enemy_Lazer.Damage(Player1.X_pos, Player1.Y_pos) == False: #used to adjust the enemy health bar after being hit by the player's lazer
                        Player1_Health.TotalBlocks = Player1_Health.TotalBlocks - Player1_Health.Chunks
                        Player1_Health.DamageTaken = Player1_Health.DamageTaken + 1 #Adjusts he colour of the health bar by incrementing the damage taken for comparison to the initial chunks 
                        if Player1_Health.TotalBlocks > 1: #Temp argument to keep the game from crashing after the final shot is given 
                            Player1_Health.ColourAdjust(Blocks)
                            Player1_Health.X_pos = Player1_Health.X_pos + Player1_Health.Chunks #Moves the player health bar to the right propotionately to the ammount that's been removed from it 
                        Player1_Health.Draw(self.game_screen)
                        PlayerHit = False

                    if Player1.X_pos >= Enemy.X_pos - 50 and Player1.X_pos <= Enemy.X_pos + 75 and Player1.Y_pos >= Enemy.Y_pos - 60 and Player1.Y_pos <= Enemy.Y_pos + 65: #Checks if the ships collide, numbers adjust to accomodate the shpe and size of the sprites
                        Explode.Y_pos = Player1.Y_pos
                        Explode.X_pos = Player1.X_pos
                        Explode.Draw (self.game_screen)
                        Explode.Y_pos = Enemy.Y_pos
                        Explode.X_pos = Enemy.X_pos
                        Explode.Draw (self.game_screen)
                        Player1_Health.TotalBlocks = Player1_Health.TotalBlocks - Player1_Health.Chunks
                        Player1_Health.DamageTaken = Player1_Health.DamageTaken + 1 #Adjusts he colour of the health bar by incrementing the damage taken for comparison to the initial chunks 
                        if Player1_Health.TotalBlocks > 1: #Temp argument to keep the game from crashing after the final shot is given 
                            Player1_Health.ColourAdjust(Blocks)
                        Player1_Health.draw(self.game_screen)
                        

                elif Player1.x_pos - 35 <= Enemy.x_pos and Player1.x_pos + 25 >= Enemy.x_pos: #Used to queue lazer fire with the AI
                    Enemy_Lazer.y_pos = Enemy.y_pos
                    Enemy_Lazer.x_pos = Enemy.x_pos + 35
                    LazerCount = 1 #Queued lazer fire with the AI





            pygame.display.update() #Updates the current frame after completing the loop
            clock.tick(self.tick_rate) #Sets the frame rate per second
    


pygame.init()

new_game = game(screen_title,screen_width,screen_height) #creates a new game part of the "game class"

new_game.run_game_loop() #Starts the game loop as defined in the class to continue looping until the game over state becomes true 

pygame.quit()
quit()


