#!/usr/bin/env python3

from .player_actions import get_input, move_player, take_item, use_item
from .utils import attempt_open_treasure, describe_current_room, show_help, solve_puzzle


def process_command(game_state, command):
    """Обрабатывает команду пользователя и выполняет соответствующие действия.
    
    Args:
        game_state (dict): Текущее состояние игры
        command (str): Введенная пользователем команда
        
    Returns:
        bool: True если игра должна продолжиться, False если завершена

    """
    parts = command.lower().split()
    if not parts:
        return True
    action = parts[0]
    argument = parts[1] if len(parts) > 1 else None

    match action:
        case 'quit' | 'exit':
            print("\nСпасибо за игру! До свидания!")
            return False
        case 'look':
            describe_current_room(game_state)
        case 'inventory':
            if game_state['player_inventory']:
                print(f"\nВаш инвентарь: {', '.join(game_state['player_inventory'])}") # noqa: E501
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
        case 'use':
            if argument:
                use_item(game_state, argument)
            else:
                print("\nВы не можете использовать предмет.")
        case 'solve':
                if game_state['current_room'] == 'treasure_room':
                    attempt_open_treasure(game_state)
                else:
                    solve_puzzle(game_state)
        case 'help':
            show_help()
        case 'north' | 'south' | 'west' | 'east':
            move_player(game_state, action)
            describe_current_room(game_state)
        case _:
            print(f"Неизвестная команда: '{command}'. Введите 'help' для списка команд.") # noqa: E501
    return True
        

def main():
    """Основная функция игры, запускающая игровой цикл."""
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

  