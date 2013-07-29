"""
:module: intranet.tests.test_file_storage
:date: 2013-07-28
:author: Laurent LAPORTE <sandlol2009@gmail.com>

Test case of 'intranet.model.file_storage' module.
"""
from intranet.model.file_storage import safe_makedirs, FileStorage
import os
import shutil
import tempfile
import unittest


class TestFileStorage(unittest.TestCase):
    """
    Test case of 'FileStorage' class.
    """

    def __init__(self, methodName='runTest'):
        super(TestFileStorage, self).__init__(methodName=methodName)
        self.tempdir = None

    @staticmethod
    def create_tempdir():
        return tempfile.mkdtemp(prefix=__name__ + '.', suffix='.tmp')

    @staticmethod
    def delete_tempdir(tempdir):
        shutil.rmtree(tempdir, ignore_errors=True)

    def setUp(self):
        super(TestFileStorage, self).setUp()
        self.tempdir = self.create_tempdir()

    def tearDown(self):
        self.delete_tempdir(self.tempdir)
        super(TestFileStorage, self).tearDown()

    def test_safe_makedirs(self):
        dir_path = os.path.join(self.tempdir, 'toto', 'titi')
        safe_makedirs(dir_path)
        self.assertTrue(os.path.isdir(dir_path),
                        'Missing directory: "{}"'.format(dir_path))
        safe_makedirs(dir_path)
        self.assertTrue(os.path.isdir(dir_path),
                        'Missing directory: "{}"'.format(dir_path))
        text_path = os.path.join(dir_path, 'my_file.txt')
        with file(text_path, "w") as text_file:
            text_file.write("content\n")
        with self.assertRaises(OSError):
            safe_makedirs(text_path)

    def test_contains(self):
        file_storage = FileStorage(self.tempdir)

        # -- empty file_storage
        self.assertFalse('my_path.txt' in file_storage)
        self.assertTrue('my_path.txt' not in file_storage)
        self.assertFalse(file_storage)
        self.assertTrue(not file_storage)

        # -- one file in file_storage
        my_path = os.path.join(self.tempdir, 'my_path.txt')
        with file(my_path, 'w') as my_file:
            my_file.write("my data")
        self.assertTrue('my_path.txt' in file_storage)
        self.assertFalse('my_path.txt' not in file_storage)
        self.assertTrue(file_storage)
        self.assertFalse(not file_storage)

    def test_len(self):
        file_storage = FileStorage(self.tempdir)

        # -- empty file_storage
        actual = len(file_storage)
        self.assertEqual(actual, 0, "empty storage expected")

        # -- one file in file_storage
        my_path = os.path.join(self.tempdir, 'my_path.txt')
        with file(my_path, 'w') as my_file:
            my_file.write("my data")
        actual = len(file_storage)
        self.assertEqual(actual, 1, "one file expected")

        # -- one directory and two files in file_storage
        my_path = os.path.join(self.tempdir, 'subdir', 'my_path.txt')
        os.makedirs(os.path.dirname(my_path))
        with file(my_path, 'w') as my_file:
            my_file.write("my data")
        actual = len(file_storage)
        self.assertEqual(actual, 2, "two files expected")

        # -- one directory and two files in file_storage
        for ignore in ('.git', '.svn', 'CVS'):
            my_path = os.path.join(self.tempdir, ignore, 'my_path.txt')
            os.makedirs(os.path.dirname(my_path))
            with file(my_path, 'w') as my_file:
                my_file.write("my data")
        actual = len(file_storage)
        self.assertEqual(actual, 2, "two files expected")

    def test_getitem(self):
        file_storage = FileStorage(self.tempdir)

        # -- empty file_storage
        with self.assertRaises(KeyError):
            file_storage['my_path.txt']
        with self.assertRaises(KeyError):
            file_storage['subdir/my_path.txt']
        if os.name == "nt":
            with self.assertRaises(EnvironmentError):
                file_storage['?']

        # -- one file in file_storage
        my_path = os.path.join(self.tempdir, 'my_path.txt')
        with file(my_path, 'w') as my_file:
            my_file.write("my data")
        actual = file_storage['my_path.txt']
        self.assertEqual(actual, "my data", "corupted data")

    def test_setitem(self):
        file_storage = FileStorage(self.tempdir)

        # -- empty file_storage
        file_storage['my_path.txt'] = "my data"
        my_path = os.path.join(self.tempdir, 'my_path.txt')
        with file(my_path, 'r') as my_file:
            self.assertEqual(my_file.read(), "my data")

        # -- overwrite
        file_storage['my_path.txt'] = "my new data"
        with file(my_path, 'r') as my_file:
            self.assertEqual(my_file.read(), "my new data")

        # -- with subdir
        file_storage['subdir/my_path.txt'] = "my other data"
        my_path = os.path.join(self.tempdir, 'subdir', 'my_path.txt')
        with file(my_path, 'r') as my_file:
            self.assertEqual(my_file.read(), "my other data")

    def test_delitem(self):
        file_storage = FileStorage(self.tempdir)

        # -- empty file_storage
        with self.assertRaises(KeyError):
            del file_storage['my_path.txt']
        with self.assertRaises(KeyError):
            del file_storage['subdir/my_path.txt']
        if os.name == "nt":
            with self.assertRaises(EnvironmentError):
                del file_storage['?']

        # -- one file in file_storage
        my_path = os.path.join(self.tempdir, 'my_path.txt')
        with file(my_path, 'w') as my_file:
            my_file.write("my data")
        del file_storage['my_path.txt']
        self.assertFalse(os.path.exists(my_path))

    def test_iter(self):
        file_storage = FileStorage(self.tempdir)

        # -- create some files
        path_list = ['path1.txt', 'path2.txt', 'path3.txt',
                     'subdir1/path1.txt', 'subdir1/path2.txt',
                     'subdir2/path1.txt', 'subdir2/path2.txt',
                     'subdir1/folder1/path1.txt', 'subdir1/folder1/path2.txt']
        for path in path_list:
            file_storage[path] = "content of '{}'".format(path)

        # -- iterate over the file_storage
        actual_list = [path for path in file_storage]

        # -- check the result
        actual_list.sort()
        expected_list = [os.path.normpath(path) for path in path_list]
        expected_list.sort()
        self.assertEquals(actual_list, expected_list)

        # -- iterate with 'iter'
        actual_list = [path for path in iter(file_storage)]

        # -- check the result
        actual_list.sort()
        expected_list = [os.path.normpath(path) for path in path_list]
        expected_list.sort()
        self.assertEquals(actual_list, expected_list)

    def test_eq_ne(self):
        dict1 = {'file1.txt': "content1",
                 'file2.txt': "content2",
                 'file3.txt': "content3"}
        dict2 = {'file1.txt': "content1",
                 'file3.txt': "content3",
                 'file4.txt': "content4"}

        file_storage1_dir = os.path.join(self.tempdir, 'file_storage1')
        file_storage2_dir = os.path.join(self.tempdir, 'file_storage2')
        file_storage3_dir = os.path.join(self.tempdir, 'file_storage3')

        file_storage1 = FileStorage(file_storage1_dir, dict1)
        file_storage2 = FileStorage(file_storage2_dir, dict2)
        file_storage3 = FileStorage(file_storage3_dir, dict2)  # same as 2

        # -- compare with another file_storage

        self.assertTrue(file_storage1 == file_storage1)
        self.assertTrue(file_storage1 != file_storage2)
        self.assertTrue(file_storage1 != file_storage3)

        self.assertTrue(file_storage2 != file_storage1)
        self.assertTrue(file_storage2 == file_storage2)
        self.assertTrue(file_storage2 == file_storage3)

        self.assertTrue(file_storage3 != file_storage1)
        self.assertTrue(file_storage3 == file_storage2)
        self.assertTrue(file_storage3 == file_storage3)

        # -- compare with a classic dictionary

        self.assertTrue(file_storage1 == dict1)
        self.assertTrue(file_storage1 != dict2)

        self.assertTrue(file_storage2 != dict1)
        self.assertTrue(file_storage2 == dict2)

        self.assertTrue(file_storage3 != dict1)
        self.assertTrue(file_storage3 == dict2)


if __name__ == "__main__":
    unittest.main()
