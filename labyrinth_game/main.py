#!/usr/bin/env python3

from .constants import ROOMS
from .utils import describe_current_room
from .player_actions import get_input

def main():
    game_state = {
    'player_inventory': [], # Инвентарь игрока
    'current_room': 'entrance', # Текущая комната
    'game_over': False, # Значения окончания игры
    'steps_taken': 0 # Количество шагов
    }

    print("Добро пожаловать в Лабиринт сокровищ!")

    describe_current_room(game_state)

    while not game_state['game_over']:
        command = get_input("\nВведите команду: ").lower()
if __name__ == "__main__":
    main()
  