from enum import Enum


class Code(Enum):
    CODE_ANALOG = 1
    CODE_DIGITAL = 2
    CODE_CUSTOM = 3
    CODE_LIMITSET = 4
    CODE_SINGLENOE = 5
    CODE_MULTIPLENODE = 6
    CODE_CONSUMER = 7
    CODE_SOURCE = 8

    def __eq__(self, other):
        if isinstance(other, Code):
            if self.name == other.name:
                return True
            else:
                return False
        elif isinstance(other, str):
            if self.name == other:
                return True
            else:
                return False


Codes = [Code.CODE_ANALOG.name, Code.CODE_DIGITAL.name, Code.CODE_CUSTOM.name, Code.CODE_LIMITSET.name,
         Code.CODE_SINGLENOE.name, Code.CODE_MULTIPLENODE.name, Code.CODE_CONSUMER.name, Code.CODE_SOURCE.name]
