"""
Python Class & Abstraction

Topic above is a fancy way of saying hey, let’s talk about Object Oriented Programming-
although this time, we’ll be considering a recreational and competitive board game alongside
our program which will consist of objects in form of data, (things that’ll enable game play)
and methods- body of events/codes designed to uphold the rules and observe various intricacies
tailored to our board game.

Chess, it’s collectively regarded as an abstract strategy game involving no hidden
information. It is played on a squared-board with 64 neatly arranged squares in an 8x8 grid.
At the start, each player controls 16 pieces: 1king, 1queen, 2bishops, 2castles, 2knights, and 8pawns
whilst the objective is to checkmate either player’s king. During the game, players each
get a turn to move their choice piece either to an unoccupied square or one occupied by an
opponent’s piece, which is captured and removed from play. Each piece has its own unique way of moving,
which this article drills down on to demonstrate abstraction, and fashioned into a structured program
with a python type, class.

Let’s start with data, shall we? We need a way to represent each of those piece types mentioned earlier,
also, we need to be able to formulate some sort of squares/columns that’ll be used for movements
throughout the game. In other words we need to structure our data. Apart from king and queen piece, every
other type has at least two in total per player- the first player’s pieces are arranged on the first
two rows like this:
"""
row = 'abcdefgh'  # represents horizontal lines throughout the board
column = range(1, 2)  # represents vertical lines, 1st column

player_a = {
    'pawn': [(r, c) for r in row for c in range(2, 3)],  # second row
    'castle': [(r, c) for r in row[::7] for c in column],
    'knight': [(r, c) for r in row[1:-1:5] for c in column],
    'bishop': [(r, c) for r in row[2:-2:3] for c in column],
    'queen': [('d', 1)],
    'king': [('e', 1)],
}
"""
>>> print(player_a)
{'pawn': [('a', 2), ('b', 2), ('c', 2), ('d', 2), ('e', 2), ('f', 2), ('g', 2), ('h', 2)], 
'castle': [('a', 1), ('h', 1)], 
'knight': [('b', 1), ('g', 1)], 
'bishop': [('c', 1), ('f', 1)], 
'queen': [('d', 1)], 'king': [('e', 1)]}
"""
"""
On the other hand, structuring the opponent's piece involves an opposite arrangement to the 
other player's, so let's workout a reversed arrangement for the other player pieces
"""
column = range(8, 9)

player_b = {
    'pawn': [(r, c) for r in row[::-1] for c in range(7, 8)],
    'castle': [(r, c) for r in row[::7][::-1] for c in column],
    'knight': [(r, c) for r in row[1:-1:5][::-1] for c in column],
    'bishop': [(r, c) for r in row[2:-2:3][::-1] for c in column],
    'queen': [('d', 8)],
    'king': [('e', 8)],
}
"""
>>> print(player_b)
{'pawn': [('h', 7), ('g', 7), ('f', 7), ('e', 7), ('d', 7), ('c', 7), ('b', 7), ('a', 7)], 
'castle': [('h', 8), ('a', 8)], 
'knight': [('g', 8), ('b', 8)], 
'bishop': [('f', 8), ('c', 8)], 
'queen': [('d', 8)], 'king': [('e', 8)]}
"""
"""
Typically each key in our dictionaries maps to a container that allows mutability to be able to 
support our mutating actions like replacing a pawn for instance.
Now, we have a chessboard and all the pieces positioned ready for a game of chess. Time to 
write a class for our player objects, followed by some definitions of their interactions.
"""


