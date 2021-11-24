import json
import Components.UpdateCurrentGameState as UpdateCurrentGameState
import Components.DartRules as DartRules


class ReceiveData():

    def __init__(self, data):
        self.data = data
        print("init receive data")
        print(self.data)
        self.updateCurrentGameState = UpdateCurrentGameState.UpdateCurrentGameState()

        key = list(data.keys())[0]

        if(key == "throws"):
            self.inputScores(data["throws"])
        elif(key == "new_match_stats"):
            self.changeDisplayedMatchStats(data["new_match_stats"])
        elif(key == "new_league_stats"):
            self.changeDisplayedLeagueStats(data["new_league_stats"])

    #data can either look like:
    change_stats = {
        "new_match_stats": "180s in Match"
    }
    # or
    change_stats = {
        "new_league_stats": "180s in Season"
    }
    # or
    change_stats = {
        "throws": {
            "player1": ["DB", "11", "T20"]
        }
    }    

    def changeDisplayedMatchStats(self, key):
        self.updateCurrentGameState.update_displayed_match_stats(key)

    def changeDisplayedLeagueStats(self, key):
        self.updateCurrentGameState.update_displayed_league_stats(key)

    def inputScores(self, throws):
        # key of throw data is "player1" or "player2"
        player = list(throws.keys())[0]
        scores = throws[player]
        
        dart_rules = DartRules.DartRules(self.updateCurrentGameState)
        dart_rules.add_score(player, scores[0])
        dart_rules.add_score(player, scores[1])
        dart_rules.add_score(player, scores[2])

        # toggle player
        if(not self.updateCurrentGameState.new_leg):
            self.updateCurrentGameState.toggle_turn()
        else:
            self.updateCurrentGameState.new_leg = False
        # commented out because of keyerror
        #dart_rules.register_statistics(player,scores)


