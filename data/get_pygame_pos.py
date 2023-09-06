def get_pygame_pos(pos, screen_x, screen_y, square_size):
    file = 'abcdefgh'
    rank = '12345678'
    a = b = 0
    for index_2, char in enumerate(file):
        if char == pos[0]:
            b = index_2
    for index_1, num in enumerate(rank):
        if num == pos[1]:
            a = index_1
    x = screen_x / 2 - 4 * square_size
    y = screen_y / 2 + 3 * square_size
    return x + (a * square_size), y - (b * square_size)


print(get_pygame_pos('d3', 1920, 1080, 100))
