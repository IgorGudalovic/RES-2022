import unittest
from unittest.mock import Mock

from components.load_balancer import LoadBalancer
from models.description import Description
from constants.codes import Code
from models.item import Item
from components.load_balancer import descID

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
        

        
        
        


if __name__ == '__main__':
    unittest.main()