class Chess:
    score = [0, 0]  # records each player's number of wins on all instances of Chess

    def __init__(self, a, b):
        """
        :param a: represents all pieces for player A
        :param b: represents all pieces for player B
        """
        self.a = a
        self.b = b
        self.all_moves = {
            'king': self.move_king,
            'queen': self.move_queen,
            'bishop': self.move_bishop,
            'knight': self.move_knight,
            'pawn': self.move_pawn,
            'castle': self.move_castle
        }
        self.start()  # begin the game

    def start(self):
        """
        each player starts with equal num of pieces, when start() is called
        it checks if the rotated player observing current turn has a king-
        if False, opponent wins
        :return:
        """
        while True:
            for player in (self.a, self.b):  # player is the one currently playing
                opponent = self.b if player == self.a else self.a
                turn = 'player A' if player == self.a else 'player B'
                if 'king' not in player:
                    turn = 'player B' if turn == 'player A' else 'player A'  # winner
                    print("%s wins" % turn)
                    return self
                else:
                    print(turn)
                    print('--------')
                    self.play(player, opponent)
                    print()
                continue

    def __str__(self):
        if 'king' not in self.a: self.score[1] += 1
        elif 'king' not in self.b: self.score[0] += 1
        return "playerA %d : %d playerB" % (self.score[0], self.score[1])

    def play(self, player: dict, opponent: dict) -> None:
        # decide which piece to move; king, queen, pawn etc
        # if any of its member is movable
        movable_types = []
        for key in player:
            for pc in player[key]:  # pc: piece
                move = self.all_moves[key]  # returns a list when bounded move is called
                if move(pc, player, opponent) and key not in movable_types:
                    movable_types.append(key)
        for piece in range(len(movable_types)):
            print(piece, movable_types[piece])
        choice_type = input("Enter the preceding num to your choice piece: ")
        if self.validate_input(choice_type) and int(choice_type) < len(movable_types):
            choice_type = movable_types[int(choice_type)]  # king, queen, or pawn etc
        else: raise Exception("%s is not part of the options" % choice_type)   # IndexError or ValueError
        func = self.all_moves[choice_type]  # returns a list when bounded func is called
        # actual movable pc in choice_type/key in (specifics)
        specifics = [pc for pc in player[choice_type] if func(pc, player, opponent)]
        for pc in range(len(specifics)):
            print(pc, specifics[pc])
        choice_pc = input("Enter the preceding num to your choice %s: " % choice_type)
        if self.validate_input(choice_pc) and int(choice_pc) < len(specifics):
            choice_pc = specifics[int(choice_pc)]  # pawn at a2, c2, or d2 etc
        else: raise Exception("%s is not part of the options" % choice_pc)
        # present moves, make move
        moves = self.all_moves[choice_type](choice_pc, player, opponent)
        for move in range(len(moves)):
            print(move, moves[move])
        choice_mv = input("Enter the preceding num to your choice move: ")
        if self.validate_input(choice_mv) and int(choice_mv) < len(moves):
            choice_mv = moves[int(choice_mv)]
        else: raise Exception("%s is not part of the options" % choice_mv)
        # when move is made, that piece changes column, if the piece knocks out
        # opponent's, the piece is withdrawn or becomes None in this instance
        self.replace_piece(player, choice_type, choice_pc, choice_mv)  # pc becomes move
        if choice_type == "pawn" and (choice_mv[1] == 1 or choice_mv[1] == 8):
            # choice_mv replaced choice_pc at this stage already,
            # so pop it and send it as arg
            choice_mv = player['pawn'].index(choice_mv)
            choice_mv = player['pawn'].pop(choice_mv)
            self.replace_pawn(player, choice_mv)
        # chance to knockout piece
        # each move method returns a list of all possible moves based on choice
        # piece, our interface filters this list to gather common moves for both
        # players into a separate list for confirmation on take_out_piece method call
        if choice_mv in [m for m in moves if m in self.all_pieces(opponent)]:
            for k, v in opponent.items():
                if choice_mv in v:
                    choice_type = k  # corresponding key for opponent's piece to pop
                    break
            self.take_out_piece(opponent, choice_type, choice_mv)
        return

    @staticmethod
    def validate_input(string):
        try:
            if int(string) == 0: return True
            else: return bool((int(string)))
        except ValueError as e: return

    @staticmethod
    def replace_piece(player: dict, key: str, pc: tuple, move: tuple):
        # index pc, insert move at index, pop pc at index+1
        pos = player[key].index(pc)
        player[key].insert(pos, move)
        player[key].pop(pos+1)
        return

    @staticmethod
    def all_pieces(player: dict):
        return [item for elem in player.values() for item in elem]

    @staticmethod
    def take_out_piece(opponent: dict, key: str, move: tuple):
        pos = opponent[key].index(move)
        opponent[key].pop(pos)
        if not opponent[key]: opponent.pop(key)

    @staticmethod
    def replace_pawn(player, pc):
        # if queen, reinstate other piece following priority_list else,
        # cede priority to queen piece, once you reclaim all super pieces- enjoy!
        priority_list = ['queen', 'bishop', 'knight', 'castle']
        if 'queen' in player:
            for key in priority_list[1:]:
                # has one type left
                if key in player and len(player[key]) < 2:
                    player[key].append(pc)
                    return
                else:
                    player[key] = [pc]
                    return
        elif 'queen' not in player: player['queen'] = [pc]
        return

    def move_pawn(self, choice_pc, player, opponent):
        """
        a pawn, at first move can leap 2 steps ahead with a consequent 1 following the first
        also, it can diagonally take out an opponent piece one step from its position
        this function returns a list of all possible moves 
        """
        from itertools import zip_longest

        num = choice_pc[1]  # consider choice_pc = ('a', 2)
        ri = row.index(choice_pc[0])  # ri: row index
        ro1 = row[ri-1:ri+2:2]
        ro2 = row[ri+1:ri+2]
        direction = 1 if player == self.a else -1
        col = range(num+direction, num+(direction*2))
        not_moved = bool(num == 2 or num == 7)
        pl_pcs = self.all_pieces(player)
        opponent_pcs = self.all_pieces(opponent)
        moves = []
        if not_moved:
            for m in zip([choice_pc[0]]*2, [num+direction, num+(direction*2)]):
                if m not in pl_pcs and m not in opponent_pcs:
                    moves.append(m)
                else: break
            if ri > 0:
                m1 = [m for m in zip_longest(ro1, col, fillvalue=num+direction)
                      if m in opponent_pcs]
            else:
                m1 = [m for m in zip_longest(ro2, col, fillvalue=num+direction)
                      if m in opponent_pcs]
        else:
            for m in zip(choice_pc[0], [num+direction]):
                if m not in pl_pcs+opponent_pcs:
                    moves.append(m)
                else: break
            if ri > 0:
                m1 = [m for m in zip_longest(ro1, col, fillvalue=num+direction)
                      if m in opponent_pcs]
            else:
                m1 = [m for m in zip_longest(ro2, col, fillvalue=num+direction)
                      if m in opponent_pcs]
        if m1: moves.extend(m1)
        moves[:] = [m for m in moves if 1 <= m[1] <= 8]
        return moves

    def move_castle(self, choice_pc: tuple, player: dict, opponent: dict):
        """
        a castle moves in a straight line in all four directions. our job is to pick
        all possible moves/columns whilst avoiding occupied columns, except its occupied by
        opponent's providing a knock out opportunity
        :param choice_pc:
        :param player:
        :param opponent:
        :return:
        """
        moves = []
        mid = row.index(choice_pc[0])
        ro1 = row[:mid][::-1]
        ro2 = row[mid+1:]
        h_co = range(choice_pc[1], choice_pc[1]-1, -1)   # horizontal column
        v_co1 = range(choice_pc[1]-1, 1, -1)  # -ve y axis
        v_co2 = range(choice_pc[1]+1, 9)
        pl_pcs = self.all_pieces(player)
        opponent_pcs = self.all_pieces(opponent)
        # moves horizontally
        for m in zip(ro1, list(h_co)*len(ro1)):
            if m not in pl_pcs and m in opponent_pcs:
                moves.append(m)
                break
            elif m not in pl_pcs and m not in opponent_pcs:
                moves.append(m)
                continue
            else: break
        for m in zip(ro2, list(h_co)*len(ro2)):
            if m not in pl_pcs and m in opponent_pcs:
                moves.append(m)
                break
            elif m not in pl_pcs and m not in opponent_pcs:
                moves.append(m)
                continue
            else: break
        # moves vertically
        for m in zip(choice_pc[0]*(choice_pc[1]-1), v_co1):
            if m not in pl_pcs and m in opponent_pcs:
                moves.append(m)
                break
            elif m not in pl_pcs and m not in opponent_pcs:
                moves.append(m)
                continue
            else: break
        for m in zip(choice_pc[0]*(choice_pc[1]-1), v_co2):
            if m not in pl_pcs and m in opponent_pcs:
                moves.append(m)
                break
            elif m not in pl_pcs and m not in opponent_pcs:
                moves.append(m)
                continue
            else: break
        moves[:] = [m for m in moves if 1 <= m[1] <= 8]
        return moves

    def move_knight(self, choice_pc, player, opponent):
        """
        knight moves are interesting, you could even pick out an octagon
        from a knight's maximum moves. take a step from the knight's position
        on both sides, step twice upwards and downwards, 4moves. take two steps
        from the knight's position on both sides, step upwards and downwards the
        other 4moves to complete 8 maximum moves. we'll also handle some intricate ones
        with our conditionals
        :param choice_pc:
        :param player:
        :param opponent:
        :return:
        """
        from itertools import chain

        mid = row.index(choice_pc[0])
        col = choice_pc[1]
        pl_pcs = self.all_pieces(player)
        if 1 < mid < 6:
            # here, maximum moves is possible as we pick two rows each, left and right of knight
            ro1 = row[mid-2:mid+3]
            # pop mid chr since there are no moves on that line
            ro1 = (lambda s: ''.join(s.split(ro1[2])))(ro1)
            # first fours
            mv1 = ((r, c) for r in ro1[::3] for c in range(col-1, col+2, 2)
                   if (r, c) not in pl_pcs if 1 <= c <= 8)
            mv2 = ((r, c) for r in ro1[1:-1] for c in range(col-2, col+4, 4)
                   if (r, c) not in pl_pcs if 1 <= c <= 8)
            moves = [m for m in chain(mv1, mv2)]
            return moves
        elif mid == 1:
            ro1 = row[mid-1:mid+3]
            ro1 = (lambda s: ''.join(s.split(ro1[1])))(ro1)
            mv1 = ((r, c) for r in ro1[:-1] for c in range(col-2, col+4, 4)
                   if (r, c) not in pl_pcs if 1 <= c <= 8)
            mv2 = ((r, c) for r in ro1[-1] for c in range(col-1, col+2, 2)
                   if (r, c) not in pl_pcs if 1 <= c <= 8)
            moves = [m for m in chain(mv1, mv2)]
            return moves
        elif mid == 6:
            ro1 = row[mid-2:]
            ro1 = (lambda s: ''.join(s.split(ro1[2])))(ro1)
            mv1 = ((r, c) for r in ro1[1:] for c in range(col-2, col+4, 4)
                   if (r, c) not in pl_pcs if 1 <= c <= 8)
            mv2 = ((r, c) for r in ro1[0] for c in range(col-1, col+2, 2)
                   if (r, c) not in pl_pcs if 1 <= c <= 8)
            moves = [m for m in chain(mv1, mv2)]
            return moves
        elif mid == 0:
            ro1 = row[1:3]
            mv1 = ((r, c) for r in ro1[0] for c in range(col-2, col+4, 4)
                   if (r, c) not in pl_pcs if 1 <= c <= 8)
            mv2 = ((r, c) for r in ro1[1] for c in range(col-1, col+2, 2)
                   if (r, c) not in pl_pcs if 1 <= c <= 8)
            moves = [m for m in chain(mv1, mv2)]
            return moves
        elif mid == 7:
            ro1 = row[-3:]
            ro1 = (lambda s: ''.join(s.split(ro1[2])))(ro1)
            mv1 = ((r, c) for r in ro1[0] for c in range(col-1, col+2, 2)
                   if (r, c) not in pl_pcs if 1 <= c <= 8)
            mv2 = ((r, c) for r in ro1[1] for c in range(col-2, col+4, 4)
                   if (r, c) not in pl_pcs if 1 <= c <= 8)
            moves = [m for m in chain(mv1, mv2)]
            return moves

    def move_bishop(self, choice_pc: tuple, player: dict, opponent: dict) -> list:
        """
        moves run through a bishop piece diagon-alley from left to right leaving
        us with 2 halves containing possible move for this piece
        :param choice_pc:
        :param player:
        :param opponent:
        :return:
        """
        opponent_pcs = self.all_pieces(opponent)
        pl_pcs = self.all_pieces(player)
        moves = []
        ri = row.index(choice_pc[0])  # row index
        mid = choice_pc[1]
        ro1 = row[ri-1::-1]  # first half
        ro2 = row[ri+1:]
        distance1 = len(ro1)  # from row[0] to pc[0]
        distance2 = len(ro2)
        co1 = range(mid+1, mid+distance1+1)  # 1st half column
        co2 = range(mid-1, 0, -1)
        co3 = range(mid+1, 1+mid+distance2)
        # first half
        zip1 = zip(ro1, co1)
        zip2 = zip(ro1, co2)
        if zip1:
            for m in zip1:
                if m not in pl_pcs and (m in opponent_pcs and 1 <= m[1] <= 8):
                    moves.append(m)
                    break
                elif m not in pl_pcs and (m not in opponent_pcs and 1 <= m[1] <= 8):
                    moves.append(m)
                    continue
                else: break  # accumulate possible empty columns, break when occupied
        if zip2:
            for m in zip2:
                if m not in pl_pcs and (m in opponent_pcs and 1 <= m[1] <= 8):
                    moves.append(m)
                    break
                elif m not in pl_pcs and (m not in opponent_pcs and 1 <= m[1] <= 8):
                    moves.append(m)
                    continue
                else: break
        # 2nd, diagon alley  :)
        zip1 = zip(ro2, co3)
        zip2 = zip(ro2, co2)
        if zip1:
            for m in zip1:
                if m not in pl_pcs and (m in opponent_pcs and 1 <= m[1] <= 8):
                    moves.append(m)
                    break
                elif m not in pl_pcs and (m not in opponent_pcs and 1 <= m[1] <= 8):
                    moves.append(m)
                    continue
                else: break
        if zip2:
            for m in zip2:
                if m not in pl_pcs and (m in opponent_pcs and 1 <= m[1] <= 8):
                    moves.append(m)
                    break
                elif m not in pl_pcs and (m not in opponent_pcs and 1 <= m[1] <= 8):
                    moves.append(m)
                    continue
                else: break
        return moves

    def move_queen(self, choice_pc, player, opponent):
        """
        well a queen got moves- with a reach sometimes extending up
        to a quarter of the board. its simply an addition of our bishop and
        castle moves
        :param choice_pc:
        :param player:
        :param opponent:
        :return:
        """
        return self.move_bishop(choice_pc, player, opponent) + \
            self.move_castle(choice_pc, player, opponent)

    def move_king(self, choice_pc, player, opponent):
        """
        a king has similar movement pattern to a queen albeit a step in all
        directions

        :param choice_pc:
        :param player:
        :param opponent:
        :return:
        """
        from itertools import chain

        pl_pcs = self.all_pieces(player)
        ri = row.index(choice_pc[0])
        ro1 = row[ri-1:ri+2]
        ro2 = row[ri:ri+2]
        ro3 = row[ri:ri-2:-1]
        col = range(choice_pc[1]-1, choice_pc[1]+2)
        if 0 < ri < 7:
            zip1 = zip([ro1[0]]*len(col), col)
            zip2 = zip([ro1[1]]*len(col), col)
            zip3 = zip([ro1[2]]*len(col), col)
            moves = [m for m in chain(zip1, zip2, zip3) if m != choice_pc
                     if m not in pl_pcs if 1 <= m[1] <= 8]
            return moves
        elif ri == 7:
            zip1 = zip([ro3[0]]*len(col), col)
            zip2 = zip([ro3[1]]*len(col), col)
            moves = [m for m in chain(zip1, zip2) if m != choice_pc
                     if m not in pl_pcs if 1 <= m[1] <= 8]
            return moves
        else:
            zip1 = zip([ro2[0]]*len(col), col)
            zip2 = zip([ro2[1]]*len(col), col)
            moves = [m for m in chain(zip1, zip2) if m != choice_pc
                     if m not in pl_pcs if 1 <= m[1] <= 8]
            return moves

"""
Okay, that was some lines and it could easily be furthered considering methods like 
move_pawn_to_king_side() is missing. However, all our codes so far is sufficient to demonstrate 
abstraction in computer programming which is certainly at the core of OOP.
In this article, we looked at how to structure chess data for both players on a board, and 
a definition of how these data are affected during a game of chess. For an easier read,
checkout the complete code on github.
"""