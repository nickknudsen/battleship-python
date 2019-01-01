import os
import sys
from string import ascii_lowercase

from .battleship import Game
from .exceptions import InvalidPosition


LETTERS = {letter: str(index) for index, letter in enumerate(ascii_lowercase, start=0)}
NUMBERS = {index: letter for index, letter in enumerate(ascii_lowercase, start=0)}


def print_board(board, points, shots, time_elapsed):
    os.system('clear')
    print('\nPoints: ', points, end="     ")
    print('Shots Available: ', shots, end="     ")
    print('Time elapsed: {} sec'.format(int(time_elapsed)), end="\n")
    print('-' * 90)
    # Table Header
    print('| ', end='')
    print('{:<3}'.format('-'), end='')
    for i in range(board.COLS):
        print('| ', end='')
        print('{:<3}'.format(i), end='')
    print('| ', end='\n')
    print('-' * 90)
    # Table Body
    for i, row in enumerate(board.matrix):
        print('| ', end='')
        print('{:<2}'.format(NUMBERS[i]), end=" | ")
        for col in row:
            if col['shooted']:
                if not col['ship']:
                    print('{:<2}'.format('O'), end=" | ")
                else:
                    print('{:<2}'.format(col['ship'].initials), end=" | ")
            else:
                print('{:<2}'.format('.'), end=" | ")

        print()

    print('-' * 90)
    print('Labels')
    print('-' * 7)
    for ship in board.ships:
        text = '<{}> \t length: {} \t| initials: {} \t| Hits: {} | sunk: {}'
        print(text.format(
            ship.name.title(),
            ship.length,
            ship.initials,
            ship.hits,
            'yes' if ship.sink else 'no'
        ))

    print()
    print('-' * 90)


def print_ship_hit(ship_hit, points, shots, time_elapsed):
    os.system('clear')
    print('\nPoints: ', points, end="     ")
    print('Shots Available: ', shots, end="     ")
    print('Time elapsed: {} sec'.format(int(time_elapsed)), end="\n")
    print('-' * 90)
    print('\n\n\n\n')
    if ship_hit.sink:
        print('\t\t\t You Destroy a {}'.format(ship_hit.name.title()))
    else:
        print('\t\t\t You Hit a {}'.format(ship_hit.name.title()))

    print('\n\n\n\n')
    input("Press Enter to continue...")


def print_status(game):
    os.system('clear')
    print('\nPoints: ', game.points, end="     ")
    print('Lost Shots: ', game.lost_shot, end="     ")
    print('Right Shots: ', game.lost_shot, end="     ")
    print('Shots Missing: ', game.shots, end="\n")
    print('-' * 90)
    print('Sunken Ships: ', game.board.sunken_ships, end="     ")
    print('Missing Ships: ', game.board.total_ships - game.board.sunken_ships, end="   ")
    print('Time elapsed: {} sec'.format(int(game.time_elapsed)), end="\n")
    print('-' * 90)
    for s in game.board.ships:
        print('<{}> \t Sunk: {} \t| Hits: {}'.format(
            s.name.title(),
            'yes' if s.sink else 'no',
            s.hits
        ))

    print('-' * 90)


def main():
    game = Game()
    print_board(game.board, game.points, game.shots, game.time_elapsed)

    while True:
        while True:
            try:
                print('Press CTRL+C to exit ...')
                result = input('Choose your coordinates. Ex: a1, b15: c10 \n\nCoordinates: ').strip()

                x = int(LETTERS[result[0].lower()])
                y = int(result[1:].strip())

                if (x > 16 and x < 0) or (y > 16 and y < 0):
                    raise InvalidPosition()

                is_valid, ship = game.play(x, y)
                if is_valid:
                    print_ship_hit(ship, game.points, game.shots, game.time_elapsed)
                    break

                print_board(game.board, game.points, game.shots, game.time_elapsed)

                if game.end_game():
                    sys.exit(print_status(game))

            except Exception as exc:
                os.system('clear')
                print(str(exc))
                input('\n\n\n\t\t\tYou can only use letters and numbers. Ex: a1, c10, etc...')
                print_board(game.board, game.points, game.shots, game.time_elapsed)
            except KeyboardInterrupt:
                sys.exit(print_status(game))

        print_board(game.board, game.points, game.shots, game.time_elapsed)

