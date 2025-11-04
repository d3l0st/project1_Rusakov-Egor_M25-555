# labyrinth_game/players_actions.py
from .constants import ROOMS


def show_inventory(game_state):
    """Показывает содержимое инвентаря игрока.
    
    Args:
        game_state (dict): Текущее состояние игры с информацией об инвентаре

    """
    if game_state['player_inventory']:
        print(game_state['player_inventory'])
    else:
        print("Инвентарь пуст")

def get_input(prompt="> "):
    """Запрашивает ввод от пользователя с обработкой исключений.
    
    Args:
        prompt (str): Текст приглашения для ввода
        
    Returns:
        str: Введенная пользователем строка или "quit" при прерывании

    """
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"
    
def move_player(game_state, direction):
    """Перемещает игрока в указанном направлении с проверкой доступа.
    
    Args:
        game_state (dict): Текущее состояние игры
        direction (str): Направление движения (north/south/east/west)
        
    Returns:
        bool: True если перемещение успешно, False если нет
    
    """
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    if direction in room_data['exits']:
        new_room = room_data['exits'][direction]
        if new_room == 'treasure_room' and 'rusty_key' not in game_state['player_inventory']: # noqa: E501
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return False
        game_state['current_room'] = new_room    
        print(f"Вы переместились в направлении {direction} в {new_room}.")
        if new_room == 'treasure_room' and 'rusty_key' in game_state['player_inventory']: # noqa: E501
            print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.") # noqa: E501
        from .utils import random_event
        random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")
        return False

def take_item(game_state, item_name):
    """Позволяет игроку взять предмет из текущей комнаты.
    
    Args:
        game_state (dict): Текущее состояние игры
        item_name (str): Название предмета для взятия
        
    Returns:
        bool: True если предмет взят успешно, False если нет

    """
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
    """Использует предмет из инвентаря игрока.
    
    Args:
        game_state (dict): Текущее состояние игры
        item_name (str): Название предмета для использования
        
    Returns:
        bool: True если предмет использован успешно, False если нет
    """
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
                    print("\nВы взяли ржавый ключ. Он может использоваться для открытия сундука") # noqa: E501
                else:
                    print("Но у вас уже есть такой ключ.")
            case _:
                print(f"Вы не знаете как использовать {item_name}.")
    else:
        print("У вас нет такого предмета.")
