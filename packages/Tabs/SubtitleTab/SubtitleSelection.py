from PySide2.QtCore import Signal
from PySide2.QtWidgets import (
    QGroupBox,
    QVBoxLayout,
)

from packages.Startup.DefaultOptions import Default_Subtitle_Extension
from packages.Tabs.GlobalSetting import *
from packages.Tabs.SubtitleTab.Widgets.MatchSubtitleLayout import MatchSubtitleLayout
from packages.Tabs.SubtitleTab.Widgets.SubtitleDelayDoubleSpinBox import SubtitleDelayDoubleSpinBox
from packages.Tabs.SubtitleTab.Widgets.SubtitleExtensionsCheckableComboBox import SubtitleExtensionsCheckableComboBox
from packages.Tabs.SubtitleTab.Widgets.SubtitleLanguageComboBox import SubtitleLanguageComboBox
from packages.Tabs.SubtitleTab.Widgets.SubtitleSetDefaultCheckBox import SubtitleSetDefaultCheckBox
from packages.Tabs.SubtitleTab.Widgets.SubtitleSetForcedCheckBox import SubtitleSetForcedCheckBox
from packages.Tabs.SubtitleTab.Widgets.SubtitleSourceButton import SubtitleSourceButton
from packages.Tabs.SubtitleTab.Widgets.SubtitleSourceLineEdit import SubtitleSourceLineEdit
from packages.Tabs.SubtitleTab.Widgets.SubtitleTrackNameLineEdit import SubtitleTrackNameLineEdit
from packages.Widgets.InvalidPathDialog import *
from packages.Widgets.ReloadFilesDialog import *


