import datetime
import os
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch
import LogCleaner


class TestLogCleaner(TestCase):
    """ methods to mock:
        get_file_stat(file)
        get_file_list(path)
        check_access_to_path(path)"""

    @patch('LogCleaner.LogCleaner.get_file_list')
    @patch('LogCleaner.LogCleaner.get_modification_time')
    def test_list_files_older_than(self, modification_time, file_list):
        path = 'C:\\Procs\\Was_Imports\\Logs'

        cleaner = LogCleaner.LogCleaner()

        cleaner.get_file_list = file_list
        cleaner.get_file_list.return_value = [
            "%s%slog_1.xml" % (path, os.sep)
        ]
        cleaner.get_modification_time = modification_time
        cleaner.get_modification_time.return_value = datetime.datetime.now() - datetime.timedelta(hours=178)

        result = cleaner.list_files_older_than(168, path)

        self.assertEqual("%s\\log_1.xml" % path, result[0])

    @patch('LogCleaner.LogCleaner.get_file_list')
    @patch('LogCleaner.LogCleaner.get_modification_time')
    @patch('LogCleaner.LogCleaner.check_access_to_path')
    def test_list_paths_with_anteriores_subfolder(self, access_to_path, modification_time, file_list):
        path = 'C:\\Procs\\Was_Imports\\Logs'
        dataset = [
            "%s%sCliente2" % (path, os.sep),
            "%s%sCliente1%sAnteriores" % (path, os.sep, os.sep)
        ]
        cleaner = LogCleaner.LogCleaner()

        cleaner.get_file_list = file_list
        cleaner.get_file_list.return_value = dataset
        cleaner.get_modification_time = modification_time
        cleaner.get_modification_time.return_value = datetime.datetime.now() - datetime.timedelta(hours=178)
        cleaner.get_access_to_path = access_to_path
        cleaner.get_access_to_path.return_value = True

        result = cleaner.list_paths_with_given_subfolder(path, "Anteriores")
        self.assertListEqual(result, [
            "%s%sCliente2%sAnteriores" % (path, os.sep, os.sep),
            "%s%sCliente1%sAnteriores%sAnteriores" % (path, os.sep, os.sep, os.sep)
        ])

    def test_remove_listed_files(self):
        self.assertTrue(True)
