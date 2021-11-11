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

        #reset counters for triple 20 and double bullseye
        t20s=0
        dbl_bulls=0
        #check the scores
        if(value==60):
            t20s=t20s+1
        elif(value==50):
            dbl_bulls=dbl_bulls+1
        #get the total numbers of each
        total_t20s=t20s+self.json_data[player]["t20s_hit"]
        total_dbl_bulls=dbl_bulls+self.json_data[player]["dbl_bulls_hit"]

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
        self.updateCurrentGameState.update_player_score(player, new_score, total_t20s, total_dbl_bulls)
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

    def register_statistics(self, player, scores):
        throw1=self.get_score_value(str(scores[0]))
        throw2=self.get_score_value(str(scores[1]))
        throw3=self.get_score_value(str(scores[2]))
        turn_sum=throw1+throw2+throw3

        print(turn_sum)
        #Check for 180
        match_180s=self.json_data[player]["match_180s"]
        if (turn_sum==180):
            match_180s+=1
        #Find avg score for this turn
        current_turn_avg=turn_sum/3
        print(current_turn_avg)
        #TODO Get avg score per turn and avg score per dart

        self.updateCurrentGameState.update_current_match_stats(player,match_180s,current_turn_avg)
        self.refresh()
        pass
    
    