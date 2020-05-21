import arcade
from config import (
    ASSETS_VIRUS_BLUE,
    ASSETS_VIRUS_BLUE2,
    ASSETS_VIRUS_YELLOW,
    ASSETS_VIRUS_YELLOW2,
    ASSETS_VIRUS_RED,
    ASSETS_VIRUS_RED2,
    ITEM_VIRUS_B,
    ITEM_VIRUS_R,
    ITEM_VIRUS_Y,
)

class SpriteBlank(arcade.SpriteSolidColor):
    def __init__(self):
        super().__init__(20, 20, arcade.color.BLACK_BEAN)
        

class SpriteBar(arcade.Sprite):
    
    def __init__(self):
        self.matrix = [[0, 0], [0, 0]]
        super().__init__()
        self.setup()

    def setup(type):
        if type == 

    def switch(self):
        pass

    def update(self, delta_time):
        pass


class SpriteBlock(arcade.Sprite):

    def __init__(self, filename):
        pass


class SpriteVirus(arcade.Sprite):

    def __init__(self, image1, image2):
        self.image1 = image1
        self.image2 = image2
        self.type = None
        super().__init__(image1, 2)


    @classmethod
    def create_blue_virus(cls,):
        virus = cls(ASSETS_VIRUS_BLUE, ASSETS_VIRUS_BLUE2)
        virus.type = ITEM_VIRUS_B
        return virus

    @classmethod
    def create_red_virus(cls,):
        virus = cls(ASSETS_VIRUS_RED, ASSETS_VIRUS_RED2)
        virus.type = ITEM_VIRUS_R
        return virus

    @classmethod
    def create_yellow_virus(cls,):
        virus = cls(ASSETS_VIRUS_YELLOW, ASSETS_VIRUS_YELLOW2)
        virus.type = ITEM_VIRUS_R
        return virus


