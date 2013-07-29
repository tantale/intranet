"""
:module: intranet.model.file_storage
:date: 2013-07-28
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import collections
import errno
import os


def safe_makedirs(path):
    try:
        os.makedirs(path)
    except OSError as cause:
        if cause.errno != errno.EEXIST or not os.path.isdir(path):
            raise


def safe_remove(path):
    try:
        os.remove(path)
    except OSError as cause:
        if cause.errno != errno.ENOENT:
            raise


class FileStorage(collections.Mapping):
    """
    Repository for uploaded files.
    """
    IGNORE_LIST = '.git', '.svn', 'CVS'

    def __init__(self, file_storage_dir, *args, **kwargs):
        """
        Initialize the file storage

        :param file_storage_dir: file storage's full path
        """
        self.file_storage_dir = os.path.normpath(file_storage_dir)
        collection = args[0] if len(args) == 1 else None
        if isinstance(collection, collections.Mapping):
            for key, value in collection.iteritems():
                self[key] = value
        elif isinstance(collection, collections.Iterable):
            for entry in collection:
                key, value = entry
                self[key] = value
        else:
            for key, value in kwargs.iteritems():
                self[key] = value

    def _get_fullpath(self, relpath):
        # TODO: check that subdirs not in IGNORE_LIST
        return os.path.normpath(os.path.join(self.file_storage_dir, relpath))

    def __contains__(self, relpath):
        """
        relpath in file_storage -> True if the file exists, else False.

        :param relpath: file's relative path
        """
        fullpath = self._get_fullpath(relpath)
        return os.path.isfile(fullpath)

    def __getitem__(self, relpath):
        """
        file_storage[relpath] -> file data, or raise KeyError.

        :param relpath: file's relative path
        """
        try:
            fullpath = self._get_fullpath(relpath)
            with file(fullpath, 'rb') as data_file:
                return data_file.read()
        except IOError as cause:
            if cause.errno == errno.ENOENT:
                msg_fmt = "Stored file '{relpath}' not found, cause: {cause}"
                raise KeyError(msg_fmt.format(relpath=relpath, cause=cause))
            raise  # FATAL error

    def __setitem__(self, relpath, data):
        """
        file_storage[relpath] = data

        :param relpath: file's relative path
        :param data: file content to store
        """
        fullpath = self._get_fullpath(relpath)
        safe_makedirs(os.path.dirname(fullpath))
        safe_remove(fullpath)
        with file(fullpath, 'wb') as data_file:
            data_file.write(data)

    def __delitem__(self, relpath):
        """
        del file_storage[relpath]

        :param relpath: file's relative path
        """
        fullpath = self._get_fullpath(relpath)
        try:
            os.remove(fullpath)
        except OSError as cause:
            if cause.errno == errno.ENOENT:
                msg_fmt = "Stored file '{relpath}' not found, cause: {cause}"
                raise KeyError(msg_fmt.format(relpath=relpath, cause=cause))
            raise  # FATAL error

    def __iter__(self):
        """
        for relpath in file_storage -> an iterator over file's relative path
        """
        for root, dir_list, name_list in os.walk(self.file_storage_dir):
            for ignore in self.IGNORE_LIST:
                if ignore in dir_list:
                    dir_list.remove(ignore)
            for filename in name_list:
                fullpath = os.path.join(root, filename)
                relpath = os.path.relpath(fullpath, self.file_storage_dir)
                yield relpath

    def __len__(self):
        """
        len(file_storage) -> the number of stored files.
        """
        return len(self.keys())

    def keys(self):
        """
        file_storage.keys() -> list of stored files.
        """
        return [key for key in self]

    def __eq__(self, other):
        """
        file_storage1 == file_storage2 -> True if the mappings are equals

        :param other: other file_storage or dictionary.
        """
        return not (self != other)

    def __ne__(self, other):
        """
        file_storage1 != file_storage2 -> True if the mappings are differents

        :param other: other file_storage or dictionary.
        """
        if not isinstance(other, collections.Mapping):
            return NotImplemented
        self_keys = self.keys()
        other_keys = other.keys()
        if set(self_keys) != set(other_keys):
            return True
        for key in self_keys:
            if self[key] != other[key]:
                return True
        return False
