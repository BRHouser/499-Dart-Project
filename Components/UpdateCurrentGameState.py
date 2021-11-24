import json

class UpdateCurrentGameState():

    def __init__(self):
        self.json_path = "current_game_state.json"
        self.new_leg = False


    #create initial current_game_state json
    def initalize_game(self, data):
        with open(self.json_path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    #replace currently displayed match stats. read new match stats from "stats" section of current game state json
    def update_displayed_match_stats(self, new_key):
        with open(self.json_path) as data:
            content = json.loads(data.read())
        #todo: lookup statistics from current game state json
        content["player1"]["matchStats"] = new_key + ":"
        content["player2"]["matchStats"] = new_key + ":"
        with open(self.json_path, "w") as data:
            data.write(json.dumps(content, ensure_ascii=False, indent=4))

    #replace currently displayed league stats. read new legaue stats from the archive
    def update_displayed_league_stats(self, new_key):
        with open(self.json_path) as data:
            content = json.loads(data.read())
        #todo: lookup statistics from archive
        content["player1"]["leagueStats"] = new_key + ":"
        content["player2"]["leagueStats"] = new_key + ":"
        with open(self.json_path, "w") as data:
            data.write(json.dumps(content, ensure_ascii=False, indent=4))

    def update_player_score(self, player, new_score):
        with open(self.json_path) as data:
            content = json.loads(data.read())
        #todo: lookup statistics from archive
        content[player]["score"] = new_score

        with open(self.json_path, "w") as data:
            data.write(json.dumps(content, ensure_ascii=False, indent=4))

    def update_current_match_stats(self,player,match_180s,current_turn_avg):
        with open(self.json_path) as data:
            content = json.loads(data.read())
        content[player]["match_180s"]=match_180s
        content[player]["current_turn_avg"]=current_turn_avg
        with open(self.json_path, "w") as data:
            data.write(json.dumps(content, ensure_ascii=False, indent=4))

    # call when a player's score hits 0; input: player string "player1" or "player2"
    def leg_win(self, player):
        with open(self.json_path) as data:
            content = json.loads(data.read())

        print(player + " wins the leg!")
        #reset scores
        reset_score = content["game"]["score"]
        content["player1"]["score"] = reset_score
        content["player2"]["score"] = reset_score
        
        #add leg win to player
        content[player]["legsWon"] += 1
        content["game"]["current_leg"] += 1
        
        #check for set win
        if content[player]["legsWon"] == content["game"]["legs"]:
            #reset legs won
            print(player + " wins the set!")
            content["player1"]["legsWon"] = 0
            content["player2"]["legsWon"] = 0
            content["game"]["current_leg"] = 0
            #add set win to player
            content[player]["setsWon"] += 1
            content["game"]["current_set"] += 1

            #check for game win
            if content[player]["setsWon"] == content["game"]["sets"]:
                print(player + "wins the game!")
                #TODO: add win state

        #TODO: which player goes first in the next leg?
        content["game"]["current_turn"] = 0
        self.new_leg = True
        #bug: this gets undone by the toggle_turn call in ReceiveData.py

        with open(self.json_path, "w") as data:
            data.write(json.dumps(content, ensure_ascii=False, indent=4))

    def toggle_turn(self):
        with open(self.json_path) as data:
            content = json.loads(data.read())

        if content["game"]["current_turn"] == 0:
            content["game"]["current_turn"] = 1
        else:
            content["game"]["current_turn"] = 0

        with open(self.json_path, "w") as data:
            data.write(json.dumps(content, ensure_ascii=False, indent=4))