import json
import time
import Components.LeagueStats as LeagueStats
import Components.MatchHistory as MatchHistory

# Class to make any changes to and read info about current game state json
# Author: Ben Houser
class UpdateCurrentGameState():

    # The purpose of this function is to initialize the current game state
    def __init__(self):
        self.json_path = "current_game_state.json"
        self.new_leg = False
        try:
            with open(self.json_path) as data:
                self.content = json.loads(data.read())
        except FileNotFoundError:
            print("Game not initialized")


    # Input: data: TODO: What exactly is data
    # The purpose is to create initial current_game_state json
    def initalize_game(self, data):
        with open(self.json_path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        self.content = data


    # Input: new_key: the new match stat to display
    # The purpose is to replace currently displayed match stats. Reads new match stats 
    # from "stats" section of current game state json
    def update_displayed_match_stats(self, new_key):
        new_key = new_key.replace("\n", "").strip()
        self.content["player1"]["matchStats"] = new_key + ": " + str(self.content["stats"]["player1"]["current"][new_key])
        self.content["player2"]["matchStats"] = new_key + ": " + str(self.content["stats"]["player2"]["current"][new_key])


    # Input: new_key: the new league stat to display
    # The purpose of this function is to replace currently displayed league stats. read new legaue stats from the archive
    def update_displayed_league_stats(self, new_key):

        new_key = new_key.replace("\n", "").strip()

        LS = LeagueStats.LeagueStats()
        name1 = self.content["player1"]["name"]
        name2 = self.content["player2"]["name"]

        self.content["player1"]["leagueStats"] = new_key + ": " + str(LS.get_stat(name1, new_key))
        self.content["player2"]["leagueStats"] = new_key + ": " + str(LS.get_stat(name2, new_key))


    # Input: player: player name
    # Input: new_score: the new score of a player
    # Purpose is to update the specified player's score
    def update_player_score(self, player, new_score):
        old = self.content[player]["score"]
        val = int(old) - new_score
        self.content["stats"][player]["sum"] += val
        LS = LeagueStats.LeagueStats()
        LS.add_score(self.content[player]["name"], val)

        self.content[player]["score"] = new_score


    # Input: player: player name
    # Input: key: the match stat
    # Input: value: the new stat value
    # Purpose is to update the current match stat
    def update_current_match_stats(self, player, key, value):
        self.content["stats"][player]["current"][key] = value


    # Input: player: player name
    # called when a player's score hits 0 to specify that the player won the leg
    def leg_win(self, player):
        #reset scores
        reset_score = self.content["game"]["score"]
        self.content["player1"]["score"] = reset_score
        self.content["player2"]["score"] = reset_score

        self.content["player1"]["perfectLeg"] = True
        self.content["player2"]["perfectLeg"] = True

        self.content["player1"]["possibleOuts"] = ""
        self.content["player2"]["possibleOuts"] = ""

        
        #add leg win to player
        self.content[player]["legsWon"] += 1
        self.content["game"]["current_leg"] += 1
        
        #check for set win
        game_win = False

        if self.content[player]["legsWon"] == self.content["game"]["legs"]:
            #reset legs won
            self.content["player1"]["legsWon"] = 0
            self.content["player2"]["legsWon"] = 0
            self.content["game"]["current_leg"] = 0
            #add set win to player
            self.content[player]["setsWon"] += 1
            self.content["game"]["current_set"] += 1

            #check for game win
            if self.content[player]["setsWon"] == self.content["game"]["sets"]:
                game_win = True
                self.game_over(player)

        if not game_win:
            last = self.content["game"]["lastStarter"]
            if(last == 0):
                self.content["game"]["current_turn"] = 1
                self.content["game"]["lastStarter"] = 1
            else:
                self.content["game"]["current_turn"] = 0
                self.content["game"]["lastStarter"] = 0

            self.new_leg = True


    # Input: player: player name
    # The purpose of this function is to decide the winner of the game 
    # and update all statistics 
    def game_over(self, player):
        self.content["game"]["won"] = True
        self.content["game"]["winner"] = player
        self.write()

        name = self.content[player]["name"]

        LS = LeagueStats.LeagueStats()
        LS.increment_win(name)
        LS.update_stat(name, "Last Win", self.content["game"]["date"])
        LS.update_ranks()

        MH = MatchHistory.MatchHistory()
        MH.add_match(self.content["throwHistory"],self.content["game"]["MatchName"],self.content["player1"]["name"],self.content["player2"]["name"], self.content["game"]["date"])

        #wait for scoreboard and scorekeeper to download current_game_state.json
        time.sleep(1)
        #register game to archive
        self.content = {}
        self.write()


    # Input: player: player name
    # Input: val: whether the player is on track for perfect leg
    # Function sets the perfect leg value for player to val (True or False)
    def perfect_leg(self, player, val):
        self.content[player]["perfectLeg"] = val


    # Input: player: player name
    # Input: val: the number of outs of a player
    # Function sets suggested outs for player
    def possible_outs(self, player, val):
        self.content[player]["possibleOuts"] = "Outs: " + val


    # This function switches player turns after turn is over
    def toggle_turn(self):

        if self.content["game"]["current_turn"] == 0:
            self.content["game"]["current_turn"] = 1
        else:
            self.content["game"]["current_turn"] = 0

    # Input: data: throw history
    # The function appends "data" object representing throw data to current throw history list
    def log_throw(self, data):
        set = self.content["game"]["current_set"]
        leg = self.content["game"]["current_leg"]

        if set >= len(self.content["throwHistory"]):
            self.content["throwHistory"].append([])

        if leg >= len(self.content["throwHistory"][set]):
            self.content["throwHistory"][set].append([])

        self.content["throwHistory"][set][leg].append(data)


    # returns list of displayed match and league stats keys. list[0] = match stats key, list[1] = league stats key
    def get_displayed_stats(self):
        
        retval = []

        stats = self.content["player1"]["matchStats"]
        retval.append(stats[0:stats.find(":")])

        stats = self.content["player1"]["leagueStats"]
        retval.append(stats[0:stats.find(":")])

        return retval

    # Gets the contents of the json
    def get_content(self):
        return self.content

    # Commits changes to the json
    def write(self):
        with open(self.json_path, "w") as data:
            data.write(json.dumps(self.content, ensure_ascii=False, indent=4))