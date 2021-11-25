import json

class UpdateCurrentGameState():

    def __init__(self):
        self.json_path = "current_game_state.json"
        self.new_leg = False
        print("init updater")
        with open(self.json_path) as data:
            self.content = json.loads(data.read())

    #create initial current_game_state json
    def initalize_game(self, data):
        with open(self.json_path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    #replace currently displayed match stats. read new match stats from "stats" section of current game state json
    def update_displayed_match_stats(self, new_key):
        #todo: lookup statistics from current game state json
        print("update game stats")
        self.content["player1"]["matchStats"] = new_key + ": " + str(self.content["stats"]["player1"]["current"][new_key])
        self.content["player2"]["matchStats"] = new_key + ": " + str(self.content["stats"]["player2"]["current"][new_key])


    #replace currently displayed league stats. read new legaue stats from the archive
    def update_displayed_league_stats(self, new_key):
        #todo: lookup statistics from archive
        print("update league stats")
        self.content["player1"]["leagueStats"] = new_key + ": "
        self.content["player2"]["leagueStats"] = new_key + ": "

    def update_player_score(self, player, new_score):

        old = self.content[player]["score"]
        val = int(old) - new_score
        self.content["stats"][player]["sum"] += val
        self.content[player]["score"] = new_score


    def update_current_match_stats(self, player, key, value):
        #change the current match stats

        self.content["stats"][player]["current"][key] = value


    # call when a player's score hits 0; input: player string "player1" or "player2"
    def leg_win(self, player):
        print(player + " wins the leg!")
        #reset scores
        reset_score = self.content["game"]["score"]
        self.content["player1"]["score"] = reset_score
        self.content["player2"]["score"] = reset_score
        
        #add leg win to player
        self.content[player]["legsWon"] += 1
        self.content["game"]["current_leg"] += 1
        
        #check for set win
        if self.content[player]["legsWon"] == self.content["game"]["legs"]:
            #reset legs won
            print(player + " wins the set!")
            self.content["player1"]["legsWon"] = 0
            self.content["player2"]["legsWon"] = 0
            self.content["game"]["current_leg"] = 0
            #add set win to player
            self.content[player]["setsWon"] += 1
            self.content["game"]["current_set"] += 1

            #check for game win
            if self.content[player]["setsWon"] == self.content["game"]["sets"]:
                print(player + "wins the game!")
                #TODO: add win state

        #TODO: which player goes first in the next leg?
        self.content["game"]["current_turn"] = 0
        self.new_leg = True

    #switch player turns after turn is over
    def toggle_turn(self):

        if self.content["game"]["current_turn"] == 0:
            self.content["game"]["current_turn"] = 1
            self.content["stats"]["player1"]["turns"] += 1
        else:
            self.content["game"]["current_turn"] = 0
            self.content["stats"]["player2"]["turns"] += 1

    # returns list of displayed match and league stats keys. list[0] = match stats key, list[1] = league stats key
    def get_displayed_stats(self):
        
        retval = []

        stats = self.content["player1"]["matchStats"]
        retval.append(stats[0:stats.find(":")])

        stats = self.content["player1"]["leagueStats"]
        retval.append(stats[0:stats.find(":")])

        return retval

    def get_content(self):
        return self.content

    def write(self):
        #print("write:")
        #print(self.content)
        with open(self.json_path, "w") as data:
            data.write(json.dumps(self.content, ensure_ascii=False, indent=4))