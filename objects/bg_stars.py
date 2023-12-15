# File containing background stars

class star_obj: 
    """
    Class for defining star object to be drawn in the background
    """
    def __init__(self, x_pos, y_pos, width, height):

        # Scales the image that's been loaded in 
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
    
    def draw (self,background):
        """
        Mehtod used to display the object on the game screen
        """
        pygame.draw.circle(self.game_screen, full_colour, (x_pos_list[star_num], y_pos_list[star_num]), star_size)


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


# This code will only be executed if the script is run as the main program
# Used for debugging and unit testing
if __name__ == "__main__":
    import pygame, random

    # TODO - Define game object to import and create tests

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

    print("Test completed")