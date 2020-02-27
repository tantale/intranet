# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import glob
import logging
import os
import shutil

HERE = os.path.dirname(__file__)
PROJECT_DIR = os.path.dirname(os.path.dirname(HERE))
BACKUP_DIR = os.path.join(PROJECT_DIR, "__backup")
assert os.path.isdir(BACKUP_DIR)

LOG = logging.getLogger("intranet.restore_backup_db")


def restore_backup_db():
    LOG.info("Restore DB from '{path}'...".format(path=BACKUP_DIR))
    for db_path in glob.glob(os.path.join(BACKUP_DIR, "*data.db")):
        db_name = os.path.basename(db_path)
        if db_name.startswith(("_")):
            continue
        target_path = os.path.join(PROJECT_DIR, db_name)
        msg_fmt = "- Overwrite DB: '{name}'..." if os.path.exists(target_path) else "- Copy DB: '{name}'..."
        level = logging.WARNING if os.path.exists(target_path) else logging.INFO
        LOG.log(level, msg_fmt.format(name=db_name))
        shutil.copyfile(db_path, target_path)
    LOG.info("Restoration done.".format(path=BACKUP_DIR))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(levelname)-8s: %(name)-27s: %(message)s")
    restore_backup_db()
