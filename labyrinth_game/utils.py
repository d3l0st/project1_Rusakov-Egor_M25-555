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