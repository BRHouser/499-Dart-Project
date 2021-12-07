import os
import time

# This class checks the current game state for updates, and returns the current game state once updated
# Author: Ben Houser
# Created 10/27/21, edited 11/29/21

class UpdateScoreboard():

    first_read = True
    
    # Sets initial states for current_game_state json 
    def __init__(self, first_read):
        self.json_path = 'current_game_state.json'
        self.first_read = first_read


    # Input: req_time: time between checks
    # This function checks if current game state has been updated
    def is_updated(self, req_time):
        return os.stat(self.json_path).st_mtime > req_time

    # Returns the current game state 
    def get_current_game_state(self):
        try:
            #busy wait until game state is updated, return current game state when it is
            req_time = time.time()
            if self.first_read:
                with open(self.json_path) as data:
                    content = data.read()
                return content
            while not self.is_updated(req_time):
                time.sleep(.25) #check again after sleep
        
            with open(self.json_path) as data:
                content = data.read()
            return content
        except FileNotFoundError:
            return {}