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

    def getList(cls):
        #cstrList vraca string vrednosti enuma
        strList = Code._member_names_
        return strList