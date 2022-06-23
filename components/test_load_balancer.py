import unittest
import socket
from unittest import TestCase

from load_balancer import LoadBalancer
from models.description import Description
from constants.codes import Code
from models.item import Item
from constants.data_sets import DataSet

from unittest.mock import MagicMock, patch

class TestLoadBalancer(TestCase):

    def test_forward_data_prepare(self):
        lb = LoadBalancer([])
        code1 = Code.CODE_ANALOG
        value1 = 5
        item1 = Item(code1, value1)
        items = []
        items.append(item1)
        description1 = Description(1, items, DataSet.DataSet_1)
        actual_description = lb.ForwardDataPrepare(item1)
        self.assertEqual(description1.dataset, actual_description.dataset)

    def test_buffer_empty(self):
        mocklb = MagicMock(LoadBalancer)
        d = MagicMock(Description)
        self.assertNotEqual(LoadBalancer.Buffer(mocklb), d)

    #@patch('components.load_balancer.LoadBalancer.CreateServerSocket2')
    #def test_receive_state(self, mock_CreateServerSocket2):
    #    mock_socket = MagicMock(socket.socket)
    #    mock_socket.recv = MagicMock(return_value=4)
    #    mock_CreateServerSocket2.return_value = mock_socket
    #    mocklb = MagicMock(LoadBalancer)
    #    self.assertNotEqual(LoadBalancer.ReceiveState(mocklb), None)

    #@patch('components.load_balancer.LoadBalancer.CreateServerSocket1')
    #def test_receive_item(self, mock_CreateServerSocket1):
    #    mock_socket = MagicMock(socket.socket)
    #    mock_socket.recv = MagicMock(return_value=None)
    #    mock_CreateServerSocket1.return_value = mock_socket
    #    mocklb = MagicMock(LoadBalancer)
    #    self.assertEqual(LoadBalancer.ReceiveItem(mocklb), None)


if name == 'main':
    unittest.main()