import unittest
from unittest.mock import Mock

from components.load_balancer import LoadBalancer
from models.description import Description
from constants.codes import Code
from models.item import Item
from components.load_balancer import descID
import socket

class TestLoadBalancer(unittest.TestCase):
    
    def test_forwarddataprepare(self):
        code1 = Code.CODE_ANALOG
        value1 = 5  
        item1 = Item(code1, value1)
        items = []
        items.append(item1)
        description1 = Description(1, items, 1)
        actual_description = LoadBalancer.ForwardDataPrepare(item1)
        self.assertEqual(description1, actual_description)
        
    def test_connect1_ok(self):        
        socket1 = LoadBalancer.CreateServerSocket1()
        self.assertEqual(type(socket.socket()), type(socket1))
        
    def test_connect1_wrong(self):        
        socket1 = LoadBalancer.CreateServerSocket1()
        self.assertNotEqual(type(socket.socket()), type(socket1))    
        
    def test_connect2_ok(self):        
        socket1 = LoadBalancer.CreateServerSocket2()
        self.assertEqual(type(socket.socket()), type(socket1))
        
    def test_connect2_wrong(self):        
        socket1 = LoadBalancer.CreateServerSocket2()
        self.assertNotEqual(type(socket.socket()), type(socket1))                  

if __name__ == '__main__':
    unittest.main()