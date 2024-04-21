import pygame
from Settings import *
import os

# This is for file importing but is in Main.py anyways
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Tile(pygame.sprite.Sprite): # "tile" likely refers to a unit of measurement used to define the size of elements in a game or graphical environment.
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)

        self.sprite_type = sprite_type
        y_offset = HITBOX_OFFSET[sprite_type]
        self.image = surface
        
        if sprite_type == "object":
            self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, y_offset)
        
# In many contexts, especially in game development, a "tile" refers to a small, square or rectangular graphical element used to compose a larger image or scene. These tiles are often arranged in a grid pattern to create backgrounds, levels, or maps for games        

# self.sprite_type = sprite_type: Here, you're assigning a value to the sprite_type attribute of the sprite object. This attribute likely represents the type or category of the sprite, which can be useful for differentiating between different kinds of sprites in your game or application.
# y_offset = HITBOX_OFFSET[sprite_type]: This line retrieves a value from the HITBOX_OFFSET dictionary based on the sprite_type and assigns it to the y_offset variable. It seems like HITBOX_OFFSET contains offsets for hitboxes associated with different sprite types. This offset might be used to adjust the position or size of the sprite's hitbox relative to its image.
# self.image = surface: Finally, you're assigning the surface to the image attribute of the sprite object. This surface likely represents the graphical image or texture that will be displayed for the sprite.
# In summary, this code snippet initializes attributes for a sprite object, including its type, hitbox offset, and graphical image. These attributes are essential for defining the properties and appearance of the sprite within the game or graphical application.