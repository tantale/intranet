"""
:module: intranet.controllers.file_storage
:date: 2013-07-29
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from intranet.lib.base import BaseController
from intranet.model.file_storage import FileStorage
from tg.decorators import expose
import logging
import tg


LOG = logging.getLogger(__name__)


class FileStorageController(BaseController):
    """
    file storage controller used to extract stored files (like photos).
    """
    @expose(content_type='image/jpg')
    def _default(self, *relpath_list, **kwargs):
        relpath = "/".join(relpath_list) + '.jpg'

        if LOG.isEnabledFor(logging.DEBUG):
            msg_fmt = "Try to extract the data stored in: '{relpath}'"
            LOG.debug(msg_fmt.format(relpath=relpath))

        file_storage = FileStorage(tg.config.file_storage_dir)
        return file_storage[relpath]
