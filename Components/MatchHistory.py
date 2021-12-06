import os
import json

class MatchHistory():
    def __init__(self):
        self.json_path="match_history.json"

        self.initial={"player1":"","player2":"","throws":{}}

        if not os.path.exists(self.json_path):
            with open(self.json_path, "w") as data:
                data.write(json.dumps({}, ensure_ascii=False, indent=4))

        with open(self.json_path) as data:
                self.content = json.loads(data.read())

    def add_match(self,game,matchName,p1Name,p2Name, date):
        if matchName not in list(self.content.keys()):
            self.content[matchName]=self.initial
            self.content[matchName]["player1"]=p1Name
            self.content[matchName]["player2"]=p2Name
            self.content[matchName]["throws"]=game
            self.content[matchName]["date"]=date
            self.write()

    def write(self):
        with open(self.json_path, "w") as data:
            data.write(json.dumps(self.content, ensure_ascii=False, indent=4))

