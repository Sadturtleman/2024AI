import numpy as np


pieces = [(i, j, k, l) for i in range(2) for j in range(2) for k in range(2) for l in range(2)]  # All 16 pieces


def check_win(board):
    def check_line(line):
        if 0 in line:
            return False  # Incomplete line
        characteristics = np.array([pieces[piece_idx - 1] for piece_idx in line])
        for i in range(4):  # Check each characteristic (I/E, N/S, T/F, P/J)
            if len(set(characteristics[:, i])) == 1:  # All share the same characteristic
                return True
        return False

    def check_2x2_subgrid_win(board):
        for r in range(4 - 1):
            for c in range(4 - 1):
                subgrid = [board[r][c], board[r][c+1], board[r+1][c], board[r+1][c+1]]
                if 0 not in subgrid:  # All cells must be filled
                    characteristics = [pieces[idx - 1] for idx in subgrid]
                    for i in range(4):  # Check each characteristic (I/E, N/S, T/F, P/J)
                        if len(set(char[i] for char in characteristics)) == 1:  # All share the same characteristic
                            return True
        return False
    # Check rows, columns, and diagonals

    for col in range(4):
        if check_line([board[row][col] for row in range(4)]):
            return True
    
    for row in range(4):
        if check_line([board[row][col] for col in range(4)]):
            return True
        
    if check_line([board[i][i] for i in range(4)]) or check_line([board[i][4 - i - 1] for i in range(4)]):
        return True

    # Check 2x2 sub-grids
    if check_2x2_subgrid_win(board):
        return True
    
    return False

def find_checkmate_place(board : list[list], piece : tuple, availplace : list[tuple]) -> tuple:
    answer = list()
    for row, col in availplace:
        board[row][col] = pieces.index(piece) + 1
        if check_win(board):
            answer.append((row, col))
        board[row][col] = 0

    if len(answer) != 0:
        return answer
    return False

def find_notcheckmate_piece(board : list[list], availpiece : list[tuple], availplace : list[tuple]) -> list:

    answer = set()
    
    for piece in availpiece:
        for row, col in availplace:
            board[row][col] = pieces.index(piece) + 1
            if check_win(board):
                answer.add(piece)
                board[row][col] = 0
                break
            board[row][col] = 0
    
    return list(set(availpiece) - answer)

def find_three(board):
    def check_three_line(line):
        # 0~3인덱스의 어떤 원소가 같은지 출력

        '''
    [[1 1 0 0]
    [0 1 0 0]
    [9 9 9 9]
    [1 1 0 1]]
    [(1, 1), (2, 0)]
        '''
        answer = list()
        if line.count(0) != 1:
            return False  # Incomplete line
        characteristics = np.array([pieces[piece_idx - 1] if piece_idx != 0 else (9, 9, 9, 9) for piece_idx in line])
        for i in range(4):  # Check each characteristic (I/E, N/S, T/F, P/J)
            element, counts = np.unique(characteristics[:, i], return_counts = True)

            if np.any(counts == 3):
                temp = [9, 9, 9, 9]
                temp[i] = element[counts == 3][0]
                answer.append([temp])
        
        if len(answer) != 0:
            return answer
        return False

    def check_three_2x2_subgrid(board):
        answer = list()

        for r in range(4 - 1):
            for c in range(4 - 1):
                subgrid = [board[r][c], board[r][c+1], board[r+1][c], board[r+1][c+1]]
                if subgrid.count(0) == 1:  # cells fill in 3
                    characteristics = [pieces[idx - 1] if idx != 0 else (9, 9, 9, 9) for idx in subgrid]
                    for i in range(4):  # Check each characteristic (I/E, N/S, T/F, P/J)      
                        for item in set(char[i] for char in characteristics):
                            if [char[i] for char in characteristics].count(item) == 3:

                                temp = [9, 9, 9, 9]
                                temp[i] = item

                                x = subgrid.index(0)
                                a,b = r + x // 2, c + x % 2
                                answer.append([temp, (a, b)])
        if len(answer) != 0:
            return answer
        
        return False
    
    answer = list()

    for col in range(4):
        temp = disputelist(check_three_line([board[row][col] for row in range(4)]))

        for t in temp:
            r = [board[row][col] for row in range(4)].index(0)
            t.append((r, col))
            answer.append(t)

    for row in range(4):
        temp = disputelist(check_three_line([board[row][col] for col in range(4)]))
        
        for t in temp:
            c = [board[row][col] for col in range(4)].index(0)            
            t.append((row, c))
            answer.append(t)


    temp = disputelist(check_three_line([board[i][i] for i in range(4)]))

    
    for t in temp:
        
        i = [board[i][i] for i in range(4)].index(0)
        t.append((i, i))
        answer.append(t)

    temp = disputelist(check_three_line([board[i][4 - i - 1] for i in range(4)]))

    for t in temp:
        i = [board[i][4 - i - 1] for i in range(4)].index(0)
        t.append((i, 4 - i - 1))
        answer.append(t)
    # Check 2x2 sub-grids
    temp = disputelist(check_three_2x2_subgrid(board))
    answer.extend(temp)

    # False 제거 및 모든 리스트 내부의 튜플 풀기

    if len(answer) == 0:
        return False
    
    return answer

def disputelist(ls : list) -> list:
    if ls:
        return ls
    
    return []

def find_piece_by_point(board : list[list], availpiece : list) -> list[tuple]:

    data = find_three(board)
    ans = list()

    for point in data:
        ans.append(find_power_otherattr(point[0], availpiece))

    return ans

def find_power_otherattr(point : tuple, availpiece):
    answer = 0
    if 1 in point:
        p = (point.index(1), 0)
    else:
        p = (point.index(0), 1)

    for piece in availpiece:
        if piece[p[0]] == p[1]:
            answer += 1
    
    return answer


# piece, (row, col)

testboard = [[ 5,  0, 15,  0],
 [ 0,  8,  0,  0],
 [ 2,  0,  0,  0],
 [ 4, 14,  3,  7]]


[['0100', '0000', '1110', '0000'],
 ['0000', '0111', '0000', '0000'],
 ['0001', '0000', '0000', '0000'],
 ['0011', '1101', '0010', '0110']]


availpiece = [
    (0, 0, 0, 0),
    (0, 1, 0, 1),
    (1, 0, 0, 0),
    (1, 0, 0, 1),
    (1, 0, 1, 0),
    (1, 0, 1, 1),
    (1, 1, 0, 0),
    (1, 1, 1, 1)
]
