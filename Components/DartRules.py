import json
import Components.UpdateCurrentGameState as UpdateCurrentGameState

class DartRules():

    def __init__(self, updateCurrentGameState):
        self.json_path = "current_game_state.json"
        with open(self.json_path) as data:
            content = json.load(data)
        self.json_data = content
        self.updateCurrentGameState = updateCurrentGameState

    #input: player string ("player1" or "player2"); score string, ("19" "T20", "DB", etc.)
    def add_score(self, player, score):
        registered_score = 0
        score = str(score)
        value = self.get_score_value(score)
        current_score = int(self.json_data[player]["score"])
        print(value)
        diff = current_score - value
        if(diff < 0):
            registered_score = 0
        elif(diff == 0):
            if(score.find("D") >= 0):
                registered_score = value
        else:
            registered_score = value

        new_score = current_score - registered_score
        print("new score: " + str(new_score))
        self.updateCurrentGameState.update_player_score(player, new_score)
        self.refresh()

    def refresh(self):
        with open(self.json_path) as data:
            content = json.load(data)
        self.json_data = content

    def get_score_value(self, score):
        retval = 0
        if(score.find("DB") >= 0):
            retval = 50
        elif(score.find("B") >= 0):
            retval = 25
        elif(score.find("D") >= 0):
            retval = int(score[score.find("D")+1:]) * 2
        elif(score.find("T") >= 0):
            retval = int(score[score.find("T")+1:]) * 3
        else:
            retval = int(score)
        
        return retval

    def register_statistics(player, score):
        pass