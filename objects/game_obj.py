# Main game object
# Contains gameplay loop, frame rate and basic display
import pygame, sys

class Game:
    # Sets framerate for game to default of 60 FPS
    fps = 60
    title = "Super Space Pirate"
    clock = pygame.time.Clock()

    def __init__ (self, width, height, controls):
        self.width = width
        self.height = height 
        self.player_controls = controls
        self.game_screen = pygame.display.set_mode((width, height)) #Creates the window being displayed 
        pygame.display.set_caption(self.title)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Add more event handling logic here (e.g., player controls)
                
    def set_player_controls(self, controls):
        """
        Used to update the player controls
        """
        self.player_controls = controls


    def update(self):
        # Update game state, player, enemies, etc.
        pass

    def render(self):
        self.game_screen.fill((0, 0, 0))  # Clear the screen with black
        # Draw everything to the screen here
        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)



# This code will only be executed if the script is run as the main program
# Used for debugging and unit testing
if __name__ == "__main__":

    print("Test completed")