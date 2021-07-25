row = 'abcdefgh'
n = len(row)

player_A = {
    'pawn': [(r, c) for r in row for c in range(2, 3)],
    'castle': [(r, c) for r in row[0:n:7] for c in range(1, 2)],
    'knight': [(r, c) for r in row[1:n-1:5] for c in range(1, 2)],
    'bishop': [(r, c) for r in row[2:n-2:3] for c in range(1, 2)],
    'queen': [('d', 1)],
    'king': [('e', 1)]
}
player_B = {
    'pawn': [(r, c) for r in row[::-1] for c in range(7, 8)],
    'castle': [(r, c) for r in row[n-1::-7] for c in range(8, 9)],
    'knight': [(r, c) for r in row[n-2::-5] for c in range(8, 9)],
    'bishop': [(r, c) for r in row[n-3::-3] for c in range(8, 9)],
    'queen': [('d', 8)],
    'king': [('e', 8)]
}


if __name__ == '__main__':
    from chess import Chess
    # dx = Chess(player_A, player_B)
    # print(dx)


"""
Given 8x8 chessboard, write a function to determine how many moves it would take for a bishop to go from a start
location to an end location. Then write a function to determine how many spaces it would move
"""


def move_bishop(start: tuple, end: tuple) -> int:
    r = row.index(start[0])  # member row
    r_end = row.index(end[0])  # figure which side end is on
    if r == r_end: return 0
    mid = start[1]  # between up and down
    distance1 = len(row[:r])  # to the left
    distance2 = len(row[r+1:])  # right
    ro1 = row[:r][::-1]
    ro2 = row[r+1:]
    down_co = range(mid-1, 0, -1)  # column
    co1 = range(mid+1, mid+distance1+1)
    co2 = range(mid+1, mid+distance2+1)
    direction = 1 if start[1] < end[1] else -1  # up or down
    moves = None
    if r_end < r and direction > 0: moves = zip(ro1, co1)
    elif r_end > r and direction > 0: moves = zip(ro2, co2)
    elif r_end < r and direction < 0: moves = zip(ro1, down_co)
    elif r_end > r and direction < 0: moves = zip(ro2, down_co)
    if moves: moves = list(moves)
    else: raise Exception('Well...')  # :(
    if end in moves:
        return moves.index(end)+1
    return 0


print(move_bishop(('d', 4), ('a', 7)))
