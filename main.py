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
    GAME_SPEED_EASY,
    GRID_PAD_LEFT,
    GRID_PAD_BOTTOM,
    LEVEL_MAX,
    ITEM_VIRUS_B,
    ITEM_VIRUS_R,
    ITEM_VIRUS_Y,
)

from sprites import (
    SpriteVirus,
    SpriteBlank,
)



class Window(arcade.Window):
    def __init__(self):
        super().__init__(WIN_X, WIN_Y)
        self.grid = []
        self.grid_previous = []
        self.grid_sprite_list = arcade.SpriteList()
        self.elapsed_time = 0
        self.game_speed = 0
        self.level = 0
        self.setup()

    def setup(self):
        self.grid = [[ITEM_BLANK] * GRID_SIZE_H for i in range(GRID_SIZE_V)]
        self.game_speed = GAME_SPEED_EASY
        self.level = 1
        self.build_grid()

    def reset_grid(self):
        for row in range(GRID_SIZE_V):
            for column in range(GRID_SIZE_H):
                sprite = SpriteBlank()
                sprite.position = (
                    column * ITEM_SIZE + GRID_PAD_LEFT,
                    row * ITEM_SIZE + GRID_PAD_BOTTOM
                )
                self.grid_sprite_list.append(sprite)

    def build_grid(self):
        self.reset_grid()

        virus_count = self.level * 4
        positions = [
            (x, y)
            for y in range(GRID_SIZE_V - 3)
            for x in range(GRID_SIZE_H)
        ]

        blocks = [
            (x, y, random.choice([ITEM_VIRUS_B, ITEM_VIRUS_R, ITEM_VIRUS_Y]))
            for x, y in random.choices(positions, k=virus_count)
        ]
        for (x, y, virus) in blocks:
            self.grid[y][x] = virus
            sprite_index = y * GRID_SIZE_H + x
            new_sprite = (
                0,
                SpriteVirus.create_blue_virus,
                SpriteVirus.create_red_virus,
                SpriteVirus.create_yellow_virus,
            )[virus]()
            new_sprite.position = (
                x * ITEM_SIZE + GRID_PAD_LEFT,
                y * ITEM_SIZE + GRID_PAD_BOTTOM
            )
            old_sprite = self.grid_sprite_list[sprite_index]
            self.grid_sprite_list.remove(old_sprite)
            self.grid_sprite_list.insert(sprite_index, new_sprite)



    def on_update(self, delta_time):
        if self.elapsed_time >= self.game_speed:
            self.elapsed_time -= self.game_speed
            # self.set_item_pos()
        self.elapsed_time += delta_time

    def on_draw(self):
        arcade.start_render()
        self.grid_sprite_list.draw()


    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.LEFT:
            pass
        elif key == arcade.key.RIGHT:
            pass
        elif key == arcade.key.UP:
            pass
        elif key == arcade.key.DOWN:
            pass
        elif key == arcade.key.ESCAPE:
            self.close()
 


def main():
    Window()
    arcade.run()


if __name__ == 'main':
    main()
