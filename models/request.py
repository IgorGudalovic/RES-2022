import sys
sys.path.append('../')
class Request:
    def __init__(self, option:str, data ):
        self.option = option
        self.data = data
