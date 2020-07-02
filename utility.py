# add a func to copy file
import os
import shutil
import subprocess
import stat
import config
import re
import logging
import time

# logging set up

logging.basicConfig(level=logging.DEBUG, format="(%(asctime)s) %(name)-8s %(levelname)-8s %(message)s",
                    datefmt="%d-%m-%y %H:%M:%S",
                    filename="{0}/project_tool_{1}.log".format(os.environ["temp"], time.strftime("%Y%m%d_%H%M%S")),
                    filemode="w")

utility_logger = logging.getLogger(__name__ + ".Utility")


def copy_files_to_server(source_location, destination_location):
    shutil.copy2(source_location, destination_location)


def get_file_path(file_name, destination_location):
    for root, dirs, files in os.walk(destination_location):
        if file_name in files:
            return os.path.join(root, file_name)


def get_files_from_directory(src):
    _local_list = []
    for root, dirs, files in os.walk(src):
        if files:
            for _file in files:
                _local_list.append([_file, root])
    return _local_list


def copy_files_to_perforce_folder(source_path, destination_location="z:\\"):
    destination_path = get_file_path(os.path.basename(source_path), destination_location)
    if not os.access(destination_path, os.W_OK):
        utility_logger.info("File is read-only -> {}. Updating to Writeable".format(destination_path))
        os.chmod(destination_path, stat.S_IWRITE)
    shutil.copy2(source_path, destination_path)


def write_to_perforce_config(_server, _user, _client):
    print(config.perforce_data_file)
    with open(config.perforce_data_file, "w+") as _p:
        _p.write("P4PORT={}\nP4USER={}\nP4CLIENT={}".format(_server, _user, _client))


def read_p4config(config_path):
    if os.path.isfile(config_path):
        _p4_data = ""
        with open(config_path, "r") as _p4_file:
            _p4_data = _p4_file.readlines()
        regex_str = r".+P4PORT=(\S+)\\n.+P4USER=(\S+)\\n.+P4CLIENT=(\S+)'.+"
        try:
            _server, _user, _client = re.match(regex_str, str(_p4_data)).group(1, 2, 3)
            write_to_perforce_config(_server, _user, _client)
            return True
        except AttributeError:
            return False
    return None


def read_from_perforce_config():
    _data = ""
    with open(config.perforce_data_file, "r") as _p:
        _data = _p.readlines()
    regex_str = r".+P4PORT=(\S+)\\n.+P4USER=(\S+)\\n.+P4CLIENT=(\S+)'.+"
    _server, _user, _client = re.match(regex_str, str(_data)).group(1, 2, 3)
    return _server, _user, _client


def read_perforce_users_list():
    pass


def is_blank(_string):
    if _string and _string.strip():
        return False
    return True


def binary_to_string(string_data):
    if isinstance(string_data, bytes):
        return string_data.decode("ascii")
    return string_data


def run_command(_command):
    curr_workspace = subprocess.Popen(binary_to_string(_command), stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
    out, err = curr_workspace.communicate()
    return binary_to_string(out), binary_to_string(err)


def fix_path(_path):
    return os.path.abspath(_path)


class Struct(object):
    def __init__(self, adict):
        """Convert a dictionary to a class

        @param :adict Dictionary
        """
        self.__dict__.update(adict)
        for k, v in adict.items():
            if isinstance(v, dict):
                self.__dict__[k] = Struct(v)


def get_object(adict):
    """Convert a dictionary to a class
    @param :adict Dictionary
    @return :class:Struct
    """
    return Struct(adict)


def get_dict(astruct):
    return False


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def get_windows_display_name():

    try:
        import win32api
        import win32net

        user_info = win32net.NetUserGetInfo(win32net.NetGetAnyDCName(), win32api.GetUserName(), 2)
        full_name = user_info["full_name"]
        return full_name
    except:
        import subprocess
        name = subprocess.check_output('net user "%USERNAME%" | FIND /I "Full Name"', shell=True)
        full_name = name.replace(b"Full Name", b"").strip()
        return full_name.decode("ascii")


class Perforce(metaclass=Singleton):

    p4_logger = logging.getLogger(__name__ + ".Perforce")

    def __init__(self, server_address="", username="", client_name="", password=""):
        self.user = username
        self.server_address = server_address
        self.password = password
        self.client_name = client_name
        self.p4_logger.debug("P4USER={} P4PORT={} P4CLIENT={}".format(self.user, self.server_address, self.client_name))

    def login(self):
        pass

    def checkout(self, files):
        pass

    def revert(self, files):
        pass

    def where(self, files, local=True, depot=False):
        pass

    def submit(self, files):
        pass

