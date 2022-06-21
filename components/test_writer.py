import unittest
import socket

from writer import Writer
from unittest import mock
from unittest.mock import MagicMock, Mock, patch

class TestWriter(unittest.TestCase):

    def test_connect1_ok(self):        
        socket1 = Writer.CreateClientSocket1()
        self.assertEqual(type(socket.socket()), type(socket1))
        
    def test_connect1_wrong(self):        
        socket1 = Writer.CreateClientSocket1()
        self.assertNotEqual(type(socket.socket()), type(socket1))    
        
    def test_connect2_ok(self):        
        socket1 = Writer.CreateClientSocket2()
        self.assertEqual(type(socket.socket()), type(socket1))
        
    def test_connect2_wrong(self):        
        socket1 = Writer.CreateClientSocket2()
        self.assertNotEqual(type(socket.socket()), type(socket1))
    
    def test_Input(self):
        with mock.patch('builtins.input', return_value="1"):
            assert Writer.inputState() == "1"       
            
    def test_Input_bad(self):
        with mock.patch('builtins.input', return_value=None):
            assert Writer.inputState() == None                  
                
       
if __name__ == '__main__':
    unittest.main()
        