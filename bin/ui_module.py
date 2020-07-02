import os
import sys

from Python.ProjectManager import config
from PyQt5 import QtWidgets, QtCore, QtGui


class UI(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.tab_upload_validation_status = None
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("{}({})".format(config.name, config.version))
        self.setFixedSize(1000, 600)

        self.central_wid = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_wid)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.central_wid.setLayout(self.main_layout)

        self.app_core_widget = QtWidgets.QWidget(self)
        self.app_core_layout = QtWidgets.QVBoxLayout(self)
        self.app_core_widget.setLayout(self.app_core_layout)
        self.main_layout.addWidget(self.app_core_widget)

        self.perforce_menu_widget = QtWidgets.QWidget(self)
        self.perforce_configuration_layout = QtWidgets.QVBoxLayout(self)
        self.perforce_menu_widget.setLayout(self.perforce_configuration_layout)
        self.main_layout.addWidget(self.perforce_menu_widget)

        # Perforce configuration UI

        layout_p4_hor1 = QtWidgets.QHBoxLayout(self)
        p4_server_address_label = QtWidgets.QLabel("Perforce Server Address    :  ")
        self.ui_perforce_server_address = QtWidgets.QLineEdit(self)
        layout_p4_hor1.addSpacerItem(QtWidgets.QSpacerItem(250, 10))
        layout_p4_hor1.addWidget(p4_server_address_label)
        layout_p4_hor1.addWidget(self.ui_perforce_server_address)
        layout_p4_hor1.addSpacerItem(QtWidgets.QSpacerItem(250, 10))

        layout_p4_hor2 = QtWidgets.QHBoxLayout(self)
        p4_username_label = QtWidgets.QLabel("Perforce Username             : ")
        self.ui_perforce_user_name = QtWidgets.QLineEdit(self)
        layout_p4_hor2.addSpacerItem(QtWidgets.QSpacerItem(250, 10))
        layout_p4_hor2.addWidget(p4_username_label)
        layout_p4_hor2.addWidget(self.ui_perforce_user_name)
        layout_p4_hor2.addSpacerItem(QtWidgets.QSpacerItem(250, 10))

        layout_p4_hor3 = QtWidgets.QHBoxLayout(self)
        p4_client_label = QtWidgets.QLabel("Perforce Workspace Name : ")
        self.ui_perforce_workspace_name = QtWidgets.QLineEdit(self)
        layout_p4_hor3.addSpacerItem(QtWidgets.QSpacerItem(250, 10))
        layout_p4_hor3.addWidget(p4_client_label)
        layout_p4_hor3.addWidget(self.ui_perforce_workspace_name)
        layout_p4_hor3.addSpacerItem(QtWidgets.QSpacerItem(250, 10))

        layout_p4_hor4 = QtWidgets.QHBoxLayout(self)
        p4_config_label = QtWidgets.QLabel("Load From .P4Config          :")
        self.ui_lineedit_perforce_config = QtWidgets.QLineEdit(self)
        self.ui_lineedit_perforce_config.setEnabled(False)
        self.ui_perforce_config_browse = QtWidgets.QPushButton("...", self)
        layout_p4_hor4.addSpacerItem(QtWidgets.QSpacerItem(250, 10))
        layout_p4_hor4.addWidget(p4_config_label)
        layout_p4_hor4.addSpacerItem(QtWidgets.QSpacerItem(5, 10))
        layout_p4_hor4.addWidget(self.ui_lineedit_perforce_config)
        layout_p4_hor4.addWidget(self.ui_perforce_config_browse)
        layout_p4_hor4.addSpacerItem(QtWidgets.QSpacerItem(170, 10))

        layout_p4_hor5 = QtWidgets.QHBoxLayout(self)
        layout_p4_hor5.addSpacerItem(QtWidgets.QSpacerItem(400, 10))
        layout_p4_hor5.addWidget(QtWidgets.QLabel("---------------- OR ---------------"))

        layout_apply_hor6 = QtWidgets.QHBoxLayout(self)
        self.perforce_apply_button = QtWidgets.QPushButton("Apply Perforce Settings")
        self.perforce_apply_button.setFixedHeight(60)
        layout_apply_hor6.addSpacerItem(QtWidgets.QSpacerItem(300, 10))
        layout_apply_hor6.addWidget(self.perforce_apply_button)
        layout_apply_hor6.addSpacerItem(QtWidgets.QSpacerItem(300, 10))

        self.perforce_configuration_layout.addSpacerItem(QtWidgets.QSpacerItem(10, 200))
        self.perforce_configuration_layout.addLayout(layout_p4_hor1)
        self.perforce_configuration_layout.addLayout(layout_p4_hor2)
        self.perforce_configuration_layout.addLayout(layout_p4_hor3)
        self.perforce_configuration_layout.addLayout(layout_p4_hor5)
        self.perforce_configuration_layout.addLayout(layout_p4_hor4)
        self.perforce_configuration_layout.addLayout(layout_apply_hor6)
        self.perforce_configuration_layout.addSpacerItem(QtWidgets.QSpacerItem(10, 450))

        # reset p4 information
        self.reset_p4_informaton = QtWidgets.QPushButton("Reset Perforce Information")
        # add refresh button
        self.ui_but_refresh_UI = QtWidgets.QPushButton("Refresh UI")
        horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.app_core_layout.addLayout(horizontal_layout)
        horizontal_layout.addWidget(self.reset_p4_informaton)
        horizontal_layout.addWidget(self.ui_but_refresh_UI)

        # tab widget
        self.tab_widget_main = QtWidgets.QTabWidget(self)
        self.app_core_layout.addWidget(self.tab_widget_main)

        # customize tab widget
        self.tab_widget_main.setTabPosition(self.tab_widget_main.South)

        # --
        # upload tab
        self.tab_upload = QtWidgets.QWidget(self)
        self.tab_widget_main.addTab(self.tab_upload, "Upload")
        self.tab_upload_main_layout = QtWidgets.QVBoxLayout(self)
        tab_upload_hor_layout_browse_area = QtWidgets.QHBoxLayout(self)
        self.tab_upload.setLayout(self.tab_upload_main_layout)
        self.tab_upload_validation_status = None
        tab_upload_hor_layout_user_upload_label = QtWidgets.QHBoxLayout(self)
        tab_upload_header_label = QtWidgets.QLabel("Upload for Review")
        _font = QtGui.QFont("Times", 15, QtGui.QFont.Bold)
        tab_upload_header_label.setFont(_font)
        tab_upload_hor_layout_user_upload_label.addWidget(tab_upload_header_label, alignment=QtCore.Qt.AlignHCenter)
        tab_upload_label = QtWidgets.QLabel("File Path :    ")
        self.tab_upload_browse_file_field = QtWidgets.QLineEdit(self)
        self.tab_upload_browse_file_field.setEnabled(False)
        self.tab_upload_browse_button = QtWidgets.QPushButton("Browse", self)
        tab_upload_hor_layout_browse_area.addWidget(tab_upload_label)
        tab_upload_hor_layout_browse_area.addWidget(self.tab_upload_browse_file_field)
        tab_upload_hor_layout_browse_area.addWidget(self.tab_upload_browse_button)
        tab_upload_video_details_layout = QtWidgets.QHBoxLayout(self)
        tab_video_label = QtWidgets.QLabel("Video Path : ")
        self.tab_upload_browse_video_field = QtWidgets.QLineEdit(self)
        self.tab_upload_browse_video_field.setEnabled(False)
        self.tab_upload_browse_video_button = QtWidgets.QPushButton("Browse", self)
        self.tab_upload_browse_video_button.setEnabled(False)
        tab_upload_video_details_layout.addWidget(tab_video_label)
        tab_upload_video_details_layout.addWidget(self.tab_upload_browse_video_field)
        tab_upload_video_details_layout.addWidget(self.tab_upload_browse_video_button)
        tab_upload_label2 = QtWidgets.QLabel("Project : ")
        self.tab_upload_project_radio_layout = QtWidgets.QHBoxLayout(self)
        self.tab_upload_project_radio_layout.addSpacerItem(QtWidgets.QSpacerItem(250, 10))
        self.tab_upload_project_radio_layout.addWidget(tab_upload_label2)
        tab_upload_hor_layout_validation_area = QtWidgets.QHBoxLayout(self)
        tab_upload_ver_layout1 = QtWidgets.QVBoxLayout(self)
        tab_upload_hor_layout_local1 = QtWidgets.QHBoxLayout(self)
        self.tab_upload_validation_layout = QtWidgets.QHBoxLayout(self)
        tab_upload_label3 = QtWidgets.QLabel("Validations Status : ")
        self.tab_upload_validation_status = QtWidgets.QLabel("")
        self.tab_upload_validation_button = QtWidgets.QPushButton("Run Validation Check(s)", self)
        tab_upload_hor_layout_local1.addSpacerItem(QtWidgets.QSpacerItem(200, 10))
        tab_upload_hor_layout_local1.addWidget(self.tab_upload_validation_button)
        tab_upload_hor_layout_local1.addSpacerItem(QtWidgets.QSpacerItem(200, 10))
        self.tab_upload_validation_layout.addSpacerItem(QtWidgets.QSpacerItem(200, 10))
        self.tab_upload_validation_layout.addWidget(tab_upload_label3)
        self.tab_upload_validation_layout.addWidget(self.tab_upload_validation_status)
        self.tab_upload_validation_layout.addSpacerItem(QtWidgets.QSpacerItem(300, 10))
        tab_upload_ver_layout1.addLayout(tab_upload_hor_layout_local1)
        tab_upload_ver_layout1.addLayout(self.tab_upload_validation_layout)
        tab_upload_hor_layout_validation_area.addLayout(tab_upload_ver_layout1)
        tab_upload_hor_layout_upload_button_area = QtWidgets.QHBoxLayout(self)
        self.tab_upload_upload_button = QtWidgets.QPushButton("Upload File", self)
        self.tab_upload_upload_button.setEnabled(False)
        self.tab_upload_upload_button.setFixedHeight(50)
        tab_upload_hor_layout_upload_button_area.addSpacerItem(QtWidgets.QSpacerItem(150, 10))
        tab_upload_hor_layout_upload_button_area.addWidget(self.tab_upload_upload_button)
        tab_upload_hor_layout_upload_button_area.addSpacerItem(QtWidgets.QSpacerItem(150, 10))
        # layout for - upload
        self.tab_upload_main_layout.addLayout(tab_upload_hor_layout_user_upload_label)
        self.tab_upload_main_layout.addLayout(self.tab_upload_project_radio_layout)
        self.tab_upload_main_layout.addLayout(tab_upload_hor_layout_browse_area)
        self.tab_upload_main_layout.addLayout(tab_upload_video_details_layout)
        self.tab_upload_main_layout.addLayout(tab_upload_hor_layout_validation_area)
        self.tab_upload_main_layout.addLayout(tab_upload_hor_layout_upload_button_area)
        self.tab_upload_main_layout.addSpacerItem(QtWidgets.QSpacerItem(10, 400))

        # --
        # reviewer tab
        self.tab_reviewer = QtWidgets.QWidget(self)
        self.tab_widget_main.addTab(self.tab_reviewer, "Reviewer")
        self.tab_reviewer_main_layout = QtWidgets.QVBoxLayout(self)
        self.tab_reviewer.setLayout(self.tab_reviewer_main_layout)
        self.tab_reviewer_project_radio_layout = QtWidgets.QHBoxLayout(self)
        tab_reviewer_table_layout = QtWidgets.QHBoxLayout(self)
        self.tab_reviewer_main_layout.addLayout(self.tab_reviewer_project_radio_layout)
        self.tab_reviewer_main_layout.addLayout(tab_reviewer_table_layout)

        # radio buttons
        tab_reviewer_label1 = QtWidgets.QLabel("Project : ", self)
        self.tab_reviewer_project_radio_layout.addSpacerItem(QtWidgets.QSpacerItem(250, 10))
        self.tab_reviewer_project_radio_layout.addWidget(tab_reviewer_label1)
        # table layout
        self.tab_reviewer_table = QtWidgets.QTableWidget(self)
        tab_reviewer_table_layout.addWidget(self.tab_reviewer_table)


        # --
        # user based tab
        self.tab_user_based = QtWidgets.QWidget(self)
        self.tab_widget_main.addTab(self.tab_user_based, "User Based")
        self.tab_user_based_main_layout = QtWidgets.QVBoxLayout(self)
        self.tab_user_based.setLayout(self.tab_user_based_main_layout)
        self.tab_widget_main.setTabVisible(2, False)
        self.tab_user_based_project_radio_layout = QtWidgets.QHBoxLayout(self)
        self.tab_user_based_project_radio_layout.addSpacerItem(QtWidgets.QSpacerItem(250, 10))
        tab_user_based_label_project = QtWidgets.QLabel("Project : ", self)
        self.tab_user_based_project_radio_layout.addWidget(tab_user_based_label_project)
        self.tab_user_based_main_layout.addLayout(self.tab_user_based_project_radio_layout)

        # --
        # submission tab
        self.tab_submissions = QtWidgets.QWidget(self)
        self.tab_widget_main.addTab(self.tab_submissions, "Submissions")
        self.tab_submissions_main_layout = QtWidgets.QVBoxLayout(self)
        self.tab_submissions.setLayout(self.tab_submissions_main_layout)
        self.tab_submissions_project_radio_layout = QtWidgets.QHBoxLayout(self)
        self.tab_submissions_project_radio_layout.addSpacerItem(QtWidgets.QSpacerItem(250, 10))
        tab_submissions_table_layout = QtWidgets.QHBoxLayout(self)
        self.tab_submissions_main_layout.addLayout(self.tab_submissions_project_radio_layout)
        self.tab_submissions_main_layout.addLayout(tab_submissions_table_layout)
        tab_submission_label_project = QtWidgets.QLabel("Project : ", self)
        self.tab_submissions_project_radio_layout.addWidget(tab_submission_label_project)

        # table layout
        self.tab_submissions_table = QtWidgets.QTableWidget(self)
        tab_submissions_table_layout.addWidget(self.tab_submissions_table)

        # --
        # dashboard tab
        self.tab_dashboard = QtWidgets.QWidget(self)
        self.tab_widget_main.addTab(self.tab_dashboard, "Dashboard")
        tab_dashboard_table_layout = QtWidgets.QHBoxLayout(self)
        self.tab_dashboard.setLayout(tab_dashboard_table_layout)
        self.tab_dashboard_project_radio_layout = QtWidgets.QHBoxLayout(self)
        self.tab_dashboard_project_radio_layout.addSpacerItem(QtWidgets.QSpacerItem(250, 10))

        # table layout
        self.tab_dashboard_table = QtWidgets.QTableWidget(self)
        tab_dashboard_table_layout.addWidget(self.tab_dashboard_table)

    def browse_file_directory(self, _file_filters="*.*"):
        file_dir = self.create_window_in_qt(_file_filters)
        if os.path.isfile(file_dir):
            return file_dir

    def create_window_in_qt(self, _f):
        _f = " ".join(_f)
        asset_file = QtWidgets.QFileDialog.getOpenFileName(self, caption='Browse File', filter="Files ({})".format(_f))
        asset_file = str(asset_file[0])
        return asset_file

    def create_message_window(self, _err_message, _err_title):
        ErrorMessageUI(_err_title, _err_message)

    def update_file_validation_status(self, status="pending"):
        self.tab_upload_validation_status.setText(status)
        eval("self.tab_upload_validation_status.setStyleSheet(config.{}_status_color)".format(status))


class ErrorMessageUI(QtWidgets.QWidget):
    def __init__(self, title = "default", message = "Sample Message"):
        QtWidgets.QWidget.__init__(self)
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)

        _res = msg_box.exec_()


class AdvancedButton(QtWidgets.QPushButton):
    def __init__(self, button_name, guid):
        QtWidgets.QPushButton.__init__(self, button_name)
        self.status = button_name
        self.guid = guid


class RadioButton(QtWidgets.QRadioButton):
    def __init__(self, button_name):
        QtWidgets.QRadioButton.__init__(self, button_name)
        self.name = button_name
