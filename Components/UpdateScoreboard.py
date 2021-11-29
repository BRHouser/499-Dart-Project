import os
import time

from flask.wrappers import Request

# This class checks the current game state for updates, and returns the current game state once updated
# Author: Ben Houser

class UpdateScoreboard():

    first_read = True

    def __init__(self, first_read):
        self.json_path = 'current_game_state.json'
        self.first_read = first_read
        #print(first_read)

    def is_updated(self, req_time):
        #checks if current game state has been updated
        return os.stat(self.json_path).st_mtime > req_time

    def get_current_game_state(self):
        try:
            #print("get current game state")
            #busy wait until game state is updated, return current game state when it is
            req_time = time.time()
            if self.first_read:
                with open(self.json_path) as data:
                    content = data.read()
                return content
            #print("busy wait")
            while not self.is_updated(req_time):
                time.sleep(.25) #check again after sleep
        
            with open(self.json_path) as data:
                content = data.read()
            return content
        except FileNotFoundError:
            return {}