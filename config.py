
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
import sys
from pathlib import Path
sys.path.append(current_directory)

name = "Project Manager"
version = "0.1"
__guid_file = r"resources\project_data.guid"
__database_file = r"resources\project_data.db"
__semaphore_guid = __guid_file.replace("guid", "guid.locked")
__semaphore_database = __database_file.replace("db", "db.locked")

guid_file = os.path.join(current_directory, __guid_file)
database_file = os.path.join(current_directory, __database_file)
perforce_data_file = os.path.join(os.environ["APPDATA"], "project_tool.p4data")

projects = {
    "body": {
        "folder_path": r"G:\upload\body_files",
        "accepted_file_types": ["ani", "txt"]
    },

    "face": {
        "folder_path": r"G:\upload\face_files",
        "accepted_file_types": ["mov", "txt"]
    },

}

tab_names = {
    0: "upload",
    1: "reviewer",
    2: "user_based",
    3: "submissions",
    4: "dashboard"
}


if not os.path.exists(os.path.dirname(guid_file)):
    Path(os.path.dirname(guid_file)).mkdir(parents=True, exist_ok=True)


# style sheets
pending_status_color = "QLabel { color : orange }"
failed_status_color = "QLabel { color : red }"
passed_status_color = "QLabel { color : green }"

column_data = {
        "file_name": "File Name",
        "perforce_file_path": "P4 Path",
        "perforce_user_name": "P4 User Name",
        "perforce_client_name": "P4 Workspace",
        "status": "File Status",
        "validation": "Validation Status",
        "reviewer_name": "Reviewer Name",
        "display_name": "User",
        "project_type": "Project",
        "guid": "GUID"
}

reviewer_columns = ["file_name", "perforce_file_path", "validation", "display_name", "perforce_user_name"]
user_based_columns = ["file_name", "perforce_user_name", "validation", "display_name"]
submissions_columns = ["file_name", "perforce_file_path", "perforce_user_name", "display_name", "validation", "status"]
dashboard_columns = ["file_name", "perforce_file_path", "perforce_user_name", "display_name", "perforce_client_name", "validation", "status",
                     "reviewer_name", "project_type"]


reviewer_header_labels = []
user_based_header_labels = []
submissions_header_labels = []
dashboard_header_labels = []

labels = ["upload", "reviewer", "user_based", "submissions", "dashboard"]

for l in labels:
    if not l == "upload":
        for d in eval("{}_columns".format(l)):
            eval("{}_header_labels.append(column_data[d])".format(l))
