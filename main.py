import random

import arcade
from config import (
    ASSETS_BAR_BLUE_BLUE,
    ASSETS_BALL_BLUE,
    ASSETS_BALL_RED,
    ASSETS_BALL_YELLOW,
    WIN_X,
    WIN_Y,
    GRID_SIZE_H,
    GRID_SIZE_V,
    ITEM_BLANK,
    ITEM_SIZE,
    DIFFICULTY_EASY,
    KEY_SPEED,
    GAME_SPEED,
    DROPDOWN_SPEED,
    GRID_PAD_LEFT,
    GRID_PAD_BOTTOM,
    LEVEL_MAX,
    ITEM_VIRUS_B,
    ITEM_VIRUS_R,
    ITEM_VIRUS_Y,
    DIRECTION_NEUTRAL,
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
    DIRECTION_DOWN,
    ROTATION_NEUTRAL,
    ROTATION_LEFT,
    ROTATION_RIGHT,
)

from sprites import (
    SpriteVirus,
    SpriteBlank,
    SpriteBar,
)


class Window(arcade.Window):

    def __init__(self):
        super().__init__(WIN_X, WIN_Y)
        self.grid = []
        self.grid_previous = []
        self.grid_sprite_list = None
        self.elapsed_time = 0
        self.elapsed_key_time = 0
        self.elapsed_dropdown_time = 0
        self.game_speed = GAME_SPEED
        self.key_speed = KEY_SPEED
        self.dropdown_speed = 0
        self.level = 0
        self.bars = None
        self.current_bar = None
        self.direction = DIRECTION_NEUTRAL
        self.rotation = ROTATION_NEUTRAL
        self.debug = True
        self.setup()

    def setup(self):
        self.grid_sprite_list = arcade.SpriteList()
        self.grid = [[ITEM_BLANK] * GRID_SIZE_H for i in range(GRID_SIZE_V)]
        self.difficulty = DIFFICULTY_EASY
        self.dropdown_speed = DROPDOWN_SPEED
        self.level = 20
        self.bars = [SpriteBar.Random(), SpriteBar.Random(), SpriteBar.Random()]
        self.current_bar = SpriteBar.Random()
        self.build_grid()

    def reset_grid(self):
        for row in range(GRID_SIZE_V):
            for column in range(GRID_SIZE_H):
                sprite = SpriteBlank()
                sprite.position = (column * ITEM_SIZE + GRID_PAD_LEFT,
                                   row * ITEM_SIZE + GRID_PAD_BOTTOM)
                self.grid_sprite_list.append(sprite)

    def build_grid(self):
        self.reset_grid()

        virus_count = self.level * 4
        positions = [[x, y] for y in range(GRID_SIZE_V - 3) for x in range(GRID_SIZE_H)]
        weights = [1 / (position[1] + 1) for position in positions]
        blocks = []
        for _ in range(virus_count):
            index = random.choices(range(len(positions)), weights, k=1)[0]
            virus = random.choice([ITEM_VIRUS_B, ITEM_VIRUS_R, ITEM_VIRUS_Y])
            blocks.append(positions[index] + [virus])
            positions.pop(index)
            weights.pop(index)
            

        for (x, y, virus) in blocks:
            self.grid[y][x] = virus
            sprite_index = y * GRID_SIZE_H + x
            new_sprite = (
                0,
                SpriteVirus.create_blue_virus,
                SpriteVirus.create_red_virus,
                SpriteVirus.create_yellow_virus,
            )[virus]()
            new_sprite.position = (x * ITEM_SIZE + GRID_PAD_LEFT, y * ITEM_SIZE + GRID_PAD_BOTTOM)
            old_sprite = self.grid_sprite_list[sprite_index]
            self.grid_sprite_list.remove(old_sprite)
            self.grid_sprite_list.insert(sprite_index, new_sprite)

    def debug_grid(self):
        positions = [(
            GRID_PAD_LEFT + (i * ITEM_SIZE),
            GRID_PAD_BOTTOM + (j * ITEM_SIZE),
        ) for i in range(GRID_SIZE_H) for j in range(GRID_SIZE_V)]

        for x, y in positions:
            arcade.draw_rectangle_outline(x, y, width=20, height=20, color=arcade.color.ORANGE)

    def next_bar(self):
        self.current_bar = self.bars.pop()
        self.bars.append(SpriteBar.Random())

    def on_update(self, delta_time):
        if self.elapsed_time >= self.game_speed:
            self.elapsed_time -= self.game_speed

            # MOVE THE BAR ON INPUT
            if self.direction is not DIRECTION_NEUTRAL and self.elapsed_key_time > self.key_speed:
                self.current_bar.move(self.direction)
                self.elapsed_key_time = 0

            # ROTATE THE BAR
            if self.rotation is not ROTATION_NEUTRAL:
                self.current_bar.rotate(self.rotation)
                self.rotation = ROTATION_NEUTRAL

            # MOVE THE BAR AUTOMATICLY
            if self.elapsed_dropdown_time > self.dropdown_speed:
                self.current_bar.move(DIRECTION_DOWN)
                self.elapsed_dropdown_time = 0

        self.elapsed_time += delta_time
        self.elapsed_key_time += delta_time
        self.elapsed_dropdown_time += delta_time

    def on_draw(self):
        arcade.start_render()
        self.grid_sprite_list.draw()
        self.current_bar.draw()
        if self.debug:
            self.debug_grid()
            self.current_bar.debug_matrix()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.direction = DIRECTION_LEFT
            self.elapsed_key_time = KEY_SPEED
        elif key == arcade.key.RIGHT:
            self.direction = DIRECTION_RIGHT
            self.elapsed_key_time = KEY_SPEED
        elif key == arcade.key.DOWN:
            self.direction = DIRECTION_DOWN
            self.elapsed_key_time = KEY_SPEED
        elif key == arcade.key.A:
            self.rotation = ROTATION_LEFT
        elif key == arcade.key.E:
            self.rotation = ROTATION_RIGHT

        elif key == arcade.key.ESCAPE:
            self.close()

        elif key == arcade.key.R:
            self.setup()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT and self.direction == DIRECTION_LEFT:
            self.direction = DIRECTION_NEUTRAL

        if key == arcade.key.RIGHT and self.direction == DIRECTION_RIGHT:
            self.direction = DIRECTION_NEUTRAL

        if key == arcade.key.DOWN and self.direction == DIRECTION_DOWN:
            self.direction = DIRECTION_NEUTRAL


def main():
    Window()
    arcade.run()


if __name__ == '__main__':
    main()
