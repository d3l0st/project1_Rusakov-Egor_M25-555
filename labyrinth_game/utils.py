# labyrinth_game/utils.py
from .constants import ROOMS
from .player_actions import get_input

def describe_current_room(game_state):
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
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]
    if room['puzzle']:
        question, answer = room['puzzle']
        print(question)
        user_answer = get_input("Ваш ответ: ").strip()
        if user_answer.lower().strip() == answer.lower().strip():
            print("\nПравильно! Загадка решена!")
            room['puzzle'] = None
            reward = 'magic_glove'
            game_state['player_inventory'].append(reward)
            print(f"\nВы получаете награду {reward}!")
        else:
            print("\nНеверно. Попробуйте снова.")
    else: 
        print("Загадок здесь нет.")
    
def attempt_open_treasure(game_state):
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

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")