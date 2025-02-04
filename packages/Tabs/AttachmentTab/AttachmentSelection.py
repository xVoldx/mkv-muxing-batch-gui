from PySide2.QtCore import Signal
from PySide2.QtWidgets import QVBoxLayout, QGroupBox

from packages.Tabs.AttachmentTab.Widgets.AttachmentSourceButton import AttachmentSourceButton
from packages.Tabs.AttachmentTab.Widgets.AttachmentSourceLineEdit import AttachmentSourceLineEdit
from packages.Tabs.AttachmentTab.Widgets.AttachmentTable import AttachmentTable
from packages.Tabs.AttachmentTab.Widgets.AttachmentsTotalSizeValueLabel import AttachmentsTotalSizeValueLabel
from packages.Tabs.AttachmentTab.Widgets.DiscardOldAttachmentsCheckBox import DiscardOldAttachmentsCheckBox
from packages.Tabs.GlobalSetting import *
from packages.Tabs.GlobalSetting import sort_names_like_windows, get_readable_filesize, get_files_names_absolute_list, \
    get_file_name_absolute_path
from packages.Widgets.InvalidPathDialog import *


# noinspection PyAttributeOutsideInit
def get_files_size_list(files_list, folder_path):
    files_size_list = []
    for i in range(len(files_list)):
        file_name_absolute = get_file_name_absolute_path(file_name=files_list[i], folder_path=folder_path)
        file_size_bytes = os.path.getsize(file_name_absolute)
        files_size_list.append(get_readable_filesize(size_bytes=file_size_bytes))
    return files_size_list


