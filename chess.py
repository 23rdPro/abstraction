from itertools import zip_longest, chain
from operator import itemgetter


class Chess:
    """
    what better way to abstract than to trace
    movement patterns on a chess board?
    """
    # we have two class variables:
    # row is immutable and available as is to all our Chess instance,
    # score records each player's number of wins on all instances of Chess
    row = 'abcdefgh'
    score = [0, 0]

    def __init__(self, a: dict, b: dict):
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
        self.start()

    def __str__(self):
        if 'king' not in self.a: self.score[1] += 1
        elif 'king' not in self.b: self.score[0] += 1
        return "playerA %d : %d playerB" % (self.score[0], self.score[1])

    def start(self):
        """
        each player starts with equal num of pieces, when start() is called
        it checks if the rotated player observing current turn has a king-
        if False, opponent wins

        each move method returns a list of all possible moves based on choice
        piece, our interface filters this list to gather common moves for both
        players into a separate list for confirmation on take_out_piece method
        call
        :return:
        """
        while True:
            for player in (self.a, self.b):  # player is the one currently playing
                opponent = self.b if player == self.a else self.a
                turn = 'player A' if player == self.a else 'player B'
                print(self.a)
                print(self.b)
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

    def play(self, player, opponent):
        # decide which piece to move; king, queen, pawn etc
        # if any of its member is movable
        movable_types = []
        for key in player:
            for pc in player[key]:  # pc: piece
                move = self.all_moves[key]
                # every member type that is movable in the list
                if move(pc, player, opponent) and key not in movable_types:
                    movable_types.append(key)
        for piece in range(len(movable_types)):
            print(piece, movable_types[piece])  # present movable member type
        choice_type = input("Enter the preceding num to your choice piece: ")
        if self.validate_input(choice_type) and int(choice_type) < len(movable_types):
            choice_type = movable_types[int(choice_type)]  # king, queen, or pawn etc
        else: raise Exception("%s is not part of the options" % choice_type)   # IndexError or ValueError
        func = self.all_moves[choice_type]
        # actual movable pc in choice_type or key
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
        # opponent's, the piece is withdrawn or becomes None
        self.replace_piece(player, choice_type, choice_pc, choice_mv)  # pc becomes move
        if choice_type == "pawn" and (choice_mv[1] == 1 or choice_mv[1] == 8):
            # choice_mv replaced choice_pc at this stage,
            # so pop it and send it as arg
            choice_mv = player['pawn'].index(choice_mv)
            choice_mv = player['pawn'].pop(choice_mv)
            self.replace_pawn(player, choice_mv)
        # chance to knockout piece
        # if choice_mv was popped, its still choice_mv- important!
        if choice_mv in [m for m in moves if m in self.all_pieces(opponent)]:
            for k, v in opponent.items():
                if choice_mv in v:
                    choice_type = k  # corresponding key for opponent's piece
                    break
            self.take_out_piece(opponent, choice_type, choice_mv)
        return

    # @staticmethod
    # def replace_pawn(player, pc):
    #     priority_list = ['queen', 'bishop', 'knight', 'castle']
    #     if 'queen' in player:
    #         for k in priority_list[1:]:
    #             if k in player:
    #                 num_pc = (lambda d, x: len(d[x]))(player, k)
    #                 if num_pc < 2:
    #                     player[k].append(pc)
    #                     return
    #                 continue
    #             elif k not in player:
    #                 player[k] = [pc]
    #                 return
    #     else: player['queen'] = [pc]
    #     return

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

    @staticmethod
    def validate_input(string):
        try:
            if int(string) == 0: return True
            else: return bool((int(string)))
        except ValueError as e: return

    @staticmethod
    def take_out_piece(opponent, key, move):
        pos = opponent[key].index(move)
        opponent[key].pop(pos)
        if not opponent[key]: opponent.pop(key)

    @staticmethod
    def replace_piece(player: dict, key: str, pc: tuple, move: tuple):
        # index pc, insert at index, pop at index+1
        pos = player[key].index(pc)
        player[key].insert(pos, move)
        player[key].pop(pos+1)
        return

    @staticmethod
    def all_pieces(player: dict):
        return [item for elem in player.values() for item in elem]

    # def priority_move(self, moves, opponent, choice_pc):
    #     # basically, exclude the one piece so you can include it
    #     # as the only possible piece available for knockout
    #     opponent_pcs = self.all_pieces(opponent)
    #     mvs = list(set(moves) & set(opponent_pcs))  # present in both players'
    #     if mvs:
    #         mvs.sort(key=itemgetter(1))
    #         if choice_pc[1] < mvs[0][1]:
    #             mvs.pop(0)
    #             return mvs
    #         elif choice_pc[1] > mvs[-1][1]:
    #             mvs.pop()
    #             return mvs
    #     else: return

    def move_pawn(self, choice_pc, player, opponent):
        row = self.row
        num = choice_pc[1]
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
            if ri > 0:  # when pc[0] is  `a`
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

    def move_castle(self, choice_pc, player, opponent):
        row = self.row
        moves = []
        mid = row.index(choice_pc[0])
        ro1 = row[:mid][::-1]
        ro2 = row[mid+1:]
        h_co = range(choice_pc[1], choice_pc[1]-1, -1)   # horizontal column
        v_co1 = range(choice_pc[1]-1, 1, -1)
        v_co2 = range(choice_pc[1]+1, 9)
        pl_pcs = self.all_pieces(player)
        opponent_pcs = self.all_pieces(opponent)
        # horizontally
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
        # vertically
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
        row = self.row
        mid = row.index(choice_pc[0])
        col = choice_pc[1]
        pl_pcs = self.all_pieces(player)
        if 1 < mid < 6:
            ro1 = row[mid-2:mid+3]
            ro1 = (lambda s: ''.join(s.split(ro1[2])))(ro1)  # mid chr since there are no moves on that line
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

    def move_bishop(self, choice_pc, player, opponent):
        opponent_pcs = self.all_pieces(opponent)
        pl_pcs = self.all_pieces(player)
        row = self.row
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
        return self.move_bishop(choice_pc, player, opponent) + \
               self.move_castle(choice_pc, player, opponent)

    def move_king(self, choice_pc, player, opponent):
        pl_pcs = self.all_pieces(player)
        row = self.row
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
