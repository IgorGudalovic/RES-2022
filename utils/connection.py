from mysql import connector


class Connector:
    @staticmethod
    def GetConnection():
        return connector.connect(host='localhost', user='user', passwd='passwd', database='mysql')
