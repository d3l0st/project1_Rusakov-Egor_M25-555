# labyrinth_game/utils.py
from .constants import ROOMS

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