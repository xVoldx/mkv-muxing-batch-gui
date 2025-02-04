from PySide2.QtCore import Signal
from PySide2.QtWidgets import QPushButton

from packages.Startup import GlobalFiles
from packages.Tabs.GlobalSetting import GlobalSetting


class MoveChapterTopButton(QPushButton):
    swap_happened_signal = Signal()
    selected_row_after_swap = Signal(int)

    def __init__(self):
        super().__init__()
        self.current_index = -1
        self.max_index = -1
        self.hint_when_enabled = ""
        self.setIcon(GlobalFiles.TopIcon)
        self.setup_tool_tip_hint()
        self.clicked.connect(self.clicked_button)

    def clicked_button(self):
        current_index = self.current_index
        if current_index != 0 and current_index != -1:
            temp_for_swap = GlobalSetting.CHAPTER_FILES_LIST[current_index]
            GlobalSetting.CHAPTER_FILES_LIST[current_index] = GlobalSetting.CHAPTER_FILES_LIST[0]
            GlobalSetting.CHAPTER_FILES_LIST[0] = temp_for_swap
            self.swap_happened_signal.emit()
            self.selected_row_after_swap.emit(0)

    def setup_tool_tip_hint(self):
        self.setToolTip("Move Chapter To Top (Ctrl+PageUp)")
        self.setToolTipDuration(3000)

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
