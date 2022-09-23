import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw


class HumbleComboBox(qtw.QComboBox):
    def __init__(self, *args):
        super().__init__(*args)
        self.setFocusPolicy(qtc.Qt.FocusPolicy.StrongFocus)

    def focusInEvent(self, event):
        self.setFocusPolicy(qtc.Qt.FocusPolicy.WheelFocus)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.setFocusPolicy(qtc.Qt.FocusPolicy.StrongFocus)
        super().focusOutEvent(event)

    def wheelEvent(self, event):
        if self.hasFocus():
            return super().wheelEvent(event)
        else:
            event.ignore()