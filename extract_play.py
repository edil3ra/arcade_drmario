from wand.image import Image
import matplotlib.pyplot as plt


img = Image(filename="assets/tetris_dr_mario_sprites_virus.png")

def make_block():
    pad_left = 0
    pad_top = 40

    width = 20
    height = 20

    offset_x = 40
    offset_y = 25

    size_x = 3
    size_y = 3


    for h_count in range(size_y):
        for w_count in range(size_x):
            start_x = (w_count * offset_x) + pad_left
            end_x = start_x + width
            start_y = (h_count * offset_y) + pad_top
            end_y = start_y + height
            with img[start_x:end_x, start_y:end_y] as chunk:
                chunk.save(filename='assets/block_y{}_x{}.jpg'.format(h_count, w_count))


def make_virus():
    size_x = 10
    size_y = 10

    blue_x = 5
    blue_y = 0

    with img[blue_x:blue_x+size_x, blue_y:blue_y+size_y] as chunk:
        chunk.save(filename='assets/blue1.jpg')
        
    blue_y = 20
    with img[blue_x:blue_x+size_x, blue_y:blue_y+size_y] as chunk:
        chunk.save(filename='assets/blue2.jpg')



    size_x = 10
    size_y = 10

    red_x = 135
    red_y = 0

    with img[red_x:red_x+size_x, red_y:red_y+size_y] as chunk:
        chunk.save(filename='assets/red1.jpg')
        
    red_y = 20
    with img[red_x:red_x+size_x, red_y:red_y+size_y] as chunk:
        chunk.save(filename='assets/red2.jpg')


    size_x = 10
    size_y = 10

    yellow_x = 135 + 130
    yellow_y = 0

    with img[yellow_x:yellow_x+size_x, yellow_y:yellow_y+size_y] as chunk:
        chunk.save(filename='assets/yellow1.jpg')
        
    yellow_y = 20
    with img[yellow_x:yellow_x+size_x, yellow_y:yellow_y+size_y] as chunk:
        chunk.save(filename='assets/yellow2.jpg')