class AttachmentSelectionSetting(GlobalSetting):
    tab_clicked_signal = Signal()
    activation_signal = Signal(bool)

    def __init__(self):
        super().__init__()
        self.attachment_source_label = QLabel("Attachment Source Folder:")
        self.attachment_total_size_label = QLabel("Total Attachment Size:")
        self.attachment_total_size_value_label = AttachmentsTotalSizeValueLabel()
        self.attachment_source_lineEdit = AttachmentSourceLineEdit()
        self.attachment_source_button = AttachmentSourceButton()
        self.discard_old_attachments_checkBox = DiscardOldAttachmentsCheckBox()
        self.table = AttachmentTable()
        self.MainLayout = QVBoxLayout()
        self.attachment_main_groupBox = QGroupBox(self)
        self.attachment_main_layout = QGridLayout()
        self.folder_path = ""
        self.files_names_list = []
        self.files_checked_list = []
        self.files_names_absolute_list = []
        self.files_size_list = []
        self.setup_layouts()
        self.connect_signals()

    def setup_layouts(self):
        self.setup_main_layout()
        self.setup_attachment_main_groupBox()
        self.MainLayout.addWidget(self.attachment_main_groupBox)
        self.setLayout(self.MainLayout)

    def setup_attachment_main_groupBox(self):
        self.attachment_main_groupBox.setTitle("Attachments")
        self.attachment_main_groupBox.setCheckable(True)
        self.attachment_main_groupBox.setChecked(False)
        self.attachment_main_groupBox.setLayout(self.attachment_main_layout)

    def update_folder_path(self, new_path: str):
        if new_path != "":
            self.attachment_source_lineEdit.setText(new_path)
            self.update_files_lists(new_path)

            self.update_total_size()
            self.show_files_list()

    def update_total_size(self):
        self.attachment_total_size_value_label.update_total_size(self.files_names_absolute_list)

    def update_files_lists(self, folder_path):
        if folder_path == "" or folder_path.isspace():
            self.folder_path = ""
            self.attachment_source_lineEdit.setText("")
            return
        try:
            self.folder_path = folder_path
            self.files_names_list = self.get_files_list(self.folder_path)
            self.files_names_absolute_list = get_files_names_absolute_list(self.files_names_list, self.folder_path)
            self.files_size_list = get_files_size_list(files_list=self.files_names_list, folder_path=self.folder_path)
        except Exception as e:
            invalid_path_dialog = InvalidPathDialog()
            invalid_path_dialog.execute()

    def get_files_list(self, folder_path):
        temp_files_names = sort_names_like_windows(names_list=os.listdir(folder_path))
        temp_files_names_absolute = get_files_names_absolute_list(temp_files_names, folder_path)
        result = []
        for i in range(len(temp_files_names)):
            if os.path.isdir(temp_files_names_absolute[i]):
                continue
            if os.path.getsize(temp_files_names_absolute[i]) == 0:
                continue
            result.append(temp_files_names[i])
        return result

    def show_files_list(self):
        self.table.show_files_list(files_names_list=self.files_names_list, files_size_list=self.files_size_list)
        self.update_other_classes_variables()

    def update_other_classes_variables(self):
        self.change_global_last_path_directory()
        self.change_global_attachment_list()
        self.attachment_source_lineEdit.set_current_folder_path(self.folder_path)

    def setup_main_layout(self):
        self.attachment_main_layout.addWidget(self.attachment_source_label, 0, 0)
        self.attachment_main_layout.addWidget(self.attachment_source_lineEdit, 0, 1, 1, 80)
        self.attachment_main_layout.addWidget(self.attachment_source_button, 0, 81, 1, 1)
        self.attachment_main_layout.addWidget(self.attachment_total_size_label, 1, 0)
        self.attachment_main_layout.addWidget(self.attachment_total_size_value_label, 1, 1)
        self.attachment_main_layout.addWidget(self.discard_old_attachments_checkBox, 1, 40, 1, -1,
                                              alignment=Qt.AlignRight)
        self.attachment_main_layout.addWidget(self.table, 2, 0, 1, -1)

    def change_global_last_path_directory(self):
        if self.folder_path != "" and not self.folder_path.isspace():
            GlobalSetting.LAST_DIRECTORY_PATH = self.folder_path

    def change_global_attachment_list(self):
        GlobalSetting.ATTACHMENT_FILES_LIST = self.files_names_list
        GlobalSetting.ATTACHMENT_FILES_ABSOLUTE_PATH_LIST = self.files_names_absolute_list
        GlobalSetting.ATTACHMENT_FILES_CHECKING_LIST = [True] * len(self.files_names_list)

    def connect_signals(self):
        self.attachment_source_button.clicked_signal.connect(self.update_folder_path)
        self.attachment_source_lineEdit.edit_finished_signal.connect(self.update_folder_path)
        self.attachment_main_groupBox.toggled.connect(self.activate_tab)
        self.tab_clicked_signal.connect(self.tab_clicked)
        self.table.update_checked_attachment_signal.connect(self.attachment_total_size_value_label.attachment_checked)
        self.table.update_unchecked_attachment_signal.connect(
            self.attachment_total_size_value_label.attachment_unchecked)

    def tab_clicked(self):
        if not GlobalSetting.JOB_QUEUE_EMPTY:
            self.disable_editable_widgets()
        else:
            self.enable_editable_widgets()

    def disable_editable_widgets(self):
        self.attachment_source_lineEdit.setEnabled(False)
        self.attachment_source_button.setEnabled(False)
        self.discard_old_attachments_checkBox.setEnabled(False)
        self.attachment_main_groupBox.setCheckable(False)

    def enable_editable_widgets(self):
        self.attachment_source_lineEdit.setEnabled(True)
        self.attachment_source_button.setEnabled(True)
        self.discard_old_attachments_checkBox.setEnabled(True)
        if GlobalSetting.ATTACHMENT_ENABLED:
            self.attachment_main_groupBox.setCheckable(True)
        else:
            self.attachment_main_groupBox.setCheckable(True)
            GlobalSetting.ATTACHMENT_ENABLED = False
            self.attachment_main_groupBox.setChecked(GlobalSetting.ATTACHMENT_ENABLED)

    def activate_tab(self, on):
        if not on:
            self.table.clear_table()
            self.attachment_source_lineEdit.setText("")
            self.attachment_total_size_value_label.set_total_size_zero()
            self.discard_old_attachments_checkBox.setChecked(False)
            self.folder_path = ""
            self.files_names_list = []
            self.files_names_absolute_list = []
            self.files_size_list = []
            GlobalSetting.ATTACHMENT_FILES_LIST = []
            GlobalSetting.ATTACHMENT_FILES_ABSOLUTE_PATH_LIST = []
            GlobalSetting.ATTACHMENT_FILES_CHECKING_LIST = []
            GlobalSetting.ATTACHMENT_DISCARD_OLD = False
        self.activation_signal.emit(on)
        GlobalSetting.ATTACHMENT_ENABLED = on
