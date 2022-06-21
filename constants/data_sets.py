from constants.codes import *


class DataSet(Enum):
    DataSet_1 = (Code.CODE_ANALOG, Code.CODE_DIGITAL)
    DataSet_2 = (Code.CODE_CUSTOM, Code.CODE_LIMITSET)
    DataSet_3 = (Code.CODE_SINGLENOE, Code.CODE_MULTIPLENODE)
    DataSet_4 = (Code.CODE_CONSUMER, Code.CODE_SOURCE)


DataSets = [DataSet.DataSet_1.name, DataSet.DataSet_2.name, DataSet.DataSet_3.name, DataSet.DataSet_4.name]
