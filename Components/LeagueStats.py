import os
import json

# Class to update, read, and validate league stats database
class LeagueStats():

    # Sets the initial scores of a player added to the database to 0 or nothing
    def __init__(self):
        self.json_path = "league_stats.json"

        self.initial = {"turns": 0, "sum": 0, "League Rank": -1, "Last Win": "No Wins", "Average League Score": 0, "Lifetime 180s": 0, "Wins": 0}

        if not os.path.exists(self.json_path):
            with open(self.json_path, "w") as data:
                data.write(json.dumps({}, ensure_ascii=False, indent=4))

        with open(self.json_path) as data:
                self.content = json.loads(data.read())

    # Input: name: Player Name
    # The purpose of this function is to add the player to the database
    def add_player(self, name):
        if name not in list(self.content.keys()):   # if player is not already added
            self.content[name] = self.initial       # sets name of player
            self.update_ranks()                     # Reupdates the ranks for everyone
            self.write()                            # commit it

    # Input: player: Player Name
    # Input: stat: The name of the stat
    # Output: The stat
    # The purpose of this function is to retrieve a specified stat of a player
    def get_stat(self, player, stat):
        if player in list(self.content.keys()):     # if player is in the database
            return self.content[player][stat]       # return the information
        return ""

    # Input: player: Player Name
    # Input: stat: The name of the stat
    # Input: val: The new value of the stat
    # The purpose of this function is to set a specified stat of a player    
    def update_stat(self, player, stat, val):       
        self.add_player(player)             # make sure player is in database and add if not
        self.content[player][stat] = val    # change the stat
        self.write()                        # commit stat change
    
    # Input: player: Player Name
    # Output: the number of turns
    # TODO: (IS this correct) The purpose of this function is to keep track of the overall number of 
    # throws a player has taken
    def increment_turn(self, player):
        self.add_player(player)             # make sure player is in database and add if not
        self.content[player]["turns"] +=1   # increment turns
        self.write()                        # commit
        return self.content[player]["turns"]

    # Input: player: Player Name
    # The purpose of this function is to add win to player's stats
    def increment_win(self, player):
        self.add_player(player)
        self.content[player]["Wins"] +=1
        
        self.write()

    # refresh rankings
    # ranking is based on number of wins
    def update_ranks(self):
        player_list = []
        for key in list(self.content.keys()): # for each player
            temp = []
            temp.append(key)
            temp.append(self.content[key]["Wins"])

            player_list.append(temp)

        player_list.sort(reverse = True, key = self.sort_func) # sort by most wins (first is highest)

        count = 1

        for pair in player_list:
            self.content[pair[0]]["League Rank"] = count
            count += 1
        self.write()

    # TODO: What is the purpose of this function
    def sort_func(self, pair):
        return pair[1]

    # Input: player: Player Name
    # Input: score: the total score from the three darts thrown
    # The purpose of this function is to increment sum with score
    def add_score(self, player, score):
        self.add_player(player)
        self.content[player]["sum"] += score
        self.write()

    # Input: player: Player Name
    # The purpose of this function is to delete a player from the json
    def delete_player(self, player):
        self.content.pop(player, None)
        self.update_ranks()
        self.write()

    # The purpose of this function is to update the json
    def write(self):
        with open(self.json_path, "w") as data:
            data.write(json.dumps(self.content, ensure_ascii=False, indent=4))