# noinspection PyAttributeOutsideInit
class SubtitleSelectionSetting(GlobalSetting):
    tab_clicked_signal = Signal()
    activation_signal = Signal(bool)

    def __init__(self):
        super().__init__()
        self.create_properties()
        self.create_widgets()
        self.setup_widgets()
        self.connect_signals()

    def create_widgets(self):
        self.subtitle_source_label = QLabel("Subtitle Source Folder:")
        self.subtitle_language_label = QLabel("Language:")
        self.subtitle_extension_label = QLabel("Subtitle Extension:")
        self.subtitle_delay_label = QLabel("Subtitle Delay:")
        self.subtitle_source_lineEdit = SubtitleSourceLineEdit()
        self.subtitle_source_button = SubtitleSourceButton()
        self.subtitle_extensions_comboBox = SubtitleExtensionsCheckableComboBox()
        self.subtitle_language_comboBox = SubtitleLanguageComboBox()
        self.subtitle_track_name_lineEdit = SubtitleTrackNameLineEdit()
        self.subtitle_delay_spin = SubtitleDelayDoubleSpinBox()
        self.subtitle_set_forced_checkBox = SubtitleSetForcedCheckBox()
        self.subtitle_set_default_checkBox = SubtitleSetDefaultCheckBox()
        self.subtitle_match_layout = MatchSubtitleLayout(parent=self)
        self.subtitle_options_layout = QHBoxLayout()
        self.subtitle_set_default_forced_layout = QHBoxLayout()
        self.MainLayout = QVBoxLayout()
        self.main_layout = QGridLayout()
        self.subtitle_main_groupBox = QGroupBox()
        self.subtitle_match_groupBox = QGroupBox("Subtitle Matching")
        self.subtitle_match_groupBox.setLayout(self.subtitle_match_layout)

    def setup_widgets(self):
        self.setup_subtitle_main_groupBox()
        self.setup_layouts()

    # noinspection PyUnresolvedReferences
    def connect_signals(self):
        self.subtitle_main_groupBox.toggled.connect(self.activate_tab)
        self.subtitle_source_button.clicked_signal.connect(self.update_folder_path)
        self.subtitle_source_lineEdit.edit_finished_signal.connect(self.update_folder_path)
        self.subtitle_extensions_comboBox.close_list.connect(self.check_extension_changes)
        self.subtitle_match_layout.sync_subtitle_files_with_global_files_after_swap_signal.connect(
            self.sync_subtitle_files_with_global_files)
        self.tab_clicked_signal.connect(self.tab_clicked)

    def create_properties(self):
        self.folder_path = ""
        self.files_names_list = []
        self.files_names_absolute_list = []
        self.current_subtitle_extensions = [Default_Subtitle_Extension]

    def setup_layouts(self):
        self.setup_subtitle_check_default_forced_layout()
        self.setup_subtitle_options_layout()
        self.setup_main_layout()
        self.setLayout(self.MainLayout)
        self.MainLayout.addWidget(self.subtitle_main_groupBox)

    def setup_subtitle_check_default_forced_layout(self):
        self.subtitle_set_default_forced_layout.addWidget(self.subtitle_set_default_checkBox)
        self.subtitle_set_default_forced_layout.addWidget(self.subtitle_set_forced_checkBox)

    def setup_subtitle_options_layout(self):
        self.subtitle_options_layout.addWidget(self.subtitle_extensions_comboBox)
        self.subtitle_options_layout.addWidget(self.subtitle_language_label)
        self.subtitle_options_layout.addWidget(self.subtitle_language_comboBox)
        self.subtitle_options_layout.addWidget(self.subtitle_track_name_lineEdit)
        self.subtitle_options_layout.addWidget(self.subtitle_delay_label)
        self.subtitle_options_layout.addWidget(self.subtitle_delay_spin)
        self.subtitle_options_layout.addSpacing(10)
        self.subtitle_options_layout.addLayout(self.subtitle_set_default_forced_layout)
        self.subtitle_options_layout.addStretch()

    def setup_main_layout(self):
        self.main_layout.addWidget(self.subtitle_source_label, 0, 0)
        self.main_layout.addWidget(self.subtitle_source_lineEdit, 0, 1, 1, 1)
        self.main_layout.addWidget(self.subtitle_source_button, 0, 2)
        self.main_layout.addWidget(self.subtitle_extension_label, 1, 0)
        self.main_layout.addLayout(self.subtitle_options_layout, 1, 1, 1, 2)
        self.main_layout.addWidget(self.subtitle_match_groupBox, 2, 0, 1, -1)

    def setup_subtitle_main_groupBox(self):
        self.subtitle_main_groupBox.setParent(self)
        self.subtitle_main_groupBox.setLayout(self.main_layout)
        self.subtitle_main_groupBox.setTitle("Subtitles")
        self.subtitle_main_groupBox.setCheckable(True)
        self.subtitle_main_groupBox.setChecked(True)

    def update_folder_path(self, new_path: str):
        if new_path != "":
            self.subtitle_source_lineEdit.setText(new_path)
            self.update_files_lists(new_path)
            self.show_subtitle_files_list()

    def update_files_lists(self, folder_path):
        if folder_path == "" or folder_path.isspace():
            self.folder_path = ""
            self.subtitle_source_lineEdit.setText("")
            return
        try:
            self.folder_path = folder_path
            self.files_names_list = self.get_files_list(self.folder_path)
            self.files_names_absolute_list = get_files_names_absolute_list(self.files_names_list, self.folder_path)
        except Exception as e:
            invalid_path_dialog = InvalidPathDialog()
            invalid_path_dialog.execute()

    def check_extension_changes(self, new_extensions):
        if self.current_subtitle_extensions != new_extensions:
            self.current_subtitle_extensions = new_extensions
            self.update_files_lists(self.folder_path)
            self.show_subtitle_files_list()

    def get_files_list(self, folder_path):
        temp_files_names = sort_names_like_windows(names_list=os.listdir(folder_path))
        temp_files_names_absolute = get_files_names_absolute_list(temp_files_names, folder_path)
        current_extensions = self.subtitle_extensions_comboBox.currentData()
        result = []
        for i in range(len(temp_files_names)):
            if os.path.isdir(temp_files_names_absolute[i]):
                continue
            if os.path.getsize(temp_files_names_absolute[i]) == 0:
                continue
            for j in range(len(current_extensions)):
                temp_file_extension_start_index = temp_files_names[i].rfind(".")
                if temp_file_extension_start_index == -1:
                    continue
                temp_file_extension = temp_files_names[i][temp_file_extension_start_index + 1:]
                if temp_file_extension.lower() == current_extensions[j].lower():
                    result.append(temp_files_names[i])
                    break
        return result

    def show_subtitle_files_list(self):
        self.update_other_classes_variables()
        self.subtitle_match_layout.show_subtitle_files()

    def update_other_classes_variables(self):
        self.change_global_last_path_directory()
        self.change_global_subtitle_list()
        self.subtitle_source_button.set_is_there_old_file(len(self.files_names_list) > 0)
        self.subtitle_source_lineEdit.set_is_there_old_file(len(self.files_names_list) > 0)
        self.subtitle_extensions_comboBox.set_is_there_old_file(len(self.files_names_list) > 0)
        self.subtitle_source_lineEdit.set_current_folder_path(self.folder_path)
        self.subtitle_extensions_comboBox.set_current_folder_path(self.folder_path)
        self.subtitle_extensions_comboBox.set_current_files_list(self.files_names_list)

    def change_global_subtitle_list(self):
        GlobalSetting.SUBTITLE_FILES_LIST = self.files_names_list
        GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST = self.files_names_absolute_list

    def show_video_files_list(self):
        if self.subtitle_main_groupBox.isChecked():
            self.subtitle_match_layout.show_video_files()

    def activate_tab(self, on):
        if on:
            self.show_video_files_list()
        else:
            self.subtitle_source_lineEdit.setText("")
            self.subtitle_match_layout.clear_tables()
            self.folder_path = ""
            self.files_names_list = []
            self.files_names_absolute_list = []
            self.current_subtitle_extensions = [Default_Subtitle_Extension]
            self.subtitle_extensions_comboBox.setData(self.current_subtitle_extensions)
            self.subtitle_track_name_lineEdit.setText("")
            self.subtitle_set_forced_checkBox.setChecked(False)
            self.subtitle_set_default_checkBox.setChecked(False)
            self.subtitle_delay_spin.setValue(0)
            GlobalSetting.SUBTITLE_FILES_LIST = []
            GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST = []
            GlobalSetting.SUBTITLE_TRACK_NAME = ""
            GlobalSetting.SUBTITLE_DELAY = 0.0
            GlobalSetting.SUBTITLE_SET_DEFAULT = False
            GlobalSetting.SUBTITLE_SET_FORCED = False
            GlobalSetting.SUBTITLE_LANGUAGE = ""
        self.activation_signal.emit(on)
        GlobalSetting.SUBTITLE_ENABLED = on

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.buttons() == Qt.RightButton:
            self.subtitle_match_layout.clear_subtitle_selection()
        if (QMouseEvent.buttons() == Qt.RightButton or QMouseEvent.buttons() == Qt.LeftButton) and (
                self.subtitle_source_lineEdit.text() == ""):
            self.subtitle_source_lineEdit.setText(self.folder_path)
        return QWidget.mousePressEvent(self, QMouseEvent)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        if self.subtitle_main_groupBox.isChecked():
            self.show_video_files_list()

    def change_global_last_path_directory(self):
        if self.folder_path != "" and not self.folder_path.isspace():
            GlobalSetting.LAST_DIRECTORY_PATH = self.folder_path

    def tab_clicked(self):
        if self.subtitle_main_groupBox.isChecked():
            self.show_subtitle_files_list()
            self.show_video_files_list()
        if not GlobalSetting.JOB_QUEUE_EMPTY:
            self.update_subtitle_set_default_forced_state()
            self.disable_editable_widgets()
        else:
            self.enable_editable_widgets()
            self.update_subtitle_set_default_forced_state()

    def update_subtitle_set_default_forced_state(self):
        self.subtitle_set_default_checkBox.update_check_state()
        self.subtitle_set_forced_checkBox.update_check_state()

    def disable_editable_widgets(self):
        self.subtitle_source_lineEdit.setEnabled(False)
        self.subtitle_source_button.setEnabled(False)
        self.subtitle_extensions_comboBox.setEnabled(False)
        self.subtitle_language_comboBox.setEnabled(False)
        self.subtitle_track_name_lineEdit.setEnabled(False)
        self.subtitle_delay_spin.setEnabled(False)
        self.subtitle_set_default_checkBox.setEnabled(False)
        self.subtitle_set_forced_checkBox.setEnabled(False)
        self.subtitle_main_groupBox.setCheckable(False)
        self.subtitle_match_layout.disable_editable_widgets()

    def enable_editable_widgets(self):
        self.subtitle_source_lineEdit.setEnabled(True)
        self.subtitle_source_button.setEnabled(True)
        self.subtitle_extensions_comboBox.setEnabled(True)
        self.subtitle_language_comboBox.setEnabled(True)
        self.subtitle_track_name_lineEdit.setEnabled(True)
        self.subtitle_delay_spin.setEnabled(True)
        self.subtitle_set_default_checkBox.setEnabled(True)
        self.subtitle_set_forced_checkBox.setEnabled(True)
        if GlobalSetting.SUBTITLE_ENABLED:
            self.subtitle_main_groupBox.setCheckable(True)
        else:
            self.subtitle_main_groupBox.setCheckable(True)
            GlobalSetting.SUBTITLE_ENABLED = False
            self.subtitle_main_groupBox.setChecked(GlobalSetting.SUBTITLE_ENABLED)
        self.subtitle_match_layout.enable_editable_widgets()

    def sync_subtitle_files_with_global_files(self):
        self.files_names_list = GlobalSetting.SUBTITLE_FILES_LIST
        GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST = get_files_names_absolute_list(self.files_names_list,
                                                                                        self.folder_path)
        self.files_names_absolute_list = GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST

        self.update_other_classes_variables()
