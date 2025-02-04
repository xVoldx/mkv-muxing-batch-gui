from PySide2.QtGui import Qt
from PySide2.QtWidgets import QComboBox

from packages.Startup.InitializeScreenResolution import screen_size
from packages.Startup.PreDefined import AllAudiosTracks
from packages.Tabs.GlobalSetting import GlobalSetting


class MakeThisTrackDefaultComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.addItems(AllAudiosTracks)
        self.setMinimumWidth(screen_size.width() // 12)
        self.setMaximumWidth(screen_size.width() // 6)
        self.setMaxVisibleItems(8)
        self.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.setCurrentIndex(-1)
        self.disable_track_text_from_being_selected()
        self.disable_language_text_from_being_selected()
        self.hint_when_enabled = ""
        self.setDisabled(True)
        self.model().item(11).setEnabled(False)
        self.model().item(11).setTextAlignment(Qt.AlignCenter)

    def disable_track_text_from_being_selected(self):
        for i in range(len(AllAudiosTracks)):
            if AllAudiosTracks[i] == "---Tracks---":
                self.model().item(i).setEnabled(False)
                self.model().item(i).setTextAlignment(Qt.AlignCenter)
                break

    def disable_language_text_from_being_selected(self):
        for i in range(len(AllAudiosTracks)):
            if AllAudiosTracks[i] == "---Languages---":
                self.model().item(i).setEnabled(False)
                self.model().item(i).setTextAlignment(Qt.AlignCenter)
                break

    def setEnabled(self, new_state: bool):
        super().setEnabled(new_state)
        if not new_state and not GlobalSetting.JOB_QUEUE_EMPTY:
            if self.hint_when_enabled != "":
                self.setToolTip("<nobr>" + self.hint_when_enabled + "<br>" + GlobalSetting.DISABLE_TOOLTIP)
            else:
                self.setToolTip("<nobr>" + GlobalSetting.DISABLE_TOOLTIP)
        else:
            self.setToolTip(self.hint_when_enabled)

    def setDisabled(self, new_state: bool):
        super().setDisabled(new_state)
        if new_state and not GlobalSetting.JOB_QUEUE_EMPTY:
            if self.hint_when_enabled != "":
                self.setToolTip("<nobr>" + self.hint_when_enabled + "<br>" + GlobalSetting.DISABLE_TOOLTIP)
            else:
                self.setToolTip("<nobr>" + GlobalSetting.DISABLE_TOOLTIP)
        else:
            self.setToolTip(self.hint_when_enabled)

    def setToolTip(self, new_tool_tip: str):
        if self.isEnabled() or GlobalSetting.JOB_QUEUE_EMPTY:
            self.hint_when_enabled = new_tool_tip
        super().setToolTip(new_tool_tip)
