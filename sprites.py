import arcade
import random

from config import (
    ASSETS_VIRUS_BLUE,
    ASSETS_VIRUS_BLUE2,
    ASSETS_VIRUS_YELLOW,
    ASSETS_VIRUS_YELLOW2,
    ASSETS_VIRUS_RED,
    ASSETS_VIRUS_RED2,
    ASSETS_BALL_BLUE,
    ASSETS_BALL_YELLOW,
    ASSETS_BALL_RED,
    ITEM_BLANK,
    ITEM_VIRUS_B,
    ITEM_VIRUS_R,
    ITEM_VIRUS_Y,
    ITEM_BLOCK_B,
    ITEM_BLOCK_R,
    ITEM_BLOCK_Y,
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

ball_textures = {
    ITEM_BLOCK_B: ASSETS_BALL_BLUE,
    ITEM_BLOCK_Y: ASSETS_BALL_YELLOW,
    ITEM_BLOCK_R: ASSETS_BALL_RED,
}


class SpriteBlank(arcade.SpriteSolidColor):

    def __init__(self):
        super().__init__(20, 20, arcade.color.BLACK_BEAN)


class SpriteBlock(arcade.Sprite):

    def __init__(self, block_type):
        super().__init__(ball_textures[block_type], scale=2)
        self.type = block_type


class SpriteBar():

    def __init__(self, block1, block2):
        self.block1 = block1
        self.block2 = block2
        self.grid_position = [GRID_SIZE_H // 2 - 1, GRID_SIZE_V - 1]
        self.matrix = [[self.block1, self.block2], [0, 0]]
        self.set_position()

    def set_position(self):
        for col in range(2):
            for row in range(2):
                item = self.matrix[col][row]
                if item is self.block1 or item is self.block2:
                    item.position = (GRID_PAD_LEFT + (self.grid_position[0] + row) * ITEM_SIZE,
                                     GRID_PAD_BOTTOM + (self.grid_position[1] + col) * ITEM_SIZE)

    def rotate(self, direction=ROTATION_LEFT):
        if direction == ROTATION_LEFT:
            self.matrix = [list(r) for r in zip(*self.matrix[::-1])]
        elif direction == ROTATION_RIGHT:
            self.matrix = [list(r) for r in reversed(list(zip(*self.matrix)))]
        self.set_position()

    def move(self, direction):
        if direction == DIRECTION_DOWN:
            self.grid_position[1] -= 1

        elif direction == DIRECTION_LEFT:
            self.grid_position[0] -= 1

        elif direction == DIRECTION_RIGHT:
            self.grid_position[0] += 1

        self.set_position()

    def draw(self):
        self.block1.draw()
        self.block2.draw()

    @classmethod
    def Random(cls):
        blocks = [
            (ITEM_BLOCK_R, ITEM_BLOCK_R),
            (ITEM_BLOCK_R, ITEM_BLOCK_Y),
            (ITEM_BLOCK_R, ITEM_BLOCK_B),
            (ITEM_BLOCK_B, ITEM_BLOCK_B),
            (ITEM_BLOCK_B, ITEM_BLOCK_R),
            (ITEM_BLOCK_B, ITEM_BLOCK_Y),
            (ITEM_BLOCK_Y, ITEM_BLOCK_B),
            (ITEM_BLOCK_Y, ITEM_BLOCK_R),
            (ITEM_BLOCK_Y, ITEM_BLOCK_Y),
        ]
        choosen_blocks = random.choice(blocks)
        block1 = SpriteBlock(choosen_blocks[0])
        block2 = SpriteBlock(choosen_blocks[1])
        return SpriteBar(block1, block2)

    def debug_matrix(self):
        positions = [(
            GRID_PAD_LEFT + (self.grid_position[0] + i) * ITEM_SIZE,
            GRID_PAD_BOTTOM + (self.grid_position[1] + j) * ITEM_SIZE,
        ) for i in range(len(self.matrix)) for j in range(len(self.matrix))]

        for x, y in positions:
            arcade.draw_rectangle_outline(x, y, width=20, height=20, color=arcade.color.GREEN)


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
