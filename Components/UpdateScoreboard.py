import os
import time

from flask.wrappers import Request

# This class checks the current game state for updates, and returns the current game state once updated
class UpdateScoreboard():

    first_read = True

    def __init__(self, first_read):

        self.first_read = first_read
        #print(first_read)

    def is_updated(self, req_time):
        #checks if current game state has been updated
        #print("check is updated")
        return os.stat('current_game_state.json').st_mtime > req_time

    def get_current_game_state(self):
        #print("get current game state")
        #busy wait until game state is updated, return current game state when it is
        req_time = time.time()
        if self.first_read:
            with open('current_game_state.json') as data:
                content = data.read()
            return content
        #print("busy wait")
        while not self.is_updated(req_time):
            time.sleep(.25)
    
        with open('current_game_state.json') as data:
            content = data.read()
        return content