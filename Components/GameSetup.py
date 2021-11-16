import json
import Components.UpdateCurrentGameState as UpdateCurrentGameState

class GameSetup():

    # Open empty game state json, populate with game data, save to current_game_state.json
    # Inout: game_data is json object sent to server from Start Match modal
    def __init__(self, game_data):
        self.init_json = "initial_game_state.json"
        self.active_json = "current_game_state.json"
        self.game_data = game_data

        print(game_data)

        with open(self.init_json) as f:
            self.init_data = json.load(f)

        self.set_game_info()

        updateCurrentGameState = UpdateCurrentGameState.UpdateCurrentGameState()
        updateCurrentGameState.initalize_game(self.init_data)

    def set_game_info(self):

        self.init_data["game"]["sets"] = self.game_data["SetNumber"]
        self.init_data["game"]["legs"] = self.game_data["NumberOfLegs"]
        self.init_data["game"]["score"] = self.game_data["Score"]

        self.init_data["player1"]["name"] = self.game_data["Player1Name"]
        self.init_data["player1"]["score"] = self.game_data["Score"]

        self.init_data["player2"]["name"] = self.game_data["Player2Name"]
        self.init_data["player2"]["score"] = self.game_data["Score"]

        print(self.init_data)
        