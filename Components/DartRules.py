import json
import Components.UpdateCurrentGameState as UpdateCurrentGameState

#Class to apply dart gameplay rules: score arithmetic, check for win, calculate outs, and register dart statistics.
#Authors: Ben Houser and Anthony Dohogne

class DartRules():

    def __init__(self, updateCurrentGameState):
        self.json_path = "current_game_state.json"

        self.json_data = updateCurrentGameState.get_content()
        self.updateCurrentGameState = updateCurrentGameState
        self.bust = False
        self.throw_sum = 0
        self.throws = 0

        self.throw_data = {
            "player": 0,
            "throws": [],
            "score": 0
        }


        # TODO: init new throw entry in score history

    #input: player string ("player1" or "player2"); score string, ("19" "T20", "DB", etc.) 
    def add_score(self, player, score):
        if not self.bust:

            self.throw_data["player"] = player
            self.throw_data["throws"].append(score)

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

            if value != 60:
                self.updateCurrentGameState.perfect_leg(player, False)
            if new_score < 170:
                #outs = ""
                outs = " ".join(self.calculate_winning_throws(new_score))
                self.updateCurrentGameState.possible_outs(player, outs)

            self.updateCurrentGameState.update_player_score(player, new_score)

            self.refresh()
            self.register_statistics(player, score)

            self.throw_data["score"] = new_score

            #check for win
            if new_score == 0:
                self.updateCurrentGameState.log_throw(self.get_throw_data())
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

    #return self.throw_data
    def get_throw_data(self):
        return self.throw_data

    # input
    def calculate_winning_throws(self, score):
        winning_throws = []
        if (score == 170):
            winning_throws = ['T20', 'T20', 'DB']
        elif (score == 167):
            winning_throws = ['T19', 'T20', 'DB']
        elif (score == 164):
            winning_throws = ['T20', 'T18', 'DB']
        elif (score == 161):
            winning_throws = ['T19', 'T18', 'DB']
        elif (score == 160):
            winning_throws = ['T20', 'DB', 'DB']
        elif (score == 158):
            winning_throws = ['T18', 'T18', 'DB']
        elif (score == 157):
            winning_throws = ['T19', 'DB', 'DB']
        elif (score == 156):
            winning_throws = ['D7', 'T19', 'DB']
        elif (score == 155):
            winning_throws = ['T16', 'T19' ,'DB' ]
        elif (score == 154):
            winning_throws = ['T18', 'DB', 'DB']
        elif (score == 153):
            winning_throws = ['T20', 'T19', 'D18']
        elif (score == 152):
            winning_throws = ['T18', 'T18', 'DB']
        elif (score == 151):
            winning_throws =['T20', 'T17', 'D20']
        elif (score == 150):
            winning_throws = ['DB', 'DB', 'DB']
        elif (score == 149):
            winning_throws = ['T20', 'T19', 'D16']
        elif (score == 148):
            winning_throws = ['T16', 'DB', 'DB']
        elif (score == 147):
            winning_throws = ['T20', 'T17', 'D18']
        elif (score == 146):
            winning_throws = ['T12', 'T20', 'DB']
        elif (score == 145):
            winning_throws = ['T20', 'T15', 'D20']
        elif (score == 144):
            winning_throws = ['D20', 'T18', 'DB']
        elif (score == 143):
            winning_throws = ['T20', 'T17', 'D16']
        elif (score == 142):
            winning_throws = ['T14', 'DB', 'DB']
        elif (score == 141):
            winning_throws = ['T20', 'T19', 'D12']
        elif (score == 140):
            winning_throws = ['D20', 'DB', 'DB']
        elif (score == 139):
            winning_throws = ['T19', 'T14', 'D20']
        elif (score == 138):
            winning_throws = ['D14', 'T20', 'DB']
        elif (score == 137):
            winning_throws = ['T20', 'T19', 'D10']
        elif (score == 136):
            winning_throws = ['D13', 'T20', 'DB']
        elif (score == 135):
            winning_throws = ['D20', 'T15', 'DB']
        elif (score == 134):
            winning_throws = ['D12', 'T20', 'DB']
        elif (score == 133):
            winning_throws = ['T20', 'T19', 'D8']
        elif (score == 132):
            winning_throws = ['D11', 'T20', 'DB']
        elif (score == 131):
            winning_throws = ['T19', 'T14', 'D16']
        elif (score == 130):
            winning_throws = ['D10', 'T20', 'DB']
        elif (score == 129):
            winning_throws = ['T19', 'T16', 'D12']
        elif (score == 128):
            winning_throws = ['D9', 'T20', 'DB']
        elif (score == 127):
            winning_throws = ['T19', 'T16', 'D12']
        elif (score == 126):
            winning_throws = ['D8', 'T20', 'DB']
        elif (score == 125): # TODO:Check the single bull.. 
            #Ben: single bull is 'B'
            winning_throws = ['25','T20','D20']
        elif (score == 124):
            winning_throws = ['D7', 'T20', 'DB']
        elif (score == 123):
            winning_throws = ['T19', 'T16', 'D9']
        elif (score == 122):
            winning_throws = ['D6', 'T20', 'DB']
        elif (score == 121):
            winning_throws = ['T20', 'T11', 'D14']
        elif (score == 120):
            winning_throws = ['D5', 'T20', 'DB']
        elif (score == 119):
            winning_throws = ['T19', 'T12', 'D13']
        elif (score == 118):
            winning_throws = ['D4', 'T20', 'DB']
        elif (score == 117):
            winning_throws = ['T20', '17', 'D20']
        elif (score == 116):
            winning_throws = ['D3', 'T20', 'DB']
        elif (score == 115):
            winning_throws = ['T19', '18', 'D20']
        elif (score == 114):
            winning_throws = ['D2', 'T20', 'DB']
        elif (score == 113):
            winning_throws = ['T19', '16', 'D20']
        elif (score == 112):
            winning_throws = ['D1', 'T20', 'DB']
        elif (score == 111):
            winning_throws = ['T19', '14', 'D20']
        elif (score == 110):
            winning_throws = [ 'T20', 'DB']
        elif (score == 109):
            winning_throws = ['T20', '9', 'D20']
        elif (score == 108):
            winning_throws = ['1', 'T19', 'DB']
        elif (score == 107):
            winning_throws = ['T19', '10', 'D20']
        elif (score == 106):
            winning_throws = ['D1', 'T18', 'DB']
        elif (score == 105):
            winning_throws = ['T19', '8', 'D20']
        elif (score == 104):
            winning_throws = [ 'T18', 'DB']
        elif (score == 103):
            winning_throws = ['T19', '6', 'D20']
        elif (score == 102):
            winning_throws = ['1', 'T17', 'DB']
        elif (score == 101):
            winning_throws = ['T20', '9', 'D16']
        elif (score == 100):
            winning_throws = [ 'DB', 'DB']
        elif (score == 99):
            winning_throws = ['T19', '10', 'D16']
        elif (score == 98):
            winning_throws = [ 'T16', 'DB']
        elif (score == 97):
            winning_throws = [ 'T19', 'D20']
        elif (score == 96):
            winning_throws = ['1', 'T15', 'DB']
        elif (score == 95):
            winning_throws = [ 'T19', 'D19']
        elif (score == 94):
            winning_throws = ['D1', 'T14', 'DB']
        elif (score == 93):
            winning_throws = [ 'T19', 'D18']
        elif (score == 92):
            winning_throws = [ 'T14', 'DB']
        elif (score == 91):
            winning_throws = [ 'T17', 'D20']
        elif (score == 90):
            winning_throws = [ 'D20', 'DB']
        elif (score == 89):
            winning_throws = [ 'T19', 'D16']
        elif (score == 88):
            winning_throws = [ 'D19', 'DB']
        elif (score == 87):
            winning_throws = [ 'T17', 'D18']
        elif (score == 86):
            winning_throws = [ 'D18', 'DB']
        elif (score == 85):
            winning_throws = [ 'T15', 'D20']
        elif (score == 84):
            winning_throws = [ 'D17', 'DB']
        elif (score == 83):
            winning_throws = [ 'T17', 'D16']
        elif (score == 82):
            winning_throws = [ 'D16', 'DB']
        elif (score == 81):
            winning_throws = [ 'T19', 'D12']
        elif (score == 80):
            winning_throws = [ 'D15', 'DB']
        elif (score == 79):
            winning_throws = [ 'T19', 'D11']
        elif (score == 78):
            winning_throws = [ 'D14', 'DB']
        elif (score == 77):
            winning_throws = [ 'T19', 'D10']
        elif (score == 76):
            winning_throws = [ 'D13', 'DB']
        elif (score == 75):
            winning_throws = [ 'T17', 'D12']
        elif (score == 74):
            winning_throws = [ 'D12', 'DB']
        elif (score == 73):
            winning_throws = [ 'T19', 'D8']
        elif (score == 72):
            winning_throws = [ 'D11', 'DB']
        elif (score == 71):
            winning_throws = [ 'T13', 'D16']
        elif (score == 70):
            winning_throws = [ 'D10', 'DB']
        elif (score == 69):
            winning_throws = [ 'T19', 'D6']
        elif (score == 68):
            winning_throws = [ 'D9', 'DB']
        elif (score == 67):
            winning_throws = [ 'T9', 'D20']
        elif (score == 66):
            winning_throws = [ 'D8', 'DB']
        elif (score == 65):
            winning_throws = [ '25', 'D20']
        elif (score == 64):
            winning_throws = [ 'D7', 'DB']
        elif (score == 63):
            winning_throws = [ 'T17', 'D6']
        elif (score == 62):
            winning_throws = [ 'D6', 'DB']
        elif (score == 61):
            winning_throws = [ '25', 'D18']
        elif (score == 60):
            winning_throws = [ 'D5', 'DB']
        elif (score == 59):
            winning_throws = [ '19', 'D20']
        elif (score == 58):
            winning_throws = [ 'D4', 'DB']
        elif (score == 57):
            winning_throws = [ '17', 'D20']
        elif (score == 56):
            winning_throws = [ 'D3', 'DB']
        elif (score == 55):
            winning_throws = [ '15', 'D20']
        elif (score == 54):
            winning_throws = [ 'D2', 'DB']
        elif (score == 53):
            winning_throws = [ '13', 'D20']
        elif (score == 52):
            winning_throws = [ 'D1', 'DB']
        elif (score == 51):
            winning_throws = [ '11', 'D20']
        elif (score == 50):
            winning_throws = [  'DB']
        elif (score == 49):
            winning_throws = [ '9', 'D20']
        elif (score == 48):
            winning_throws = [ 'D4', 'D20']
        elif (score == 47):
            winning_throws = [ '7', 'D20']
        elif (score == 46):
            winning_throws = [ 'D3', 'D20']
        elif (score == 45):
            winning_throws = [ '5', 'D20']
        elif (score == 44):
            winning_throws = [ 'D2', 'D20']
        elif (score == 43):
            winning_throws = [ '3', 'D20']
        elif (score == 42):
            winning_throws = [ 'D1', 'D20']
        elif (score == 41):
            winning_throws = [ '1', 'D20']
        elif (score == 40):
            winning_throws = [  'D20']
        elif (score == 39):
            winning_throws = [ '7', 'D16']
        elif (score == 38):
            winning_throws = [  'D19']
        elif (score == 37):
            winning_throws = [ '5', 'D16']
        elif (score == 36):
            winning_throws = [  'D18']
        elif (score == 35):
            winning_throws = [ '3', 'D16']
        elif (score == 34):
            winning_throws = [  'D17']
        elif (score == 33):
            winning_throws = [ '1', 'D16']
        elif (score == 32):
            winning_throws = [  'D16']
        elif (score == 31):
            winning_throws = [ '15', 'D8']
        elif (score == 30):
            winning_throws = [  'D15']
        elif (score == 29):
            winning_throws = [ '13', 'D8']
        elif (score == 28):
            winning_throws = [  'D14']
        elif (score == 27):
            winning_throws = [ '11', 'D8']
        elif (score == 26):
            winning_throws = [  'D13']
        elif (score == 25):
            winning_throws = [ '9', 'D8']
        elif (score == 24):
            winning_throws = [  'D12']
        elif (score == 23):
            winning_throws = [ '7', 'D8']
        elif (score == 22):
            winning_throws = [  'D11']
        elif (score == 21):
            winning_throws = [ '5', 'D8']
        elif (score == 20):
            winning_throws = [  'D10']
        elif (score == 19):
            winning_throws = [ '3', 'D8']
        elif (score == 18):
            winning_throws = [  'D9']
        elif (score == 17):
            winning_throws = [ '1', 'D8']
        elif (score == 16):
            winning_throws = [  'D8']
        elif (score == 15):
            winning_throws = [ '5', 'D5']
        elif (score == 14):
            winning_throws = [  'D7']
        elif (score == 13):
            winning_throws = [ '3', 'D5']
        elif (score == 12):
            winning_throws = [  'D6']
        elif (score == 11):
            winning_throws = [ '1', 'D5']
        elif (score == 10):
            winning_throws = [  'D5']
        elif (score == 9):
            winning_throws = [ '5', 'D4']
        elif (score == 8):
            winning_throws = [  'D4']
        elif (score == 7):
            winning_throws = [ '3', 'D4']
        elif (score == 6):
            winning_throws = [  'D3']
        elif (score == 5):
            winning_throws = [ '1', 'D4']
        elif (score == 4):
            winning_throws = [  'D2']
        elif (score == 3):
            winning_throws = [ '1', 'D2']
        elif (score == 2):
            winning_throws = [  'D1']
        
        return winning_throws
    