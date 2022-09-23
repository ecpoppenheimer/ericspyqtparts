import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw


class HumbleSlider(qtw.QSlider):
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


class DelayedSlider(HumbleSlider):
    def __init__(self, orientation=qtc.Qt.Orientation.Horizontal, time_delay=.05):
        super().__init__(orientation)

        self._time_delay_ms = int(time_delay * 1000)
        self._has_time_deferred_call = False
        self._timer = qtc.QTimer()

        self.valueChanged.connect(self._emit_value_changed)
        self.valueChanged = DelayedSliderValueChanged()

    def _emit_value_changed(self):
        if not self._has_time_deferred_call:
            self._has_time_deferred_call = True
            self._timer.singleShot(self._time_delay_ms, self._emit_timed_value_changed)

    def _emit_timed_value_changed(self):
        self._has_time_deferred_call = False
        self.valueChanged.sig.emit(self.value())


class DelayedSliderValueChanged(qtc.QObject):
    sig = qtc.pyqtSignal(int)

    def connect(self, *args):
        self.sig.connect(*args)
