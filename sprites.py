import arcade
import random

from config import (
    ASSETS_VIRUS_BLUE,
    ASSETS_VIRUS_YELLOW,
    ASSETS_VIRUS_RED,
    ASSETS_BALL_BLUE,
    ASSETS_BALL_YELLOW,
    ASSETS_BALL_RED,
    ASSETS_BLACK,
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
    DIRECTION_DOWN,
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
    ROTATION_LEFT,
    ROTATION_RIGHT,
)

ball_textures = {
    ITEM_BLANK: arcade.load_texture(ASSETS_BLACK),
    ITEM_BLOCK_B: arcade.load_texture(ASSETS_BALL_BLUE),
    ITEM_BLOCK_Y: arcade.load_texture(ASSETS_BALL_YELLOW),
    ITEM_BLOCK_R: arcade.load_texture(ASSETS_BALL_RED),
    ITEM_VIRUS_B: arcade.load_texture(ASSETS_VIRUS_BLUE),
    ITEM_VIRUS_Y: arcade.load_texture(ASSETS_VIRUS_YELLOW),
    ITEM_VIRUS_R: arcade.load_texture(ASSETS_VIRUS_RED),
}


class SpriteBlock(arcade.Sprite):

    def __init__(self, block_type, scale=2):
        super().__init__(scale=scale)
        self.index = (0, 0)
        self.set_type(block_type)

    def set_type(self, block_type):
        self.type = block_type
        self.texture = ball_textures[self.type]


class SpriteBar():

    def __init__(self, block1, block2):
        self.block1 = block1
        self.block2 = block2
        self.grid_position = [0, 0]
        self.matrix = [[0, 0], [0, 0]]
        self.previous_matrix = [0, 0]
        self.previous_grid_position = [0, 0]
        self.setup()

    def setup(self):
        self.grid_position = [GRID_SIZE_H // 2 - 1, GRID_SIZE_V - 1]
        self.matrix = [[self.block1, self.block2], [0, 0]]
        self.previous_grid_position = self.grid_position
        self.previous_matrix = self.matrix
        self.set_position()

    def set_position(self):
        for col in range(2):
            for row in range(2):
                item = self.matrix[col][row]
                if item is self.block1 or item is self.block2:
                    item.index = (row, col)
                    item.position = (GRID_PAD_LEFT + (self.grid_position[0] + row) * ITEM_SIZE,
                                     GRID_PAD_BOTTOM + (self.grid_position[1] + col) * ITEM_SIZE)

    def move(self, direction):
        self.previous_grid_position = self.grid_position[::]
        if direction == DIRECTION_DOWN:
            self.grid_position[1] -= 1
        elif direction == DIRECTION_LEFT:
            self.grid_position[0] -= 1
        elif direction == DIRECTION_RIGHT:
            self.grid_position[0] += 1
        self.set_position()

    def rotate(self, rotation=ROTATION_LEFT):
        self.previous_matrix = self.matrix[::]
        if rotation == ROTATION_LEFT:
            self.matrix = [list(r) for r in zip(*self.matrix[::-1])]
        elif rotation == ROTATION_RIGHT:
            self.matrix = [list(r) for r in reversed(list(zip(*self.matrix)))]
        self.set_position()

    def set_previous_rotation(self):
        self.matrix = self.previous_matrix
        self.set_position()

    def set_previous_position(self):
        self.grid_position = self.previous_grid_position
        self.set_position()

    def draw(self):
        self.block1.draw()
        self.block2.draw()

    def blocks(self):
        "Get blocks and grid positions"
        return (
            [
                self.block1,
                self.block1.index[0] + self.grid_position[0],
                self.block1.index[1] + self.grid_position[1],
            ],
            [
                self.block2,
                self.block2.index[0] + self.grid_position[0],
                self.block2.index[1] + self.grid_position[1],
            ],
        )

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
