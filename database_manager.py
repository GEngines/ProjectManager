import os
import json
import utility
import UIDGenerator
import semaphore
import logging

db_logger = logging.getLogger(__name__ + "DB")


class DB(metaclass=utility.Singleton):
    def __init__(self):
        self.db_file = UIDGenerator.config.database_file
        self.guid = UIDGenerator.GUID()
        self.db_data = {}
        if os.path.exists(self.db_file):
            self.db_data = self._read_database_file()
        db_logger.info("Database Initialized!")

    def reload_database(self):
        self.db_data = self._read_database_file()

    def _read_database_file(self):
        with open(self.db_file, "r") as r:
            return json.load(r)

    def _write_to_database(self):
        while semaphore.is_locked("db"):
            db_logger.debug("DB file currently locked. Waiting...")
            pass
        db_logger.debug("Locking DB file...")
        semaphore.lock("db")
        with open(self.db_file, "w+") as w:
            json.dump(self.db_data, w, indent=4)
        semaphore.unlock("db")
        db_logger.debug("Unlocking DB file.")

    def print_data(self):
        print(self.db_data)

    def write_to_disk(self):
        self._write_to_database()

    def add_to_db(self, file_name, project_type, validation_status):

        # check if file exists,
        _file_exists = self.guid.check_if_exists_in_guid(file_name)
        if _file_exists is not None:
            _id = _file_exists
        else:
            _id = self.guid.add_to_guid_db(file_name)

        generated_dict = {
            "file_name": file_name,
            "perforce_file_path": "",
            "perforce_user_name": utility.Perforce().user,
            "perforce_client_name": utility.Perforce().client_name,
            "perforce_server_address": utility.Perforce().server_address,
            "status": "",
            "validation": validation_status,
            "reviewer_name": "",
            "display_name": utility.get_windows_display_name(),
            "project_type": project_type,
            "guid": _id
        }

        self.db_data[str(_id)] = generated_dict
        self._write_to_database()

        return utility.get_object(generated_dict)
