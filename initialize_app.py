# this is the script that is run.


import os
import sys
from bin import ui_module
from PyQt5 import QtWidgets, QtCore
import database_manager
import UIDGenerator
import utility
import config
from functools import partial
from validations import project_validations
import logging

project_logger = logging.getLogger(__name__)


class ProjectTool(ui_module.UI):
    def __init__(self):
        ui_module.UI.__init__(self)

        self.radio_initialized = False
        self.project_radios = {}
        self._load_prerequisite()
        UIDGenerator.GUID()
        database_manager.DB()
        self._connect_ui()
        self.load_project_radios()
        self.update_file_validation_status()

    def _load_prerequisite(self):
        if os.path.exists(config.perforce_data_file):
            self.app_core_widget.setVisible(True)
            self.perforce_menu_widget.setVisible(False)
            # read the file and start up perforce
            _s, _u, _c = utility.read_from_perforce_config()
            self.p4 = utility.Perforce(_s, _u, _c)
            # tool will continue after load.
            # return perforce class
            pass
        else:
            # show perforce UI
            self.app_core_widget.setVisible(False)
            self.perforce_menu_widget.setVisible(True)
            # have user fill it up, and store the data to file, then run this function again.

    def _connect_ui(self):
        self.tab_upload_validation_button.clicked.connect(self.run_file_validation)
        self.tab_upload_upload_button.clicked.connect(self.upload_files)
        self.tab_widget_main.currentChanged.connect(self.update_current_tab)
        self.ui_but_refresh_UI.clicked.connect(self.reload_files)
        self.ui_perforce_config_browse.clicked.connect(self.update_perforce_config_field)
        self.perforce_apply_button.clicked.connect(self.perforce_configuration_worker)
        self.reset_p4_informaton.clicked.connect(self.clear_perforce_info)

    def perforce_configuration_worker(self):

        if utility.is_blank(self.ui_lineedit_perforce_config.text()):
            if utility.is_blank(self.ui_perforce_server_address.text()) \
                    or utility.is_blank(self.ui_perforce_user_name.text()) \
                    or utility.is_blank(self.ui_perforce_workspace_name.text()):
                self.create_message_window(
                    _err_message="Please add details about the Perforce server or browse to p4config file.",
                    _err_title="Perforce Config Error")
                return
            else:
                utility.write_to_perforce_config(
                    self.ui_perforce_server_address.text(),
                    self.ui_perforce_user_name.text(),
                    self.ui_perforce_workspace_name.text())
        else:
            if os.path.isfile(self.ui_lineedit_perforce_config.text()):
                if utility.read_p4config(self.ui_lineedit_perforce_config.text()):
                    self._load_prerequisite()
                else:
                    self.create_message_window(
                        _err_message="Please provide correct p4config file, If you are not sure, please reach out to TA",
                        _err_title="Perforce Config Error")
            else:
                self.create_message_window(
                    _err_message="Please add details about the Perforce server or browse to p4config file.",
                    _err_title="Perforce Config Error")

    def reload_files(self):
        UIDGenerator.GUID().reload_guid_file()
        database_manager.DB().reload_database()
        self.update_current_tab()

    def load_file_types_for_radio(self):
        _filters = []
        _radio = self.get_selected_project_radio()
        for _p_key, _p_value in config.projects.items():
            for i in _p_value['accepted_file_types']:
                if _p_key.lower() == _radio.name.lower():
                    _filters.append('*.' + str(i))
        if self.radio_initialized:
            self.tab_upload_browse_button.clicked.disconnect()
        self.tab_upload_browse_button.clicked.connect(partial(self.update_upload_file_path, _filters))
        self.radio_initialized = True

    def load_project_radios(self):
        for i in config.labels:
            self.project_radios[i] = []

        for _p_key, _p_value in config.projects.items():
            for each_tab in config.labels:
                radio_button = ui_module.RadioButton(_p_key.title())
                radio_button.clicked.connect(partial(self.enable_radio, radio_button))
                eval("self.tab_{}_project_radio_layout.addWidget(radio_button)".format(each_tab))
                self.project_radios[each_tab].append(radio_button)
                radio_button.setChecked(True)
        self.load_file_types_for_radio()
        self.ui_adjustments()

    def ui_adjustments(self):
        self.tab_upload_project_radio_layout.addSpacerItem(QtWidgets.QSpacerItem(250, 10))
        self.tab_reviewer_project_radio_layout.addSpacerItem(QtWidgets.QSpacerItem(250, 10))
        self.tab_user_based_project_radio_layout.addSpacerItem(QtWidgets.QSpacerItem(250, 10))
        self.tab_submissions_project_radio_layout.addSpacerItem(QtWidgets.QSpacerItem(250, 10))

    def enable_radio(self, radio_obj):
        radio_obj.setChecked(True)
        if self.tab_widget_main.currentIndex() == 0:
            self.load_file_types_for_radio()
        else:
            self.update_current_tab()

    def get_selected_project_radio(self):
        for _r in self.project_radios[config.tab_names[self.tab_widget_main.currentIndex()]]:
            if _r.isChecked():
                return _r

    def update_current_tab(self):
        if self.tab_widget_main.currentIndex() > 0:
            self.populate_table_information(config.tab_names[self.tab_widget_main.currentIndex()])

    def populate_table_information(self, tab_name):
        eval("self.tab_{}_table.clear()".format(tab_name))
        eval("self.tab_{}_table.setRowCount(0)".format(tab_name))
        eval("self.tab_{}_table.setColumnCount(0)".format(tab_name))

        _radio_setting = self.get_selected_project_radio().name.lower()
        _reduction_counter = 0
        _reduction_radio_counter = 0

        for _index, v in enumerate(database_manager.DB().db_data.values()):
            if tab_name != "dashboard":
                if _radio_setting != v["project_type"].lower():
                    _reduction_radio_counter += 1
                    continue
                else:
                    if tab_name != "submissions":
                        if v["status"] == "Rejected" or v["status"] == "Approved":
                            _reduction_radio_counter += 1
                            continue
                    _index = _index - _reduction_radio_counter

            if tab_name == "submissions":
                if v["status"] != "Approved":
                    _reduction_counter += 1
                    continue
                else:
                    _index = _index - _reduction_counter
                    _reduction_counter = 0
            eval("self.tab_{}_table.insertRow(int(_index))".format(tab_name))
            create_columns = True
            if eval("self.tab_{0}_table.columnCount() >= len(config.{0}_columns)".format(tab_name)):
                create_columns = False
            for _iter, column_name in enumerate(eval("config.{}_columns".format(tab_name))):
                if create_columns:
                    eval("self.tab_{}_table.insertColumn(_iter)".format(tab_name))
                _item = QtWidgets.QTableWidgetItem(str(v[column_name]))
                _item.setTextAlignment(QtCore.Qt.AlignHCenter)  # change the alignment
                eval("self.tab_{}_table.setItem(int(_index), int(_iter), _item)".format(tab_name))

            if tab_name == "reviewer":
                download_files_button = ui_module.AdvancedButton("Download", v["guid"])
                approve_button = ui_module.AdvancedButton("Approved", v["guid"])
                reject_button = ui_module.AdvancedButton("Rejected", v["guid"])
                approve_button.clicked.connect(partial(self.validation_status, approve_button.status,
                                                       approve_button.guid))
                reject_button.clicked.connect(partial(self.validation_status, reject_button.status, reject_button.guid))
                download_files_button.clicked.connect(partial(self.download_files, download_files_button.guid))

                for _i, but in enumerate([download_files_button, approve_button, reject_button],
                                         start=len(eval("config.{}_columns".format(tab_name)))):
                    if create_columns:
                        eval("self.tab_{}_table.insertColumn(_i)".format(tab_name))
                    eval("self.tab_{}_table.setCellWidget(int(_index), _i, but)".format(tab_name))

            if tab_name == "submissions":
                submit_button = ui_module.AdvancedButton("Submit", v["guid"])
                submit_button.clicked.connect(partial(self.submit_files, submit_button.guid))
                if create_columns:
                    eval("self.tab_{0}_table.insertColumn(len(config.{0}_columns))".format(tab_name))
                eval("self.tab_{0}_table.setCellWidget(int(_index), len(config.{0}_columns), submit_button)".format(tab_name))
        eval("self.tab_{0}_table.setHorizontalHeaderLabels(config.{0}_header_labels)".format(tab_name))
        eval("self.tab_{}_table.resizeColumnsToContents()".format(tab_name))
        # _header_view = eval("self.tab_{}_table.horizontalHeader()".format(tab_name))
        # _header_view.setSectionResizeMode(_header_view.Stretch)

    def test_func(self, status="default", _v=0):
        print("Test Function executed.", status, _v)

    def submit_files(self, _guid):
        print("File Ready for Submission! -> Details : ", _guid)

    def validation_status(self, status, _guid):
        _data = database_manager.DB().db_data[str(_guid)]
        _data["status"] = status
        _data["reviewer_name"] = utility.get_windows_display_name()
        database_manager.DB().write_to_disk()
        self.update_current_tab()

    def run_file_validation(self, reset=False):
        if reset:
            self.update_file_validation_status()
            self.tab_upload_upload_button.setEnabled(False)
            self.tab_upload_browse_file_field.setText("")
            return
        _file_path = self.tab_upload_browse_file_field.text()

        if not utility.is_blank(_file_path) and os.path.isfile(_file_path) and os.path.exists(_file_path):
            project_logger.debug("Running Validation Checks. Please wait...")
            if project_validations.run_project_validations():
                self.update_file_validation_status("passed")
                self.tab_upload_upload_button.setEnabled(True)
            else:
                self.update_file_validation_status("failed")
                self.tab_upload_upload_button.setEnabled(False)

        else:
            self.create_message_window("Please select files for upload", "Error")

    def upload_files(self):
        _file_path = self.tab_upload_browse_file_field.text()
        if os.path.isfile(_file_path) and os.path.exists(_file_path):
            database_manager.DB().add_to_db(_file_path, self.get_selected_project_radio().name,
                                            self.tab_upload_validation_status.text())
            curr_file_name = os.path.basename(_file_path)
            utility.copy_files_to_server(_file_path, os.path.join(
                config.projects[self.get_selected_project_radio().name.lower()]["folder_path"], curr_file_name))
            self.run_file_validation(reset=True)
            self.create_message_window(
                "File has been uploaded for review, Please check the dashboard tab for updates.", "Upload Info")
        else:
            self.create_message_window("Please select files for upload", "Error")

    def download_files(self, _guid):
        print("Download requested for : ", _guid)
        print("---> {}".format(database_manager.DB().db_data[str(_guid)]))

    def update_upload_file_path(self, custom_filters):
        file_dir = self.browse_file_directory(custom_filters)
        self.tab_upload_browse_file_field.setText(file_dir)

    def update_perforce_config_field(self):
        file_dir = self.browse_file_directory()
        self.ui_lineedit_perforce_config.setText(file_dir)

    def clear_perforce_info(self):
        os.remove(config.perforce_data_file)
        self._load_prerequisite()


app = QtWidgets.QApplication(sys.argv)
ex = ProjectTool()
ex.show()
sys.exit(app.exec_())
