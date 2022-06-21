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
         
        
if __name__ == '__main__':
    unittest.main()        