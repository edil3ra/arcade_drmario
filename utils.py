def vertical_tree_blocks(blocks, grid):
    grid_left = [(y, x - 1) for y, x in blocks]
    grid_right = [(y, x + 1) for y, x in blocks]
    returned_blocks = []
    for block in grid_left:
        returned_blocks.append(block)

    for block in grid_right:
        returned_blocks.append(block)

    return list(set(returned_blocks))


def horizontal_tree_blocks(blocks, grid):
    grid_top = [(y + 1, x) for y, x in blocks]
    returned_blocks = []

    for block in grid_top:
        returned_blocks.append(block)

    return list(set(blocks))


def block_from_node(node, grid, taken=[]):
    y, x = node
    node_left = (y, x - 1)
    node_right = (y, x + 1)
    node_top = (y + 1, x)

    node_left_value = grid[node_left[0]][node_left[1]]
    node_right_value = grid[node_right[0]][node_right[1]]
    node_top_value = grid[node_top[0]][node_top[1]]

    if not (x - 1 < 0 or node_left_value == 0):
        if node_left not in taken:
            return block_from_node(node_left, grid, [*taken, node_left])

    if not (x + 1 > 10 or node_right_value == 0):
        if node_right not in taken:
            return block_from_node(node_right, grid, [*taken, node_right])

    if not (y + 1 > 30 or node_top_value == 0):
        if node_top not in taken:
            return block_from_node(node_top, grid, [*taken, node_top])

    return taken
