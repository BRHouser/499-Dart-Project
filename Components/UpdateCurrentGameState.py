import json

class UpdateCurrentGameState():

    def __init__(self):
        self.json_path = "current_game_state.json"


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
            data.write(json.dumps(content))

    #replace currently displayed league stats. read new legaue stats from the archive
    def update_displayed_league_stats(self, new_key):
        with open(self.json_path) as data:
            content = json.loads(data.read())
        #todo: lookup statistics from archive
        content["player1"]["leagueStats"] = new_key + ":"
        content["player2"]["leagueStats"] = new_key + ":"
        with open(self.json_path, "w") as data:
            data.write(json.dumps(content))

    def update_player_score(self, player, new_score):
        with open(self.json_path) as data:
            content = json.loads(data.read())
        #todo: lookup statistics from archive
        content[player]["score"] = new_score

        with open(self.json_path, "w") as data:
            data.write(json.dumps(content))

    def update_current_match_stats(self,player,match_180s,current_turn_avg):
        with open(self.json_path) as data:
            content = json.loads(data.read())
        content[player]["match_180s"]=match_180s
        content[player]["current_turn_avg"]=current_turn_avg
        with open(self.json_path, "w") as data:
            data.write(json.dumps(content))

