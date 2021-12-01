import json
import Components.UpdateCurrentGameState as UpdateCurrentGameState
import Components.LeagueStats as LeagueStats

#Class to set up the game, takes in form data from match setup webpage
#Author: Ben Houser

class GameSetup():

    # Open empty game state json, populate with game data, save to current_game_state.json
    # Inout: game_data is json object sent to server from Start Match modal
    def __init__(self, game_data):
        self.init_json = "initial_game_state.json"
        self.active_json = "current_game_state.json"
        self.game_data = game_data

        #print(game_data)

        with open(self.init_json) as f:
            self.init_data = json.load(f)

        self.set_game_info()

        LS = LeagueStats.LeagueStats()
        LS.add_player(self.game_data["Player1Name"])
        LS.add_player(self.game_data["Player2Name"])
        

        updateCurrentGameState = UpdateCurrentGameState.UpdateCurrentGameState()
        updateCurrentGameState.initalize_game(self.init_data)
        updateCurrentGameState.update_displayed_league_stats(game_data["LeagueStats"])
        updateCurrentGameState.update_displayed_match_stats(game_data["MatchStats"])
        updateCurrentGameState.write()

    def set_game_info(self):


        try:
            self.init_data["game"]["sets"] = int(self.game_data["SetNumber"])
            if int(self.game_data["SetNumber"]) == 0:
                self.init_data["game"]["sets"] = 1
        except:
            self.init_data["game"]["sets"] = 1
        try:
            self.init_data["game"]["legs"] = int(self.game_data["NumberOfLegs"])
            if int(self.game_data["NumberOfLegs"]) == 0:
                self.init_data["game"]["legs"] = 1
        except:
            self.init_data["game"]["legs"] = 1
        
        self.init_data["game"]["score"] = int(self.game_data["Score"])
        self.init_data["game"]["date"] = self.game_data["DateOfMatch"]

        self.init_data["player1"]["name"] = self.game_data["Player1Name"]
        self.init_data["player1"]["score"] = self.game_data["Score"]

        self.init_data["player2"]["name"] = self.game_data["Player2Name"]
        self.init_data["player2"]["score"] = self.game_data["Score"]
