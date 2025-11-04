# labyrinth_game/utils.py
import math

from .constants import COMMANDS, ROOMS
from .player_actions import get_input


def describe_current_room(game_state):
    """Выводит подробное описание текущей комнаты.
    
    Args:
        game_state (dict): Текущее состояние игры,
        включающее в себя название текущей комнаты

    """
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]

    print(f"=={current_room_name.upper()}==")

    print(room['description'])

    if room['items']:
        print("\nЗаметные предметы:", ", ".join(room['items']))
    else:
        print("Нет заметных предметов")

    if room['exits']:
        print("\nВыходы:")
        for direction, target_room in room['exits'].items():
            print(f"  {direction} -> {target_room}")
    else:
        print("\nВыходв нет")
    
    if room['puzzle']:
        print("\nКажется, здесь есть загадка (используйте команду solve).")

def solve_puzzle(game_state):
    """Позволяет игроку решить загадку в текущей комнате.
    
    Args:
        game_state (dict): Текущее состояние игры
        
    Returns:
        bool: True если загадка решена успешно, False если нет
    """
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]
    if room['puzzle']:
        question, answer = room['puzzle']
        print(question)
        user_answer = get_input("Ваш ответ: ").strip()
        is_correct = check_answer(user_answer, answer)
        if is_correct:
            print("\nПравильно! Загадка решена!")
            room['puzzle'] = None
            reward = get_room_reward(current_room_name)
            game_state['player_inventory'].append(reward)
            print(f"\nВы получаете награду {reward}!")
        else:
            print("\nНеверно. Попробуйте снова.")
            if current_room_name == 'trap_room':
                print("Неверный ответ активирует ловушку!")
                trigger_trap(game_state)
    else: 
        print("Загадок здесь нет.")

def check_answer(user_answer, correct_answer):
    """Проверяет ответ пользователя с учетом альтернативных вариантов.
    
    Args:
        user_answer (str): Ответ введенный пользователем
        correct_answer (str): Правильный ответ
        
    Returns:
        bool: True если ответ верный, False если нет
    """
    user_answer = user_answer.lower().strip()
    correct_answer = correct_answer.lower().strip()

    if user_answer == correct_answer:
        return True

    number_alternatives = {
        '10': ['десять', 'ten'],
        '8': ['восемь', 'eight'],
        '6': ['шесть', 'six'],
        '5': ['пять', 'five'],
        '3': ['три', 'three']
    }
    
    if correct_answer in number_alternatives:
        if user_answer in number_alternatives[correct_answer]:
            return True
    
    return False

def get_room_reward(current_room_name):
    rewards = {
        'hall': 'silver_key',
        'trap_room': 'axe',
        'library': 'ancient_scroll',
        'garden': 'healing_potion',
        'observatory': 'star_compass',
        'armory': 'steel_gauntlets'
    }
    return rewards.get(current_room_name, 'mysterious_item')
    
def attempt_open_treasure(game_state):
    """Попытка открыть сундук с сокровищами в treasure_room.
    
    Args:
        game_state (dict): Текущее состояние игры
        
    Returns:
        bool: True если игра завершена победой, False если нет
    """
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]
    if current_room_name != 'treasure_room':
        print("Здесь нет сундука, продолжайте искать для победы.")
    else:
        print("\nСудя по всему, для открытия сундука потребуется ключ.")
        if 'treasure_key' in game_state['player_inventory']:
            print("\nВы применяете ключ, и замок щёлкает. Сундук открыт!")
            room['items'].remove('treasure_chest')
            print("\nВ сундуке сокровище! Вы победили!")
            game_state['game_over'] = True
        else: 
            print("\nСундук заперт. На замке есть числовой замок.")
            user_answer = get_input("\nВвести код? (да/нет): ").lower().strip()
            match user_answer:
                case 'да':
                    question, correct_code = room['puzzle']
                    print(question)
                    user_code = get_input("Введите код: ").strip()
                    if user_code == correct_code:
                        print("Код верный! Замок открывается.")
                        room['items'].remove('treasure_chest')
                        print("В сундуке сокровище! Вы победили!")
                        game_state['game_over'] = True
                    else:
                        print("Неверный код. Замок не открылся.")               
                case 'нет':
                    print("Вы отступаете от сундука.")

def pseudo_random(seed, modulo):
    """Генерирует псевдослучайное число на основе синуса.
    
    Args:
        seed (int): Число для инициализации генератора
        modulo (int): Верхняя граница диапазона [0, modulo)
        
    Returns:
        int: Псевдослучайное число в диапазоне [0, modulo)
    """
    sin_value = math.sin(seed * 12.9898)
    multiplied = sin_value * 43758.5453
    fractional_part = multiplied - math.floor(multiplied)
    result = math.floor(fractional_part * modulo)
    return result

def trigger_trap(game_state):
    """Активирует ловушку с негативными последствиями для игрока.
    
    Args:
        game_state (dict): Текущее состояние игры
        
    Returns:
        bool: True если игрок выжил, False если игра завершена
    """
    print("/nЛовушка активирована! Пол стал дрожать...")
    if game_state['player_inventroy']:
        items_count = len(game_state['player_inventory'])
        lost_item_index = pseudo_random(game_state.get('steps_taken', 0), items_count)
        lost_item = game_state['player_inventory'].pop(lost_item_index)
        print(f"В результате действия ловушки вы теряете {lost_item}")
    else:
        damage_chance = pseudo_random(20, 10)
        if damage_chance < 3: 
            print("Вы не успели увернуться! Ловушка наносит смертельный удар...")
            print("Игра окончена. Вы проиграли!")
            game_state['game_over'] = True
        else:
            print("Вам удалось увернуться от ловушки! Вы уцелели, но будьте осторожнее.") # noqa: E501

def random_event(game_state):
    """Создает случайные события во время перемещения игрока.
    
    Args:
        game_state (dict): Текущее состояние игры
    """
    event_chance = pseudo_random(999, 10) 
    if event_chance != 0:
        return
    event_type = pseudo_random(888, 3)
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]     
    match event_type:
        case 0:
            # Сценарий 1: Находка
            print("\nВы заметили что-то блестящее на полу...")
            if 'coin' not in room['items']:
                room['items'].append('coin')
                print("Вы нашли монетку! Она добавлена в комнату.")
            else:
                print("Это была всего лишь пыль...")
                
        case 1:
            # Сценарий 2: Испуг
            print("\nВы слышите странный шорох из темноты...")
            if 'sword' in game_state['player_inventory']:
                print("Вы достаете меч, и шорох мгновенно прекращается!")
            else:
                print("Шорох становится громче... Вам становится не по себе.")
                
        case 2:
            # Сценарий 3: Срабатывание ловушки
            print("\nВы чувствуете, что наступили на что-то подозрительное...")
            if current_room_name == 'trap_room' and 'torch' not in game_state['player_inventory']: # noqa: E501
                print("Это была ловушка! В темноте вы не разглядели ее!")
                trigger_trap(game_state)
            else:
                print("К счастью, это оказался просто камень.")   

def show_help():
    """Выводит справку по доступным командам игры."""
    print("\nДоступные команды:")
    for comand, description in COMMANDS.items():
        formatted_command = f"{comand:<16}"
        print(f"{formatted_command} - {description}")