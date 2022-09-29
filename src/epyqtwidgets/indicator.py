import PyQt5.QtWidgets as qtw


class Indicator(qtw.QWidget):
    DEFAULT_SIZE = 20

    def __init__(self, color, *args, indicator_size=None, **kwargs):
        super().__init__(*args, **kwargs)
        size = indicator_size or self.DEFAULT_SIZE
        self.setMinimumWidth(size)
        self.setMaximumWidth(size)
        self.setMaximumHeight(size)
        self.setMinimumHeight(size)
        self.setAutoFillBackground(True)
        self.set_color(color)

    def set_color(self, color):
        self.setStyleSheet(f"background-color: {color};")
