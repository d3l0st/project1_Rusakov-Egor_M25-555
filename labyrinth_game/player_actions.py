# labyrinth_game/players_actions.py

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