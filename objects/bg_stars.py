# File containing background stars
import random

class StarObj: 
    """
    Class for defining star object to be drawn in the background
    """
    def __init__(self, x_pos, y_pos ):

        # Sets default full colour of star
        colour = (255, 255, 255)
        # Sets random ammount to reduce star brightness by on spawn
        self.dimness = random.randint(60, 120)
        # Distance from player making the star move faster or slower
        if random.randint(0, 1) == 1:
            self.speed = random.uniform(4,6)
            self.size = 2
        else:
            self.speed = random.uniform(1,3)
            self.size = 1
            # Sets dimness to double if the star is far away
            self.dimness *= 2

        # Scales the image that's been loaded in 
        self.x = x_pos
        self.y = y_pos
        self.colour = (colour[0] - self.dimness, colour[1] - self.dimness, colour[2] - self.dimness)


    def set_flicker(self):
        """
        Reroll dimness to give star a flickering effect
        """
        # Sets default full colour of star
        colour = (255, 255, 255)
        # Sets random ammount to reduce star brightness by on spawn
        self.dimness = random.randint(60, 120)
        # Distance from player making the star move faster or slower
        if self.size == 1:
            self.dimness *= 2
        self.colour = (colour[0] - self.dimness, colour[1] - self.dimness, colour[2] - self.dimness)


    def move(self, x_dir, y_dir, clock_tick):
        """
        Moves star based on directions passed
        """
        delta_time = clock_tick / 1000.0

        # Moves star at set speed based on delta time from last frame 
        self.x += (x_dir * self.speed) * delta_time
        self.y += (y_dir * self.speed) * delta_time


    def reroll(self, x_pos, y_pos, size = random.uniform(1,2), colour = (255, 255, 255)):
        """
        Reroll star attributes to make it seem like a new star
        """
        # Sets random ammount to reduce star brightness by on spawn
        dimness = random.randint(1, 90)
        # Distance from player making the star move faster or slower
        if random.randint(0, 1) == 1:
            self.speed = random.uniform(4,6)
            self.size = 2
        else:
            self.speed = random.uniform(1,3)
            self.size = 1
            # Sets dimness to double if the star is far away
            dimness *= 2

        # Scales the image that's been loaded in 
        self.x = x_pos
        self.y = y_pos
        self.colour = (colour[0] - dimness, colour[1] - dimness, colour[2] - dimness)


    def draw(self, game_screen):
        """
        Mehtod used to display the object on the game screen.
        Includes logic to make the star flicker based on distance
        """

        # Sets new dimness level to make star flicker on next draw call
        self.set_flicker()

        pygame.draw.circle(game_screen, self.colour, (self.x, self.y), self.size)


def set_star_list(window_width, window_height, starlist = [], num_of_stars = 200):
    """
    Create new list of stars for game world
    """

    for num in range(num_of_stars):
        new_star = StarObj(random.uniform(0,window_width), random.uniform(0,window_height))
        # adds new star object to the starlist
        starlist.append(new_star)

    return starlist

def all_star_move(starlist, screen, clock_tick):
    # Draw stars on screen for testing
    for star in starlist:
        star.draw(screen)
        star.move(0, 1, clock_tick)
        if star.y > height + star.size:
            star.reroll(star.x, -2)

# This code will only be executed if the script is run as the main program
# Used for debugging and unit testing
if __name__ == "__main__":
    import pygame, random

    # TODO - Define game object to import and create tests

    clock = pygame.time.Clock()
    # set tick rate
    clock_tick = clock.tick(60)
    # Screen dimensions
    width, height = 800, 600
    # Sets number of stars to be drawn in background
    total_stars = 250

    # Sets two lists with X and Y pos of stars to be drawn
    starlist_xpos = random.sample(range(1, 800), total_stars )
    starlist_ypos = random.sample(range(1, 800), total_stars )

    # List of boolean values used to determine if the star is near of far.
    starlist = [] 
    if len(starlist) == 0:
        starlist = set_star_list(width, height, starlist, total_stars)

    def run_game_loop(pygame, tick):
        pygame.display.update() #Updates the current frame after completing the loop
        clock.tick(tick) #Sets the frame rate per second

    # Initialize Pygame
    pygame.init()


    screen = pygame.display.set_mode((width, height))

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen (fill with black)
        screen.fill((0, 0, 0))
        # Draw stars on screen and move them
        all_star_move(starlist, screen, clock_tick)
        # Update game screen to draw frame
        pygame.display.update() #Updates the current frame after completing the loop
        
        
    pygame.quit()

    print("Test completed")
