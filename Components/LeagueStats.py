import os
import json

# Class to update, read, and validate league stats database
#Author

class LeagueStats():

    def __init__(self):
        self.json_path = "league_stats.json"

        self.initial = {"turns": 0, "sum": 0, "League Rank": -1, "Last Win": "No Wins", "Average League Score": 0, "Lifetime 180s": 0, "Wins": 0}

        if not os.path.exists(self.json_path):
            with open(self.json_path, "w") as data:
                data.write(json.dumps({}, ensure_ascii=False, indent=4))

        with open(self.json_path) as data:
                self.content = json.loads(data.read())

    def add_player(self, name):
        if name not in list(self.content.keys()):
            self.content[name] = self.initial
            self.update_ranks()
            self.write()

    def get_stat(self, player, stat):
        if player in list(self.content.keys()):
            return self.content[player][stat]
        return ""

    def update_stat(self, player, stat, val):
        self.add_player(player)
        self.content[player][stat] = val 
        self.write()

    def delete_player(self, name):
        print("HERE")
        #IMPLEMENT HERE PLZ          

    def increment_turn(self, player):
        self.add_player(player)
        self.content[player]["turns"] +=1
        
        self.write()
        return self.content[player]["turns"]

    # add win to player's stats
    def increment_win(self, player):
        self.add_player(player)
        #print("win for " + player)
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

        #print("\n")

        #print(player_list)
        count = 1

        #TODO: obscure bug: if there are no players in league_stats.json, upon starting a game the two players will both be ranked 2
        for pair in player_list:
            #print(count)
            #print(pair[0])
            self.content[pair[0]]["League Rank"] = count
            count += 1
            #print(self.content)

        #print(self.content)
        self.write()

    def sort_func(self, pair):
        return pair[1]

    def add_score(self, player, score):
        self.add_player(player)
        self.content[player]["sum"] += score
        
        self.write()

    def write(self):
        with open(self.json_path, "w") as data:
            data.write(json.dumps(self.content, ensure_ascii=False, indent=4))
