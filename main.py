import random
from copy import deepcopy
import arcade
from config import (
    ASSETS_BALL_BLUE,
    ASSETS_BALL_RED,
    ASSETS_BALL_YELLOW,
    WIN_X,
    WIN_Y,
    GRID_SIZE_H,
    GRID_SIZE_V,
    ITEM_BLANK,
    ITEM_BLOCK_B,
    ITEM_BLOCK_R,
    ITEM_BLOCK_Y,
    ITEM_VIRUS_B,
    ITEM_VIRUS_R,
    ITEM_VIRUS_Y,
    ITEM_SIZE,
    DIFFICULTY_EASY,
    KEY_SPEED,
    GAME_SPEED,
    DROPDOWN_SPEED,
    GRID_PAD_LEFT,
    GRID_PAD_BOTTOM,
    LEVEL_MAX,
    DIRECTION_NEUTRAL,
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
    DIRECTION_DOWN,
    ROTATION_NEUTRAL,
    ROTATION_LEFT,
    ROTATION_RIGHT,
    VERTICAL_ORIENTATION,
    HORIZONTAL_ORIENTATION
)

from sprites import (
    SpriteBlock,
    SpriteBar,
)
from utils import vertical_tree_blocks, horizontal_tree_blocks


class Window(arcade.Window):

    def __init__(self):
        super().__init__(WIN_X, WIN_Y)
        self.grid = []
        self.previous_grid = []
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
        self.previeus_bar = None
        self.direction = DIRECTION_NEUTRAL
        self.rotation = ROTATION_NEUTRAL
        self.has_move = False
        self.has_rotate = False
        self.debug = True
        self.is_playing = True
        self.clear_vertical = False
        self.clear_horizontal = False
        self.blocks_to_drop = []
        self.blocks_cleared = []
        self.setup()

    def setup(self):
        self.grid_sprite_list = arcade.SpriteList()
        self.grid = [[ITEM_BLANK] * GRID_SIZE_H for i in range(GRID_SIZE_V)]
        self.difficulty = DIFFICULTY_EASY
        self.dropdown_speed = DROPDOWN_SPEED
        self.level = 1
        self.bars = [SpriteBar.Random(), SpriteBar.Random(), SpriteBar.Random()]
        self.current_bar = SpriteBar.Random()
        self.build_grid()

    def reset_grid(self):
        for row in range(GRID_SIZE_V):
            for column in range(GRID_SIZE_H):
                sprite = SpriteBlock(ITEM_BLANK)
                sprite.position = (column * ITEM_SIZE + GRID_PAD_LEFT,
                                   row * ITEM_SIZE + GRID_PAD_BOTTOM)
                self.grid_sprite_list.append(sprite)
        self.previous_grid = self.grid[::]

    def update_grid(self):
        for row in range(GRID_SIZE_V):
            for column in range(GRID_SIZE_H):
                previous_item = self.previous_grid[row][column]
                current_item = self.grid[row][column]
                if previous_item != current_item:
                    sprite_index = (row) * (GRID_SIZE_H) + column
                    self.grid_sprite_list[sprite_index].set_type(current_item)
        self.previous_grid = deepcopy(self.grid)

    def generate_virus(self):
        virus_count = self.level * 4
        positions = [[x, y] for y in range(GRID_SIZE_V - 3) for x in range(GRID_SIZE_H)]
        weights = [(1 / (position[1] + 1)) for position in positions]
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
            self.grid_sprite_list[sprite_index].set_type(virus)

    def build_grid(self):
        self.reset_grid()
        self.generate_virus()

    def debug_grid(self):
        positions = [(
            GRID_PAD_LEFT + (i * ITEM_SIZE),
            GRID_PAD_BOTTOM + (j * ITEM_SIZE),
        ) for i in range(GRID_SIZE_H) for j in range(GRID_SIZE_V)]

        for x, y in positions:
            arcade.draw_rectangle_outline(x, y, width=20, height=20, color=arcade.color.ORANGE)

    def next_bar(self):
        self.previous_bar = self.current_bar
        self.current_bar = self.bars.pop()
        self.bars.append(SpriteBar.Random())

    def is_bar_collide_with_left_right_boundary(self):
        for _, x, _ in self.current_bar.blocks():
            if x < 0 or x >= GRID_SIZE_H:
                return True
        return False

    def is_bar_collide_with_bottom_boundary(self):
        for _, _, y in self.current_bar.blocks():
            if y < 0:
                return True
        return False

    def is_bar_collide_with_blocks(self):
        for _, x, y in self.current_bar.blocks():
            if x < GRID_SIZE_H and y < GRID_SIZE_V:
                if self.grid[y][x] is not ITEM_BLANK:
                    return True
        return False

    def is_virus(self, item):
        return item is ITEM_VIRUS_B or item is ITEM_VIRUS_R or item is ITEM_VIRUS_Y

    def is_block(self, item):
        return item is ITEM_BLOCK_B or item is ITEM_BLOCK_R or item is ITEM_BLOCK_Y

    def is_red(self, item):
        return item is ITEM_BLOCK_R or item is ITEM_VIRUS_R

    def is_blue(self, item):
        return item is ITEM_BLOCK_B or item is ITEM_VIRUS_B

    def is_yellow(self, item):
        return item is ITEM_BLOCK_Y or item is ITEM_VIRUS_Y

    def handle_clear_horizontal(self):
        self.clear_horizontal = False
        for y in range(GRID_SIZE_V):
            for x in range(GRID_SIZE_H - 4):
                blocks = self.grid[y][x:x + 4]
                all_red = all([self.is_red(block) for block in blocks])
                all_yellow = all([self.is_yellow(block) for block in blocks])
                all_blue = all([self.is_blue(block) for block in blocks])
                if all_red or all_yellow or all_blue:
                    is_checked = False
                    self.clear_horizontal = True
                    if x + 4 <= GRID_SIZE_H:
                        item = self.grid[y][x + 4]
                        if (all_red and self.is_red(item)) or\
                           (all_blue and self.is_blue(item)) or\
                           (all_yellow and self.is_yellow(item)):
                            self.grid[y][x:x + 5] = [ITEM_BLANK] * 5
                            self.blocks_cleared.append([(y, x + i) for i in range(5)])
                            is_checked = True
                    if not is_checked:
                        self.blocks_cleared.append([(y, x + i) for i in range(4)])
                        self.grid[y][x:x + 4] = [ITEM_BLANK] * 4


    def handle_clear_vertical(self):
        self.clear_vertical = False
        for y in range(GRID_SIZE_V - 4):
            for x in range(GRID_SIZE_H):
                blocks = [row[x] for row in self.grid[y:y + 4]]
                all_red = all([self.is_red(block) for block in blocks])
                all_yellow = all([self.is_yellow(block) for block in blocks])
                all_blue = all([self.is_blue(block) for block in blocks])
                if all_red or all_yellow or all_blue:
                    is_checked = False
                    self.clear_vertical = True
                    if y + 4 <= GRID_SIZE_V:
                        item = self.grid[y + 4][x]
                        if (all_red and self.is_red(item)) or\
                           (all_blue and self.is_blue(item)) or\
                           (all_yellow and self.is_yellow(item)):
                            self.blocks_cleared.append([(y + i, x) for i in range(5)])
                            for i in range(5):
                                self.grid[y + i][x] = ITEM_BLANK
                            is_checked = True
                    if not is_checked:
                        self.blocks_cleared.append([(y + i, x) for i in range(4)])
                        for i in range(4):
                            self.grid[y + i][x] = ITEM_BLANK


    def get_blocks_in_air(self):
        # if len(self.blocks_cleared) > 0:
        #     print(self.blocks_cleared)

        self.blocks_cleared.clear()
        return []

    def handle_movement(self):
        # MOVE THE BAR AUTOMATICLY
        if self.elapsed_dropdown_time > self.dropdown_speed and self.direction is not DIRECTION_DOWN:
            self.current_bar.move(DIRECTION_DOWN)
            self.elapsed_dropdown_time = 0
            self.has_move = True

        # MOVE THE BAR ON INPUT
        if self.direction is not DIRECTION_NEUTRAL and self.elapsed_key_time > self.key_speed:
            self.current_bar.move(self.direction)
            self.elapsed_key_time = 0
            self.has_move = True

        # ROTATE THE BAR
        if self.rotation is not ROTATION_NEUTRAL:
            self.current_bar.rotate(self.rotation)
            self.rotation = ROTATION_NEUTRAL
            self.has_rotate = True

    def handle_reverse_movement(self):
        if self.has_move:
            self.current_bar.set_previous_position()
        if self.has_rotate:
            self.current_bar.set_previous_rotation()

    def handle_placing_bar(self):
        for block, x, y in self.current_bar.blocks():
            self.grid[y][x] = block.type

        self.next_bar()
        self.handle_clear_horizontal()
        self.handle_clear_vertical()
        self.handle_block_in_air()

    def handle_block_in_air(self):
        if self.clear_horizontal:
            print(self.blocks_cleared)
            self.blocks_to_drop = horizontal_tree_blocks(self.blocks_cleared[0], self.grid)
        elif self.clear_vertical:
            print(self.blocks_cleared)
            self.blocks_to_drop = vertical_tree_blocks(self.blocks_cleared[0], self.grid)

    def handle_dropping_block(self):
        for x, y in self.blocks_to_drop:
            current_block = self.grid[x][y]
            self.grid[x][y] = ITEM_BLANK
            self.grid[x - 1][y] = current_block
        self.blocks_to_drop = []

    def on_update(self, delta_time):
        if not self.is_playing:
            return False

        if self.elapsed_time >= self.game_speed:
            self.elapsed_time -= self.game_speed
            if len(self.blocks_to_drop) == 0:
                self.handle_movement()
                # self.blocks_to_drop = self.get_blocks_in_air()

                has_collide_left_and_right_boundary = self.is_bar_collide_with_left_right_boundary(
                )
                has_collide_with_bottom_boundary = self.is_bar_collide_with_bottom_boundary()
                has_collide_with_blocks = self.is_bar_collide_with_blocks()
                from_horizontal = self.direction == DIRECTION_LEFT or self.direction == DIRECTION_RIGHT

                if any([
                        has_collide_left_and_right_boundary, has_collide_with_bottom_boundary,
                        has_collide_with_blocks
                ]):
                    self.handle_reverse_movement()

                if any([has_collide_with_bottom_boundary, has_collide_with_blocks
                       ]) and not has_collide_left_and_right_boundary and not from_horizontal:
                    self.handle_placing_bar()
                    # print(self.grid)

                self.has_move = False
                self.has_rotate = False
            else:
                self.handle_dropping_block()

            self.update_grid()

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
        elif key == arcade.key.P:
            self.is_playing = not self.is_playing

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
