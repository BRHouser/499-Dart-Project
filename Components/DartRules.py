import json
import Components.UpdateCurrentGameState as UpdateCurrentGameState

class DartRules():

    def __init__(self, updateCurrentGameState):
        self.json_path = "current_game_state.json"

        self.json_data = updateCurrentGameState.get_content()
        self.updateCurrentGameState = updateCurrentGameState
        self.bust = False
        self.throw_sum = 0
        self.throws = 0

    #input: player string ("player1" or "player2"); score string, ("19" "T20", "DB", etc.) 
    def add_score(self, player, score):
        if not self.bust:
            self.throws += 1
            registered_score = 0
            score = str(score)
            value = self.get_score_value(score)
            current_score = int(self.json_data[player]["score"])
            print(value)

            diff = current_score - value
            if(diff < 0 or diff == 1):
                registered_score = 0
                self.bust = True
            elif(diff == 0):
                if(score.find("D") >= 0):
                    registered_score = value
            else:
                registered_score = value

            new_score = current_score - registered_score
            self.throw_sum += registered_score

            #print("new score: " + str(new_score))
            #print("sum: " + str(self.throw_sum))
            print(self.throws)
            self.updateCurrentGameState.update_player_score(player, new_score)

            self.refresh()
            self.register_statistics(player, score)

            #check for win
            if new_score == 0:
                self.bust = True #prevent scores from carrying over to next leg
                self.updateCurrentGameState.leg_win(player)

    # reload json_data from current game state json
    def refresh(self):
        self.json_data = self.updateCurrentGameState.get_content()
        #print(self.json_data)

    # input: score string from scorekeeper; output: numerical value
    def get_score_value(self, score):
        retval = 0
        if(score == "KO"):
            retval = 0
        elif(score == "F"):
            retval = 0
        elif(score == "BO"):
            retval = 0
        elif(score.find("DB") >= 0):
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

    #player string ("player1" or "player2"); score list, (["19" "T20", "DB"])
    # registers throws to current game and league statistics 
    def register_statistics(self, player, score):
        
        print("registers stats: " + score)
        #Current Match
        stats = self.json_data["stats"][player]
        print(stats)

        if(self.throws == 3):
            stats["turns"] += 1

            #Average turn score
            current = stats["sum"]
            print("sum: " + str(current))
            new = (current)/stats["turns"]
            self.updateCurrentGameState.update_current_match_stats(player, "Average Turn Score", new)

            #180s in match
            current = stats["current"]["180s In Match"]
            if self.throw_sum == 180:
                new = stats["current"]["180s In Match"] + 1
                self.updateCurrentGameState.update_current_match_stats(player, "180s In Match", new)

            #best turn score
            current = stats["current"]["Best Turn Score"]
            print(current)
            if self.throw_sum > current:
                self.updateCurrentGameState.update_current_match_stats(player, "Best Turn Score", self.throw_sum)



        #bulls thrown
        if score == "B" or score == "DB":
            new = stats["current"]["Bulls Thrown"] + 1
            self.updateCurrentGameState.update_current_match_stats(player, "Bulls Thrown", new)
        
        #T20s thrown
        if score == "T20":
            new = stats["current"]["Triple 20s Thrown"] + 1
            self.updateCurrentGameState.update_current_match_stats(player, "Triple 20s Thrown", new)

        #League


        #TODO Get avg score per turn and avg score per dart

        #self.updateCurrentGameState.update_current_match_stats(player,match_180s,current_turn_avg)
        self.refresh()

    # input
    def calculate_winning_throws(self, player):
        score = self.updateCurrentGameState.get_player_score(player)
        winning_throws = []
        if (score == 170):
            winning_throws = ['T20', 'T20', 'DB']
        elif (score == 160):
            winning_throws = ['T20', 'DB', 'DB']
        elif (score == 158):
            winning_throws = ['T18', 'T18', 'DB']
        elif (score == 156):
            winning_throws = ['D7', 'T19', 'DB']
        elif (score == 154):
            winning_throws = ['T18', 'DB', 'DB']
        elif (score == 152):
            winning_throws = ['T18', 'T18', 'DB']
        elif (score == 150):
            winning_throws = ['DB', 'DB', 'DB']
        elif (score == 148):
            winning_throws = ['T16', 'DB', 'DB']
        elif (score == 146):
            winning_throws = ['T12', 'T20', 'DB']
        elif (score == 144):
            winning_throws = ['D20', 'T18', 'DB']
        elif (score == 142):
            winning_throws = ['T14', 'DB', 'DB']
        elif (score == 140):
            winning_throws = ['D20', 'DB', 'DB']
        elif (score == 138):
            winning_throws = ['D14', 'T20', 'DB']
        elif (score == 136):
            winning_throws = ['D13', 'T20', 'DB']
        elif (score == 134):
            winning_throws = ['D12', 'T20', 'DB']
        elif (score == 132):
            winning_throws = ['D11', 'T20', 'DB']
        elif (score == 130):
            winning_throws = ['D10', 'T20', 'DB']
        elif (score == 128):
            winning_throws = ['D9', 'T20', 'DB']
        elif (score == 126):
            winning_throws = ['D8', 'T20', 'DB']
        elif (score == 124):
            winning_throws = ['D7', 'T20', 'DB']
        elif (score == 122):
            winning_throws = ['D6', 'T20', 'DB']
        elif (score == 120):
            winning_throws = ['D5', 'T20', 'DB']
        elif (score == 118):
            winning_throws = ['D4', 'T20', 'DB']
        elif (score == 116):
            winning_throws = ['D3', 'T20', 'DB']
        elif (score == 114):
            winning_throws = ['D2', 'T20', 'DB']
        elif (score == 112):
            winning_throws = ['D1', 'T20', 'DB']
        elif (score == 110):
            winning_throws = ['BO', 'T20', 'DB']
        elif (score == 108):
            winning_throws = ['1', 'T19', 'DB']
        elif (score == 106):
            winning_throws = ['D1', 'T18', 'DB']
        elif (score == 104):
            winning_throws = ['BO', 'T18', 'DB']
        elif (score == 102):
            winning_throws = ['1', 'T17', 'DB']
        elif (score == 100):
            winning_throws = ['BO', 'DB', 'DB']
        elif (score == 98):
            winning_throws = ['BO', 'T16', 'DB']
        elif (score == 96):
            winning_throws = ['1', 'T15', 'DB']
        elif (score == 94):
            winning_throws = ['D1', 'T14', 'DB']
        elif (score == 92):
            winning_throws = ['BO', 'T14', 'DB']
        elif (score == 90):
            winning_throws = ['BO', 'D20', 'DB']
        elif (score == 88):
            winning_throws = ['BO', 'D19', 'DB']
        elif (score == 86):
            winning_throws = ['BO', 'D18', 'DB']
        elif (score == 84):
            winning_throws = ['BO', 'D17', 'DB']
        elif (score == 82):
            winning_throws = ['BO', 'D16', 'DB']
        elif (score == 80):
            winning_throws = ['BO', 'D15', 'DB']
        elif (score == 78):
            winning_throws = ['BO', 'D14', 'DB']
        elif (score == 76):
            winning_throws = ['BO', 'D13', 'DB']
        elif (score == 74):
            winning_throws = ['BO', 'D12', 'DB']
        elif (score == 72):
            winning_throws = ['BO', 'D11', 'DB']
        elif (score == 70):
            winning_throws = ['BO', 'D10', 'DB']
        elif (score == 68):
            winning_throws = ['BO', 'D9', 'DB']
        elif (score == 66):
            winning_throws = ['BO', 'D8', 'DB']
        elif (score == 64):
            winning_throws = ['BO', 'D7', 'DB']
        elif (score == 62):
            winning_throws = ['BO', 'D6', 'DB']
        elif (score == 60):
            winning_throws = ['BO', 'D5', 'DB']
        elif (score == 58):
            winning_throws = ['BO', 'D4', 'DB']
        elif (score == 56):
            winning_throws = ['BO', 'D3', 'DB']
        elif (score == 54):
            winning_throws = ['BO', 'D2', 'DB']
        elif (score == 52):
            winning_throws = ['BO', 'D1', 'DB']
        elif (score == 50):
            winning_throws = ['BO', 'BO', 'DB']
        elif (score == 48):
            winning_throws = ['BO', 'D4', 'D20']
        elif (score == 46):
            winning_throws = ['BO', 'D3', 'D20']
        elif (score == 44):
            winning_throws = ['BO', 'D2', 'D20']
        elif (score == 42):
            winning_throws = ['BO', 'D1', 'D20']
        elif (score == 40):
            winning_throws = ['BO', 'BO', 'D20']
        elif (score == 38):
            winning_throws = ['BO', 'BO', 'D19']
        elif (score == 36):
            winning_throws = ['BO', 'BO', 'D18']
        elif (score == 34):
            winning_throws = ['BO', 'BO', 'D17']
        elif (score == 32):
            winning_throws = ['BO', 'BO', 'D16']
        elif (score == 30):
            winning_throws = ['BO', 'BO', 'D15']
        elif (score == 28):
            winning_throws = ['BO', 'BO', 'D14']
        elif (score == 26):
            winning_throws = ['BO', 'BO', 'D13']
        elif (score == 24):
            winning_throws = ['BO', 'BO', 'D12']
        elif (score == 22):
            winning_throws = ['BO', 'BO', 'D11']
        elif (score == 20):
            winning_throws = ['BO', 'BO', 'D10']
        elif (score == 18):
            winning_throws = ['BO', 'BO', 'D9']
        elif (score == 16):
            winning_throws = ['BO', 'BO', 'D8']
        elif (score == 14):
            winning_throws = ['BO', 'BO', 'D7']
        elif (score == 12):
            winning_throws = ['BO', 'BO', 'D6']
        elif (score == 10):
            winning_throws = ['BO', 'BO', 'D5']
        elif (score == 8):
            winning_throws = ['BO', 'BO', 'D4']
        elif (score == 6):
            winning_throws = ['BO', 'BO', 'D3']
        elif (score == 4):
            winning_throws = ['BO', 'BO', 'D2']
        elif (score == 2):
            winning_throws = ['BO', 'BO', 'D1']
        pass
    