import json
import Components.UpdateCurrentGameState as UpdateCurrentGameState
import Components.DartRules as DartRules

#Class to process all incoming data from scorekeeper: change displayed stats or upload scores
#Author: Ben Houser

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
        self.updateCurrentGameState.write()

    def changeDisplayedLeagueStats(self, key):
        self.updateCurrentGameState.update_displayed_league_stats(key)
        self.updateCurrentGameState.write()

    # Input: dict with format of "throws" dictionary found above
    def inputScores(self, throws):
        # key of throw data is "player1" or "player2"
        player = list(throws.keys())[0]
        scores = throws[player]
        
        # add scores one by one
        dart_rules = DartRules.DartRules(self.updateCurrentGameState)
        dart_rules.add_score(player, scores[0])
        dart_rules.add_score(player, scores[1])
        dart_rules.add_score(player, scores[2])

        # update current stats because they have been recalculated by dart rules
        keys = self.updateCurrentGameState.get_displayed_stats()
        self.changeDisplayedMatchStats(keys[0])
        self.changeDisplayedLeagueStats(keys[1])

        # toggle player
        if(not self.updateCurrentGameState.new_leg):
            self.updateCurrentGameState.log_throw(dart_rules.get_throw_data())
            self.updateCurrentGameState.toggle_turn()
        else:
            self.updateCurrentGameState.new_leg = False        

        #write current game state to updated scoreboard & scorekeeper
        self.updateCurrentGameState.write()


