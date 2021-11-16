import json
import Components.UpdateCurrentGameState as UpdateCurrentGameState

class GameSetup():

    def __init__(self, game_data):
        self.init_json = "initial_game_state.json"
        self.active_json = "current_game_state.json"

        print(game_data)