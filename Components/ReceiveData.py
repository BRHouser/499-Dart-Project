import json


class ReceiveData():

    def __init__(self, data):
        self.data = data

        #temporary testing below
        with open('test.json', 'w') as f:
            f.write(str(json.dumps(data)))

