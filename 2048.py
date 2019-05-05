# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 22:14:48 2019

@author: Martini
"""

import random
import os
# import curses

# 保存棋盘状态
board = [
    [0, 0, 0, 0],   # Line 1
    [0, 0, 0, 0],   # Line 2
    [0, 0, 0, 0],   # Line 3
    [0, 0, 0, 0]    # Line 4
]

# wasd 为上下左右，q 退出，r 重新开始， x 初始状态
last_move = 'x'
# 结束状态定义
CONTINUE, WIN, LOSE = range(3)
status = CONTINUE   # 默认为继续
valid = True     # 表示输入是否有效


def new_game():
    # Add new numbers with 90% chances of 2 and 10% chances of 4
    global board, status, last_move
    status = CONTINUE
    board = [
            [0, 0, 0, 0],   # Line 1
            [0, 0, 0, 0],   # Line 2
            [0, 0, 0, 0],   # Line 3
            [0, 0, 0, 0]    # Line 4
    ]
    empty_space = list()
    for i in range(4):
        for j in range(4):
            empty_space.append((i, j))
    new_spaces = random.sample(empty_space, k=5)    # Get 5 random spaces
                                                    # without replacement
    for new_space in new_spaces:
        new_tile = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
        board[new_space[0]][new_space[1]] = new_tile    # Fill new number
    last_move = 'x'                                 # Reset  last_move
#    check_movable()


# def test1():
#    new_game()
#    print(board)
#
#
# test1()


def check_move_down():
    # If empty space was found in board[3] which is the bottom line,return True
    # If a number is equal to the number below it, return True
    # Check from top to bottom
    # Return can move or cannot move
    for i in range(4):
        for j in range(3):
            if board[j][i] == board[j+1][i] > 0:
                return True
            if board[j][i] > 0 and board[j+1][i] == 0:
                return True
    return False                    # Return the possibility of movement
##
#   How to use it?
##


def move_down():
    """
    top_index 为“被对比的对象”，根据 j 与 top_index 上数字的关系判断动作，若
    top_index 未被处理，则 j-1，进行 j 的下一次比较；若 top_index 已被处理，则不用
    再次处理，top_index-1，进行下一次比较。
    Return WIN or NOT
    """
    global status
    for i in range(4):
        top_index = 3
        for j in range(2, -1, -1):  # (2, 1, 0) from 2 to -1, step = -1
            if board[j][i] == 0:    # From Line3 to Line1 cos Line4 isunmovable
                continue            # Skip empty tiles
            if board[top_index][i] == board[j][i]:  # Merge equivalent tiles
                board[top_index][i] *= 2            # Merge
                board[j][i] = 0
                if board[top_index][i] == 32:      # WIN when 2048 appears
                    status = WIN
                    return True
                top_index -= 1
                continue
            if board[top_index][i] == 0:    # Line 4 is empty
                board[top_index][i] = board[j][i]   # Move down
                board[j][i] = 0
                continue
            else:                           # Different from sample
                top_index -= 1
                continue
    status = CONTINUE
    return False                            # Return WIN or NOT


def new_number():
    new_tile = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
    empty_space = list()
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                empty_space.append([i, j])
    new_space = random.choice(empty_space)
    board[new_space[0]][new_space[1]] = new_tile


def transpose():                            # 转置
    global board
    new_board = [
                [0, 0, 0, 0],   # Line 1
                [0, 0, 0, 0],   # Line 2
                [0, 0, 0, 0],   # Line 3
                [0, 0, 0, 0]    # Line 4
                ]
    for i in range(4):
        for j in range(4):
            new_board[i][j] = board[j][i]
    board = new_board


def vertical_flip():
    global board
    board = list(reversed(board))


def check_move_up():
    vertical_flip()
    result = check_move_down()
    vertical_flip()
    return result


def move_up():
    vertical_flip()
    result = move_down()
    vertical_flip()
    return result


def check_move_left():
    transpose()
    vertical_flip()
    result = check_move_down()
    vertical_flip()
    transpose()
    return result


def move_left():
    transpose()
    vertical_flip()
    result = move_down()
    vertical_flip()
    transpose()
    return result


def check_move_right():
    transpose()
    result = check_move_down()
    transpose()
    return result


def move_right():
    transpose()
    result = move_down()
    transpose()
    return result


valid_next_move = {
        'up': True,
        'down': True,
        'left': True,
        'right': True
        }


def check_movable():
    # Return LOSE or NOT
    global valid_next_move, status, valid
    if status == WIN:
        return 0
    valid_next_move = {
        'up': check_move_up(),
        'down': check_move_down(),
        'left': check_move_left(),
        'right': check_move_right()
        }
    if True in valid_next_move.values():
        status = CONTINUE
    else:
        status = LOSE


'''
┏━┳━┓   ┏ ━ ┳ ━ ┓
┣━╋━┫   ┣ ━ ╋ ━ ┫  ┃
┗━┻━┛   ┗ ━ ┻ ━ ┛
'''


def get_board():
    # Display board
    # Return string of board
    result = '┏' + ('━' * 5 + '┳') * 3 + '━' * 5 + '┓\n'
    result += f'┃{board[0][0]:^5}┃{board[0][1]:^5}┃{board[0][2]:^5}┃\
{board[0][3]:^5}┃\n'
    for i in range(1, 4):
        result += '┣' + ('━' * 5 + '╋') * 3 + '━' * 5 + '┫\n'
        result += f'┃{board[i][0]:^5}┃{board[i][1]:^5}┃{board[i][2]:^5}┃\
{board[i][3]:^5}┃\n'
    result += '┗' + ('━' * 5 + '┻') * 3 + '━' * 5 + '┛\n'
    return result


def last_input():
    # Record last move
    # Return string of last move
    result = f'上一步： {last_move}\n'
    if status == LOSE:
        result += 'You have lost :('
    elif not valid:
        result += 'Invalid movement'
    elif status == CONTINUE:
        result += 'Continue'
    elif status == WIN:
        result = '牛逼！！！'
    return result


def print_screen():
    os.system('cls')    # Clear screen
    print(get_board())
    print(last_input())


def input_prompt():
    # Process input prompt
    # Return input
    if status == CONTINUE:
        return input('<Q> Quit <R> Restart: ')
    else:
        return input('Q for Quit, R for Restart: ')


def validate_input(input_key):
    # Check the validation of input
    # Return valid or not
    global last_move, valid
    if status in (WIN, LOSE):   # Game Over
        if input_key in ('q', 'r'):
            last_move = input_key
            valid = True
            return True
    elif input_key in ('w', 'a', 's', 'd', 'q', 'r'):
        last_move = input_key
        if last_move == 'w':
            valid = valid_next_move['up']
        elif last_move == 'a':
            valid = valid_next_move['left']
        elif last_move == 's':
            valid = valid_next_move['down']
        elif last_move == 'd':
            valid = valid_next_move['right']
        elif last_move in ('q', 'r'):
            valid = True
        else:
            valid = False
    else:
        valid = False
    return valid


def do_move():
    if last_move == 'w':
        move_up()
    elif last_move == 'a':
        move_left()
    elif last_move == 's':
        move_down()
    elif last_move == 'd':
        move_right()


def new_or_exit():
    if last_move == 'q':
        exit()
    elif last_move == 'r':
        new_game()


def main():
    new_game()
    while True:
        print_screen()
        input_key = input_prompt()
        validate_input(input_key)
        if not valid:
            continue
        if last_move in ('q', 'r'):
            new_or_exit()
        else:
            do_move()
            new_number()
            check_movable()


main()
