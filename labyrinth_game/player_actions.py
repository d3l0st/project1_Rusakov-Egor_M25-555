# labyrinth_game/players_actions.py
from .constants import ROOMS
from utils import random_event

def show_inventory(game_state):
    if game_state['player_inventory']:
        print(game_state['player_inventory'])
    else:
        print("Инвентарь пуст")

def get_input(prompt="> "):
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"
    
def move_player(game_state, direction):
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    if direction in room_data['exits']:
        new_room = room_data['exits'][direction]
        game_state['current_room'] = new_room
        print(f"Вы переместились в направлении {direction} в {new_room}.")
        random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")
        return False

def take_item(game_state, item_name):
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    if item_name in room_data['items']:
        if item_name == 'treasure_chest':
            print("Вы не можете поднять сундук, он слишком тяжелый.")
        game_state['player_inventory'].append(item_name)
        room_data['items'].remove(item_name)
        print(f"Вы подняли: {item_name}.")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    if item_name in game_state['player_inventory']:
        match item_name:
            case 'torch':
                print("Вы зажгли факел, стало светлее.")
            case 'sword':
                print("Вы достали меч, уверенность растет.")
            case 'bronze_box':
                print("\nВы открыли шкатулку. Внутри лежит ржавый ключ")
                if 'rusty_key' not in game_state['player_inventory']:
                    game_state['player_inventory'].append('rusty_key')
                    print("\nВы взяли ржавый ключ. Он может использоваться для открытия сундука")
                else:
                    print("Но у вас уже есть такой ключ.")
            case _:
                print(f"Вы не знаете как использовать {item_name}.")
    else:
        print("У вас нет такого предмета.")
