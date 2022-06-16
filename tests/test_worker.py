import datetime
import os
import unittest
import sqlite3
from components.worker import Worker
from constants.codes import Code
from constants.queries import Queries
from models.worker_property import WorkerProperty


class TestWorker(unittest.TestCase):
    def setUp(self):
        self.worker = Worker(1)
        self.conn = sqlite3.connect('test_database.db')
        cur = self.conn.cursor()

        datetime_now = datetime.datetime.now()
        self.date = datetime.datetime.strptime(
            f'{datetime_now.date()} {datetime_now.hour}:{datetime_now.minute}:{datetime_now.second}',
            '%Y-%m-%d %H:%M:%S')

        cur.execute(Queries.CreateDatasetTableQuery(1))
        cur.execute(Queries.InsertItem(1, 'CODE_ANALOG', 100, self.date))
        cur.execute(Queries.InsertItem(1, 'CODE_DIGITAL', 200, self.date))

        self.conn.commit()

    def tearDown(self):
        cur = self.conn.cursor()
        cur.execute(f"""delete from main.DATASET_1 where main.DATASET_1.value>=0""")
        self.conn.commit()
        self.conn.close()
        os.remove('test_database.db')

    def test_get_data(self):
        actual = self.worker.GetData('CODE_ANALOG', 'test_database.db')
        expected = [(self.date, WorkerProperty(Code.CODE_ANALOG, 100))]

        actual_parsed = []
        expected_parsed = []
        for a, e in zip(actual, expected):
            actual_parsed.append((a[0].__str__(), a[1].code, str(a[1].worker_value)))
            expected_parsed.append((e[0].__str__(), e[1].code.name, str(e[1].worker_value)))

        self.assertListEqual(expected_parsed, actual_parsed)
        self.assertEqual(self.worker.GetData('wrong_string'), [])

    def test_get_last_value_by_code(self):
        actual = self.worker.GetLastValueByCode('CODE_ANALOG', 'test_database.db')
        expected = 100
        self.assertEqual(expected, actual)

    def test_get_value(self):
        actual = self.worker.GetValue('CODE_ANALOG', 'test_database.db')
        expected = 100
        self.assertEqual(expected, actual)

    def test_validate_value(self):
        actual = self.worker.ValidateValue(WorkerProperty(Code.CODE_ANALOG, 103), 'test_database.db')
        expected = True
        self.assertEqual(expected, actual)

    def test_check_deadband(self):
        actual = self.worker.CheckDeadband(100, 103)
        expected = True
        self.assertEqual(expected, actual)

        actual = self.worker.CheckDeadband(100, 97)
        expected = True
        self.assertEqual(expected, actual)

        actual = self.worker.CheckDeadband(100, 101)
        expected = False
        self.assertEqual(expected, actual)

        actual = self.worker.CheckDeadband(100, 99)
        expected = False
        self.assertEqual(expected, actual)

    def test_get_dataset_by_code(self):
        actual = self.worker.GetDataSetByCode('CODE_ANALOG')
        expected = 0
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
