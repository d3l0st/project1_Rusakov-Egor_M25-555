#!/usr/bin/env python3

from .constants import ROOMS
from .utils import describe_current_room
from .player_actions import get_input, move_player, take_item   

def process_command(game_state, command):
    parts = command.lower().split()
    if not parts:
        return True
    action = parts[0]
    argument = parts[1] if len(parts) > 1 else None

    match action:
        case 'quit':
            print("\nСпасибо за игру! До свидания!")
            return False
        case 'look':
            describe_current_room(game_state)
        case 'inventory':
            if game_state['inventory']:
                print(f"\nВаш инвентарь: {', '.join(game_state['inventory'])}")
            else:
                print("\nВаш инвентарь пуст")
        case 'go':
            if argument in ['north']:
                move_player(game_state, 'north')
                describe_current_room(game_state)
            elif argument in ['south']:
                move_player(game_state, 'south')
                describe_current_room(game_state)
            elif argument in ['east']:
                move_player(game_state, 'east')
                describe_current_room(game_state)
            elif argument in ['west']:
                move_player(game_state, 'west')
                describe_current_room(game_state)
            else:
                print("\nУкажите направление: идти [north|south|east|west].")
        case 'take':
            if argument:
                take_item(game_state, argument)
            else:
                print("\nУкажите предмет: take")
    return True
        

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
        should_continue = process_command(game_state, command)
        if not should_continue:
            break
if __name__ == "__main__":
    main()

  