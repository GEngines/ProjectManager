

import config
import os
import logging

semaphore_logger = logging.getLogger(__name__)


def lock(_file):
    if _file == "db":
        with open(config.__semaphore_database, "w+") as s_db:
            s_db.write("")
            semaphore_logger.debug("Finished Writing {}".format(config.__semaphore_database))
    if _file == "guid":
        with open(config.__semaphore_guid, "w+") as s_guid:
            s_guid.write("")
            semaphore_logger.debug("Finished Writing {}".format(config.__semaphore_guid))


def unlock(_file):
    if _file == "db":
        os.remove(config.__semaphore_database)
        semaphore_logger.debug("Removed {}".format(config.__semaphore_database))
    if _file == "guid":
        os.remove(config.__semaphore_guid)
        semaphore_logger.debug("Removed {}".format(config.__semaphore_guid))


def is_locked(_file):
    if _file == "guid":
        return os.path.exists(config.__semaphore_guid)
    if _file == "db":
        return os.path.exists(config.__semaphore_database)


