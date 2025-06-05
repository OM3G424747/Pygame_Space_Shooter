"""Utility to manage player control mappings.

This module defines :class:`Control` which stores the key bindings used
for player input and allows them to be updated at runtime.
"""

import pygame

class Control:
    def __init__ (self):
        # Default control settings using arrow keys
        self.controls = {
            "up": pygame.K_UP,
            "down": pygame.K_DOWN,
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "fire": pygame.K_SPACE,
            "enter": pygame.K_RETURN
        }


    def update_input(self, action, new_key):
        """ Reassign the key for a specific action. """
        if action in self.controls:
            self.controls[action] = new_key

    def get_control_key(self, action):
        """ Get the current key assigned to a specific action. """
        return self.controls.get(action, None)




# This code will only be executed if the script is run as the main program
# Used for debugging and unit testing
if __name__ == "__main__":

    print("Test completed")