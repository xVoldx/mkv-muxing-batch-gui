from PySide2.QtWidgets import QLineEdit

from packages.Startup.InitializeScreenResolution import screen_size
from packages.Tabs.GlobalSetting import GlobalSetting


class SubtitleTrackNameLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.hint_when_enabled = ""
        self.setPlaceholderText("Subtitle Track Name")
        self.setMinimumWidth(screen_size.width() // 10)
        self.setMaximumWidth(screen_size.width() // 8)
        self.setClearButtonEnabled(True)
        self.setToolTip("Subtitle Track Name")
        self.textEdited.connect(self.change_global_subtitle_track_name)

    def change_global_subtitle_track_name(self):
        GlobalSetting.SUBTITLE_TRACK_NAME = self.text()

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
