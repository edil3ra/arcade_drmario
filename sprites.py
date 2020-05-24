import arcade
import random
from config import (
    ASSETS_VIRUS_BLUE,
    ASSETS_VIRUS_BLUE2,
    ASSETS_VIRUS_YELLOW,
    ASSETS_VIRUS_YELLOW2,
    ASSETS_VIRUS_RED,
    ASSETS_VIRUS_RED2,
    ASSETS_BAR_BLUE_BLUE,
    ASSETS_BAR_RED_BLUE,
    ASSETS_BAR_YELLOW_BLUE,
    ASSETS_BAR_BLUE_RED,
    ASSETS_BAR_RED_RED,
    ASSETS_BAR_YELLOW_RED,
    ASSETS_BAR_BLUE_YELLOW,
    ASSETS_BAR_RED_YELLOW,
    ASSETS_BAR_YELLOW_YELLOW,
    ITEM_VIRUS_B,
    ITEM_VIRUS_R,
    ITEM_VIRUS_Y,
    ITEM_BAR_B_B,
    ITEM_BAR_R_B,
    ITEM_BAR_Y_B,
    ITEM_BAR_B_R,
    ITEM_BAR_R_R,
    ITEM_BAR_Y_R,
    ITEM_BAR_B_Y,
    ITEM_BAR_R_Y,
    ITEM_BAR_Y_Y,
    ITEM_SIZE,
    GRID_PAD_LEFT,
    GRID_PAD_BOTTOM,
    GRID_SIZE_V,
    GRID_SIZE_H,
    DIRECTION_NEUTRAL,
    DIRECTION_DOWN,
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
    ROTATION_NEUTRAL,
    ROTATION_LEFT,
    ROTATION_RIGHT,
)

bar_textures = {
    ITEM_BAR_B_B: arcade.load_texture(ASSETS_BAR_BLUE_BLUE),
    ITEM_BAR_R_B: arcade.load_texture(ASSETS_BAR_RED_BLUE),
    ITEM_BAR_Y_B: arcade.load_texture(ASSETS_BAR_YELLOW_BLUE),
    ITEM_BAR_B_R: arcade.load_texture(ASSETS_BAR_BLUE_RED),
    ITEM_BAR_R_R: arcade.load_texture(ASSETS_BAR_RED_RED),
    ITEM_BAR_Y_R: arcade.load_texture(ASSETS_BAR_YELLOW_RED),
    ITEM_BAR_B_Y: arcade.load_texture(ASSETS_BAR_BLUE_YELLOW),
    ITEM_BAR_R_Y: arcade.load_texture(ASSETS_BAR_RED_YELLOW),
    ITEM_BAR_Y_Y: arcade.load_texture(ASSETS_BAR_YELLOW_YELLOW),
}


class SpriteBlank(arcade.SpriteSolidColor):

    def __init__(self):
        super().__init__(20, 20, arcade.color.BLACK_BEAN)


class SpriteBar(arcade.Sprite):

    def __init__(self, type):
        self.matrix = [[1, 1], [0, 0]]
        super().__init__()
        self.type = type
        self.setup_filename(type)
        self.grid_position = [GRID_SIZE_H // 2 - 1, GRID_SIZE_V - 1]
        self.set_position()

    def setup_filename(self, type):
        self.texture = bar_textures[type]
        self.scale = 2.3

    def set_position(self):
        x = 0
        y = 0
        if self.matrix[0][1] == 1 and self.matrix[1][1] == 1:
            x = 1
        if self.matrix[1][0] == 1 and self.matrix[1][1] == 1:
            y = 1

        self.position = [
            GRID_PAD_LEFT + (self.grid_position[0] + x) * ITEM_SIZE + 15,
            GRID_PAD_BOTTOM + (self.grid_position[1] + y) * ITEM_SIZE - 3
        ]

    def rotate(self, direction=ROTATION_LEFT):
        if direction == ROTATION_LEFT:
            self.matrix = [list(r) for r in zip(*self.matrix[::-1])]
        elif direction == ROTATION_RIGHT:
            self.matrix = [list(r) for r in reversed(zip(*self.matrix))]
        self.set_position()

    def update(self, delta_time):
        pass

    def move(self, direction):
        if direction == DIRECTION_DOWN:
            self.grid_position[1] -= 1

        elif direction == DIRECTION_LEFT:
            self.grid_position[0] -= 1

        elif direction == DIRECTION_RIGHT:
            self.grid_position[0] += 1

        self.set_position()

    @classmethod
    def Random(cls):
        types = [
            ITEM_BAR_B_B,
            ITEM_BAR_R_B,
            ITEM_BAR_Y_B,
            ITEM_BAR_B_R,
            ITEM_BAR_R_R,
            ITEM_BAR_Y_R,
            ITEM_BAR_B_Y,
            ITEM_BAR_R_Y,
            ITEM_BAR_Y_Y,
        ]
        type = random.choice(types)
        return SpriteBar(type)


    def debug_matrix(self):
        positions = [(
            GRID_PAD_LEFT + (self.grid_position[0] + i) * ITEM_SIZE,
            GRID_PAD_BOTTOM + (self.grid_position[1] + j) * ITEM_SIZE,
        ) for i in range(len(self.matrix)) for j in range(len(self.matrix))]

        for x, y in positions:
            arcade.draw_rectangle_outline(x, y, width=20, height=20, color=arcade.color.GREEN)



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
