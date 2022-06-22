import sys
sys.path.append('../')
class Request:
    def __init__(self, option: str, data: str):
        self.option = option
        self.data = data
