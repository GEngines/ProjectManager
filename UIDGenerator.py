# this script will store the files locally, and keep a track of the serial numbers assigned to the file.

import os
import json
import utility
import config
import semaphore
import logging

guid_logger = logging.getLogger(__name__ + ".GUID")


class GUID(metaclass=utility.Singleton):
    def __init__(self):
        self.guid_file = config.guid_file
        self.guid_data = {}
        if os.path.exists(self.guid_file):
            self.guid_data = self._read_guid_file()
        guid_logger.info("GUID Initialized!")

    def reload_guid_file(self):
        self.guid_data = self._read_guid_file()

    def _read_guid_file(self):
        with open(self.guid_file, "r") as r:
            return json.load(r)

    def _write_guid_(self):
        while semaphore.is_locked("guid"):
            guid_logger.debug("GUID file currently locked. Waiting...")
            pass
        guid_logger.debug("GUID file available. Locking...")
        semaphore.lock("guid")
        with open(self.guid_file, "w+") as g:
            json.dump(self.guid_data, g, indent=4)
        semaphore.unlock("guid")
        guid_logger.debug("GUID file update complete. Unlocking...")

    def add_to_guid_db(self, file_name):
        _id = self._get_unique_id()
        self.guid_data[file_name] = _id
        self._write_guid_()
        return _id

    def _get_unique_id(self):
        for _id in range(0, len(self.guid_data.values()) + 1, 1):
            if _id not in list(self.guid_data.values()):
                return _id

    def get_file_name_from_id(self, _id):
        _id = int(_id)
        if _id in [*self.guid_data.values()]:
            for k,v in self.guid_data.items():
                if _id == v:
                    return k
        return None

    def get_id_from_file_name(self, file_name):
        if file_name in [*self.guid_data.keys()]:
            for k, v in self.guid_data.items():
                if k == file_name:
                    return v
        return None

    def check_if_exists_in_guid(self, file_name):
        return self.get_id_from_file_name(file_name)

