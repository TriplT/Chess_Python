def get_piece_pos(pos):
    file = 'abcdefgh'
    rank = '12345678'
    a = b = 0
    for index_2, char in enumerate(file):
        if char == pos[0]:
            b = index_2
    for index_1, num in enumerate(rank):
        if num == pos[1]:
            a = index_1
    return a*8 - (8-b)

# example: print(get_piece_pos('c4')
