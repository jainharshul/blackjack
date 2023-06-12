#! /usr/bin/env python3
# Harshul Jain
# harshul@csu.fullerton.edu
# @jainharshul

"""A BlackJack Game"""

from blackjackgame.game import BJGame


def main():
    """Game entry point; all code is in the directory blackjackgame"""
    num = int(input("Enter the number of players: "))
    game = BJGame(num)
    game.initialize_players()
    game.play()


if __name__ == "__main__":
    main()
