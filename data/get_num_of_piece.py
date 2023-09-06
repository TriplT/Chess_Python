def get_num_of_piece(piece):
    piece_type = piece[2:]
    piece_colour = piece[:1]
    num = 0
    match piece_type:
        case 'King':
            num += 1
        case 'Pawn':
            num += 2
        case 'Knight':
            num += 3
        case 'Bishop':
            num += 4
        case 'Rook':
            num += 5
        case 'Queen':
            num += 6
    match piece_colour:
        case 'W':
            num += 8
        case 'B':
            num += 16
    return num


# example: print(get_num_of_piece('W_Rook'))
