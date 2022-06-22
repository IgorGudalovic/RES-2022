import unittest
from unittest import mock
from unittest.mock import MagicMock, Mock, patch
import datetime
from datetime import timedelta
from components.reader import Reader
from models.description import Description
from constants.codes import Code
from models.item import Item
import socket

class TestReader(unittest.TestCase):
    
    def test_codeselect(self):
        with mock.patch('builtins.input', return_value="1"):
            assert Reader.codeSelectionFunction() == "1"\
                or Reader.codeSelectionFunction() == "2"\
                    or Reader.codeSelectionFunction() == "3"\
                        or Reader.codeSelectionFunction() == "4"   

    def test_server_ok(self):        
            socket1 = Reader.CreateServerSocket()
            self.assertEqual(type(socket.socket()), type(socket1))

    def test_server_bad(self):        
        socket1 = Reader.CreateServerSocket()
        self.assertNotEqual(type(socket.socket()), type(socket1))    

    def test_client_ok(self):        
        socket1 = Reader.CreateClientSocket()
        self.assertEqual(type(socket.socket()), type(socket1))

    def test_client_bad(self):        
        socket1 = Reader.CreateClientSocket()
        self.assertNotEqual(type(socket.socket()), type(socket1))          
        
if __name__ == '__main__':
    unittest.main()        